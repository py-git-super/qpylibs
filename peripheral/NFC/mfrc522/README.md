### mfrc522

**类引用：**

```python
from usr.mfrc522_module import Mfrc522_spi
```

 

**实例化参数：**

| 名称    | 必填 | 类型 | 说明                    |
| ------- | ---- | ---- | ----------------------- |
| pin_rst | 是   | int  | reset引脚，例Pin.GPIO12 |
| pin_irq | 是   | int  | 中断引脚, 例Pin.GPIO11  |

```
reader = Mfrc522_spi(pin_rst=Pin.GPIO12, pin_irq=Pin.GPIO11)
```

**接口函数：**

l **read_id()**

​	读卡的id。

参数：

​    无

返回值：

| 名称 | 类型 | 说明 |
| ---- | ---- | ---- |
| id   | int  | 卡id |

l **AntennaOn()**

​	开启天线。

参数：

​	无

返回值：

​    无

l **AntennaOff()**

​	关闭天线。

参数：

​	无

返回值：

​       无

l **MFRC522_Request(reqMode)**

​	寻卡。

参数：

​    

| 名称    | 必填 | 类型 | 说明                                                         |
| ------- | ---- | ---- | ------------------------------------------------------------ |
| reqMode | 是   | int  | 0x26：寻天线区内未进入休眠状态的卡<br />0x52：寻天线区内全部卡 |

返回值：

| 名称    | 类型 | 说明                                                         |
| ------- | ---- | ------------------------------------------------------------ |
| status  | int  | 0：成功<br />其他：失败                                      |
| TagType | int  | 卡种类：0x4400 = Mifare_UltraLight<br/>//          0x0400 = Mifare_One(S50)<br/>//          0x0200 = Mifare_One(S70)<br/>//          0x0800 = Mifare_Pro(X)<br/>//          0x4403 = Mifare_DESFire |

 **MFRC522_Anticoll()**

​	防冲撞。

参数：

​    无

返回值：

| 名称    | 类型 | 说明                                                 |
| ------- | ---- | ---------------------------------------------------- |
| status  | int  | 0：成功<br />其他：失败                              |
| id_read | int  | 长度5的存储卡id的list，可用uid_to_num接口转成int型id |

 **MFRC522_SelectTag(serNum)**

​	选择卡片。

参数：

| 名称   | 必填 | 类型 | 说明                              |
| ------ | ---- | ---- | --------------------------------- |
| serNum | 是   | list | MFRC522_Anticoll()返回的id 的list |

返回值：

| 名称    | 类型 | 说明                                                 |
| ------- | ---- | ---------------------------------------------------- |
| status  | int  | 0：成功<br />其他：失败                              |
| id_read | int  | 长度5的存储卡id的list，可用uid_to_num接口转成int型id |