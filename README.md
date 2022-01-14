# 目录

### cp_lookup

- ###### cp_trans:
  
  省级行政区与地级行政区的对应关系

- ###### Inverse_dic( ):
  
  反转dic对象的key和value

- ###### ptwoc( ):
  
  根据省级行政区域名（及其简称）给出下辖所有地级行政区域名单

- ###### ctwop( ):
  
  根据地级行政区域名（及其简称）给出所属省级行政区名

- ###### add_pro( ):
  
  根据一列地级行政区名给出一列对应的省级行政区域名

- ###### fiilup_city( ):
  
  对一列不完整的地级行政区名单进行名称补完

---

### add_ll

- ###### pro_info( ):
  
  返回两个值：省级行政区的经度与纬度

- ###### city_info( ):
  
  返回三个值：地级行政区的省、经度与纬度

- ###### pro_add( ):
  
  对一列省级行政区返回对应的经度与纬度（两个值）

- ###### city_add(mode):
  
  若mode='1'，对一列地级行政区返回对应的省
  
  若mode='2'，对一列地级行政区返回对应的经纬度（两个值）
  
  否则，返回一列 'x'

---

### critic

- ##### Critic:
  
  对pd.dataframe对象进行Critic类的实例化。pd.dataframe对象的前三列不能为指标
1. **vardata( )：**获取指标变异性数据
2. **__corrdata( )：**获取指标冲突性数据
3. **weights( )：**得到指标critic权重数据

---

### rsr

- ##### Rsr
  
  对pd.dataframe对象进行Rsr类的实例化。pd.dataframe对象的前三列不能为指标
1. **score_matrix1(bv_list)**：计算整次秩和比法得分。bv_list是由各指标正向最佳贡献值构成的列表

2. **score_matrix11(bv_list)**：优化了距离矩阵计算方法，编秩时不使用set()的整次秩和比法，使用方法同上。

3. **score_matrix2(bv_list)**：计算非整次秩和比法得分。bv_list是由各指标正向最佳贡献值构成的列表
   
   注：所谓正向最佳贡献值，指的是从正面考虑指标贡献度时的最佳值。比如用不同指标合成金融风险指数(相较于“安全”而言“风险”是一个负面形容)，因此从正面考虑时对于正向指标其最佳值便是最低值，负向指标最佳值是最高值，适度指标由文献或前人研究来确定。

---

### NonDimension

- ##### **NonDimension**
  
  对pd.dataframe对象进行NonDimension类实例化。
1. **tiny_convert(mode, change_list)**：将数组中极小值指标转化为极大值指标。change_list为存放需转化指标索引的列表；mode = "0"时采用倒数转换法，mode = "1"时采用被最大值相减的方法。

2. **middle_convert(change_list, best_value)**：将数组中中间型指标转化为极大值指标。change_list为存放需转化指标索引的列表；best_value为存放中间值指标最佳值的列表。

3. **moderate_convert(change_list, low_limit, high_limit)**：将数组中适度型指标转化为极大值指标。change_list为存放需转化指标索引的列表；low_limit与high_limit分别为存放适度下界与上界的列表。

4. **toone(mode)**：将数组矩阵归一化。mode = "0"时进行标准归一化， mode= "1"时进行平均归一化；mode = "2"时进行Z-score规范化；mode = "3"时进行向量规范化。
   
   - ###### tiny_cinvert(mode, change_list):
   
   将数组中极小值指标转化为极大值指标。change_list为存放需转化指标索引的列表；mode = "0"时采用倒数转换法，mode = "1"时采用被最大值相减的方法。
   
   - ###### middle_convert(change_list, best_value):
   
   将数组中中间型指标转化为极大值指标。change_list为存放需转化指标索引的列表；best_value为存放中间值指标最佳值的列表。
   
   - ###### moderate_convert(change_list, low_limit, high_limit):
   
   将数组中适度型指标转化为极大值指标。change_list为存放需转化指标索引的列表；low_limit与high_limit分别为存放适度下界与上界的列表。
   
   - ###### toone(mode):
   
   将数组矩阵归一化。mode = "0"时进行标准归一化， mode= "1"时进行平均归一化；mode = "2"时进行Z-score规范化；mode = "3"时进行向量规范化。

---

### topsis

- ##### **Topsis**
  
  对pd.dataframe对象进行Topsis类实例化
1. **score_matrix(weihjts)**：计算得分矩阵，weights为权重矩阵。得分越低越优秀。

---
