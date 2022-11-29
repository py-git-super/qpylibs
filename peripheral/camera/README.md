## 数码管

### tm1650

**类引用：**

```python
from usr.tm1650 import Tm1650
```

 

**实例化参数：**

| 名称 | 必填 | 类型 | 说明              |
| ---- | ---- | ---- | ----------------- |
| dio  | 是   | int  | DIO, 例Pin.GPIO13 |
| clk  | 是   | int  | CLK,例Pin.GPIO12  |

```python
tube = Tm1650(Pin.GPIO13, Pin.GPIO12)
```

**接口函数：**

l **on(), off ()**

​	开启数码管, 关闭数码管。

参数：

​    无

返回值：

​       无

l **all_show (), all_clear()**

​	全显和全部消除。(顺序都是从左到右)

参数：

​    无

返回值：

​       无

 

l **show_num (num)**

​	显示数字，不满四位的靠右显示。

参数：

| 名称 | 类型 | 说明        |
| ---- | ---- | ----------- |
| num  | int  | -999 ~ 9999 |

返回值：

| 名称 | 类型 | 说明                |
| ---- | ---- | ------------------- |
| ret  | int  | -1:error  0:success |

 

l **show_str(str)**

​	显示字符串,不足四位的靠右显示。

参数：

| 名称 | 必填 | 类型 | 说明         |
| ---- | ---- | ---- | ------------ |
| str  | 是   | str  | 四个字符以内 |

返回值：

| 名称 | 类型 | 说明                |
| ---- | ---- | ------------------- |
| ret  | int  | -1:error  0:success |

 

l **show_dp(bit)**

​	显示点。

参数：

| 名称 | 必填 | 类型 | 说明 |
| ---- | ---- | ---- | ---- |
| bit  | 是   | int  | 1-4  |

返回值：

| 名称 | 类型 | 说明                |
| ---- | ---- | ------------------- |
| ret  | int  | -1:error  0:success |

l **clear_bit (bit)**

​	清除某位显示。

参数：

| 名称 | 必填 | 类型 | 说明 |
| ---- | ---- | ---- | ---- |
| bit  | 是   | int  | 1-4  |

返回值：

| 名称 | 类型 | 说明                |
| ---- | ---- | ------------------- |
| ret  | int  | -1:error  0:success |

**demo：**

```python
tube = Tm1650(Pin.GPIO13, Pin.GPIO12) #600U PIN60,PIN59
tube.on()
tube.all_show()
utime.sleep(1)
tube.clear_bit(3)
utime.sleep(1)
tube.all_clear()
utime.sleep(1)
tube.show_dp(3)
utime.sleep(1)
tube.show_str("PPJ")
utime.sleep(1)
tube.show_num(-537)
utime.sleep(1)
tube.show_num(8537)
utime.sleep(1)
tube.circulate_show("AbCdEFH")
```

