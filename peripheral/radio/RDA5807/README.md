### rda5807

**类引用：**

```python
from usr.rda5807_module import Rda5807
```

 

**实例化参数：**

| 名称   | 必填 | 类型 | 说明             |
| ------ | ---- | ---- | ---------------- |
| RDACLK | 是   | int  | CLK, 例Pin.GPIO2 |
| RDADIO | 是   | int  | DIO, 例Pin.GPIO3 |

```python
pm = RDA5807(rdaclk = Pin.GPIO2,rdadio = Pin.GPIO3)
```

**接口函数：**

l **fm_enable(flag)**

​	使能芯片。

参数：

| 名称 | 必填 | 类型 | 说明           |
| ---- | ---- | ---- | -------------- |
| flag | 是   | int  | 1.使能 0：禁用 |

返回值：

​       无

l **vol_set (vol)**

​	音量设置。

参数：

| 名称 | 必填 | 类型 | 说明       |
| ---- | ---- | ---- | ---------- |
| vol  | 是   | int  | 音量：0-15 |

返回值：

​       无

l **mute_set (mute)**

​	静音设置。

参数：

| 名称 | 必填 | 类型 | 说明            |
| ---- | ---- | ---- | --------------- |
| mute | 是   | int  | 1 静音 0 不静音 |

返回值：

​       无

l **rssi_get ()**

​	信号强度获取。

参数：

​    无。

返回值：

| 名称 | 类型 | 说明     |
| ---- | ---- | -------- |
| rssi | int  | 信号强度 |

l **seekth_set (rssi)**

​	自动搜台信号设置阈值强度。

参数：

| 名称 | 必填 | 类型 | 说明       |
| ---- | ---- | ---- | ---------- |
| rssi | 是   | int  | 信号值0-15 |

返回值：

​       无

l **seek_channel ()**

​	自动搜台。

参数：

​    无

返回值：

​       无

**demo：**

```python
test_pm = RDA5807(rdaclk = Pin.GPIO2,rdadio = Pin.GPIO3)
test_pm._rda_init()
print("init finish. ")
test_pm.seek_channel()
print("channel seeking...")
test_pm.vol_set(15)
print('vol seted to 15.')
test_pm.fm_enable(0)
print("radio forbid.")
```

