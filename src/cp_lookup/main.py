import imp
from math import radians, cos, sin, asin, sqrt
from jieba import lcut
import jieba
import polars as pl
from .special import SIMILAR_NAMES, ZXCITIES, SAMENAMES
from .packagepath import full_path

data = pl.read_csv(full_path())
data["adcode"] = data["adcode"].apply(str)

SPECIAL_WORDS = [area for area in data["name"] if len(lcut(area)) != 1]
for word in SPECIAL_WORDS:
    jieba.add_word(word)


class AreaNameError(Exception):
    """自定义异常类"""

    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


def _prov_codes() -> list[str]:
    adcodes = data["adcode"]
    return [code for code in adcodes if str.endswith(code, "0" * 10)]


def _city_codes() -> list[str]:
    adcodes = data["adcode"]
    prov_codes = _prov_codes()
    return [
        code
        for code in adcodes
        if (str.endswith(code, "0" * 8)) & (code not in prov_codes)
    ]


def _county_codes() -> list[str]:
    adcodes = data["adcode"]
    prov_codes = _prov_codes()
    city_codes = _city_codes()
    return [
        code for code in adcodes if (code not in prov_codes) & (code not in city_codes)
    ]


PROVINCECODE: list[str] = _prov_codes()
CITYCODE: list[str] = _city_codes()
COUNTYCODE: list[str] = _county_codes()
NOTPROVINCE: list[str] = CITYCODE + COUNTYCODE
NOTCOUNTY: list[str] = PROVINCECODE + CITYCODE


def _level_choose(level: str | None) -> pl.DataFrame:
    options = ["province", "city", "county", "not province", "not county", None]
    assert level in options, "错误的等级选项！！！"
    match level:
        case "province":
            return data[data["adcode"].is_in(PROVINCECODE)]
        case "city":
            return data[data["adcode"].is_in(CITYCODE)]
        case "county":
            return data[data["adcode"].is_in(COUNTYCODE)]
        case "not province":
            return data[data["adcode"].is_in(NOTPROVINCE)]
        case "not county":
            return data[data["adcode"].is_in(NOTCOUNTY)]
        case _:
            return data


def _num_one(info: list[str], level_data: pl.DataFrame):
    addr = info[0]
    if len(level_data[level_data["name"].str.contains(addr)]) != 1:
        raise AreaNameError("地名重复或有误！！！")
    else:
        return level_data[level_data["name"].str.contains(addr)]


def _num_two(info: list[str], level_data: pl.DataFrame):
    father, addr = info
    if father == addr:
        addr_name = SAMENAMES[addr][1]
        return data[data["name"] == addr_name]
    else:
        fdata = _level_choose("not county")
        fcode = fdata[fdata["name"].str.contains(father)][0, "adcode"]
        addr_codes = level_data[level_data["name"].str.contains(addr)]["adcode"]
        for code in addr_codes:
            if (code[:4] == fcode[:4]) | (code[:2] == fcode[:2]):
                return level_data[level_data["adcode"] == code]


def _num_three(info: list[str], level_data: pl.DataFrame):
    gdfather, father, addr = info
    gddata = _level_choose("province")
    fdata = _level_choose("city")
    ldata = _level_choose("county")
    if len(level_data[level_data["name"].str.contains(addr)]) == 1:
        return level_data[level_data["name"].str.contains(addr)]
    gdcode = gddata[gddata["name"].str.contains(gdfather)][0, "adcode"]
    fdcode = fdata[fdata["name"].str.contains(father)][0, "adcode"]
    addr_codes = ldata[ldata["name"].str.contains(addr)]["adcode"]
    for code in addr_codes:
        if code[:2] == fdcode[:2] == gdcode[:2]:
            return level_data[level_data["adcode"] == code]


class Addr:
    """以区域名构建一个地区的类，包含该地区的adcode、区域名、经纬度等信息。"""

    def __init__(self, name: str, adcode: int | None = None, level: str | None = None):
        if adcode:
            self.addr = data[data["adcode"] == adcode]
        elif name in SIMILAR_NAMES.keys():
            self.addr = data[data["adcode"] == SIMILAR_NAMES.get(name)]
        else:
            obj_area_data = _level_choose(level) if level else data
            info = lcut(name)
            nums = len(info)
            match nums:
                case 1:
                    self.addr = _num_one(info, obj_area_data)
                case 2:
                    self.addr = _num_two(info, obj_area_data)
                case 3:
                    self.addr = _num_three(info, obj_area_data)

    def _belongs_to(self) -> str | None:
        assert isinstance(self.addr, pl.DataFrame)
        code = self.addr[0, "adcode"]
        fcode = (
            code[:2] + "0" * 10 if str.endswith(code, "0" * 8) else (code[:4] + "0" * 8)  # type: ignore
        )
        fdata = data[data["adcode"] == fcode]
        return fdata[0, "name"]  # type: ignore

    def _coordinate(self) -> tuple[float, float]:
        lat = self.addr[0, "latitude"]  # type: ignore
        lon = self.addr[0, "longitude"]  # type: ignore
        return lat, lon  # type: ignore


def lookup(name: str, level: str | None = None) -> str | None:
    """根据地名简称查找全称

    Args:
        name (str): 待查找地名

    Returns:
        str | None: 地名全称
    """
    if name in ZXCITIES.keys():
        new_name = ZXCITIES[name]
        obj_area = Addr(new_name, level="province").addr
    else:
        obj_area = Addr(name, level=level).addr
    return obj_area[0, "name"]  # type: ignore


def belongs_to(name: str, level: str | None = None) -> str | None:
    """根据地名查找其上级行政区名称

    Args:
        name (str): 待查找地名

    Returns:
        str | None: 上级行政区全称
    """
    if name in ZXCITIES.keys():
        new_name = ZXCITIES[name]
        obj_area = Addr(new_name, level="province")
    else:
        obj_area = Addr(name, level=level)
    return obj_area._belongs_to()


def coordinate(name: str, level: str | None = None) -> tuple[float, float]:
    """根据区域名得到其行政中心的坐标

    Args:
        name (str): 行政区名称

    Returns:
        tuple[float, float]: 行政中心经纬度
    """
    if name in ZXCITIES.keys():
        new_name = ZXCITIES[name]
        obj_area = Addr(new_name, level="province")
    else:
        obj_area = Addr(name, level=level)
    lat, lon = obj_area._coordinate()
    return lat, lon


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """利用两个地点的经纬度计算球面距离

    Args:
        lat1 (float): 地区1的纬度
        lon1 (float): 地区1的经度
        lat2 (float): 地区2的纬度
        lon2 (float): 地区2的经度

    Returns:
        float: 球面距离，单位：km
    """
    # 将十进制度数转化为弧度
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])  # radians：将角度转化为弧度

    # haversine（半正矢）公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r


def dist(
    city1: str, city2: str, level1: str | None = None, level2: str | None = None
) -> float:
    """利用两个地区的城市名称计算球面距离

    Args:
        city1 (str): 地区1的城市名称
        city2 (str): 地区2的城市名称

    Returns:
        float: 球面距离，单位：km
    """
    city1_lat, city1_lon = coordinate(city1, level=level1)
    city2_lat, city2_lon = coordinate(city2, level=level2)
    return haversine(city1_lat, city1_lon, city2_lat, city2_lon)
