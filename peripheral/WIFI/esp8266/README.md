### ESP8266

​	目前仅支持ASR平台，目前仅支持ap模式。

**类引用：**

```python
from usr.esp8266_module import Esp8266_ap
```

 

**实例化参数：**

| 名称 | 必填 | 类型 | 说明                         |
| ---- | ---- | ---- | ---------------------------- |
| uart | 是   | int  | 根据串口wiki说明，指定串口号 |

```python
esp8266 = Esp8266_ap(UART.UART2)
```

**接口函数：**

l **wifi_on()**

​	开启模块wifi功能，请确保开启前600X已拨号成功。

参数：

​	无

返回值：

​	   0 ：成功 

​	  -1 ： 失败

l **wifi_off()**

​	关闭模块wifi功能。

参数：

​	无

返回值：

​	无

l **set_ap(name=None,pwd=None)**

​	设置wifi用户名和密码。

​	注：只传入name则只修改用户名，只传入pwd则只修改密码，二者至少得有一个。

参数：

| 名称 | 必填 | 类型 | 说明     |
| ---- | ---- | ---- | -------- |
| name | 否   | str  | wifi名称 |
| pwd  | 否   | str  | wifi密码 |

返回值：

​	   0 ：成功 

​	  -1 ： 失败

**demo：**

```python
esp8266 = Esp8266_ap(UART.UART2)
esp8266.set_ap(name='大好年华',pwd='11111111')
err = esp8266.wifi_on()
if err == 0:
   print('slip network card create success')
else:
   print('slip network card create fail')
```
