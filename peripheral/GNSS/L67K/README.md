### L76K

注：暂时只支持EC600U CNLB。

**引用：**

```python
from usr.l67k_module import Gnss
```

**实例化参数：**

| 名称     | 必填 | 类型 | 说明                                                         |
| -------- | ---- | ---- | ------------------------------------------------------------ |
| uartn    | 是   | int  | UARTn范围为0-3：<br/>0-UART0 - DEBUG PORT<br/>1-UART1 – BT PORT<br/>2-UART2 – MAIN PORT<br/>3-UART3 – USB CDC PORT |
| baudrate | 是   | int  | 波特率，常用波特率都支持，如4800、9600、19200、38400、57600、115200、230400等 |
| databits | 是   | int  | 数据位（5 ~ 8），展锐平台当前仅支持8位                       |
| parity   | 是   | int  | 奇偶校验（0 – NONE，1 – EVEN，2 - ODD）                      |
| stopbits | 是   | int  | 停止位（1 ~ 2）                                              |
| flowctl  | 是   | int  | 硬件控制流（0 – FC_NONE， 1 – FC_HW）                        |

```python
gnss = Gnss(1, 9600, 8, 0, 1, 0)  
```

**接口函数：**

l **read_gnss(self,retry = 3,debug = 0)**

​	读取GNSS数据。

​	注：本函数会默认读取一（retry）次GNSS数据，并检查其GGA，RMC，GSV数据是否有效，若存在有效数据，则返回有效数据位和GNSS原始数据的二元组。

参数：

| 名称  | 必填 | 类型 | 说明                                                         |
| ----- | ---- | ---- | ------------------------------------------------------------ |
| retry | 否   | int  | 可选参数，可不填该参数；表示当读取的GNSS无效时，自动重新读取的最大尝试次数，如果读取数据长度为0（即没有读取到数据）则直接退出；这里会进行自动重新读取的前提是，当前读取的这一包原始GNSS数据中，如果GNGGA、GNRMC和GPGSV语句有任何一种没有找到或者是找到但是数据是无效的，那么就会重新去读取下一包数据，直到GNGGA、GNRMC和GPGSV语句都找到并且数据有效或者达到最大尝试次数退出。默认为1，表示只读取一次数据。 |
| debug | 否   | int  | 可选参数，可不填该参数，默认为0；表示在读取解析GNSS数据过程中，是否输出一些调试信息，为0表示不输出详细信息，为1表示输出详细信息，方便用户直观的看到解析结果以及进行比对；这里要注意的是，debug为0，并不是一点调试信息都不输出，而是仅仅输出一些简单的基本的信息，比如没有从原始的GNSS数据中找到对应数据或数据无效，则提示数据无效或者没有找到相关数据之类的基本信息，具体可参考示例。 |

返回值：

```
-1 ：失败
(有效位，原始GNSS数据) ：成功，有效位(0x01-0x07)：0x04 gga有效；0x02 rmc有效；0x01 gsv有效，
```

l **isFix()**

​	检查是否定位成功。

参数：

​    无

返回值：

​      0 - 失败

​	  1- 成功

l **getLocation()**

​	获取GPS模块定位的经纬度信息。

参数：

​    无

返回值：

```
成功返回GPS模块定位的经纬度信息，失败返回整型-1；
成功时返回值格式如下：
        (longitude, lon_direction, latitude, lat_direction)
        longitude - 经度，float型
        lon_direction - 经度方向，字符串类型，E表示东经，W表示西经
        latitude - 纬度，float型
        lat_direction - 纬度方向，字符串类型，N表示北纬，S表示南纬
```

l **getUtcTime()**

​	获取定位的UTC时间。

参数：

​    无

返回值：

​      成功返回UTC时间，字符串类型，失败返回整型-1。

l **getLocationMode()**

​	获取GPS模块定位模式。

参数：

​    无

返回值：

```
-1   获取失败，串口未读到数据或未读到有效数据
0    定位不可用或者无效
1    定位有效,定位模式：GPS、SPS 模式
2    定位有效,定位模式： DGPS、DSPS 模式
6    估算（航位推算）模式
```

l **getUsedSateCnt()**

​	获取GPS模块定位使用卫星数量。

参数：

​    无

返回值：

​      成功返回GPS模块定位使用卫星数量，返回值类型为整型，失败返回整型-1。

l **getViewedSateCnt()**

​	获取GPS模块定位可见卫星数量。

参数：

​    无

返回值：

​      成功返回GPS模块定位可见卫星数量，整型值，失败返回整型-1。

l **getGeodeticHeight()**

​	获取GPS模块定位海拔高度。

参数：

​    无

返回值：

​      成功返回浮点类型海拔高度(单位:米)，失败返回整型-1。

l **getCourse()**

​	获取可视的GNSS卫星方位角。

参数：

​    无

返回值：

​		返回所有可视的GNSS卫星方位角，范围：0 ~ 359，以正北为参考平面。
​        返回形式为字典，其中key表示卫星编号，value表示方位角。
​        要注意，value的值可能是一个整型值，也可能是''，这取决于原始的GNSS数据中GPGSV语句中方位角是否有值。

l **getSpeed()**

​	获取GPS模块对地速度。

参数：

​    无

返回值：

​      成功返回GPS模块对地速度(单位:KM/h)，浮点类型，失败返回整型-1。

**demo**：

```python
gnss = Gnss(1, 9600, 8, 0, 1, 0)
for i in range(10):
    print("开始读取GNSS数据")
    print(gnss.read_gnss(retry=3))
    utime.sleep(1)
    print("定位是否成功 {}".format(gnss.isFix()))
    print("定位时间 {}".format(gnss.getUtcTime()))
    print("GPS定位模式 {}".format(gnss.getLocationMode()))
    print("GPS使用卫星数量 {}".format(gnss.getUsedSateCnt()))
    print("GPS位置 {}".format(gnss.getLocation()))
    print("GPS模块定位可见卫星数量 {}".format(gnss.getViewedSateCnt()))
    print("GPS模块定位海拔高度 {}".format(gnss.getGeodeticHeight()))
    print("获取可视的GNSS卫星方位角 {}".format(gnss.getCourse()))
    print("获取GPS模块对地速度 {}".format(gnss.getSpeed()))
    utime.sleep(1)
```

