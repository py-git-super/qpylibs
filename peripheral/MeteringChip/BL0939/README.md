### BL0939

**类引用：**

```python
from usr.bl0939_module import Bl0939
```

 **实例化参数：**

| 名称 | 必填 | 类型 | 说明                    |
| ---- | ---- | ---- | ----------------------- |
| port | 否   | int  | SPI 的通道              |
| mode | 否   | int  | SPI 的工作模式，固定为1 |
| clk  | 否   | int  | 时钟频率，固定为0       |

```python
bl0939 = Bl0939(port=1)
```

 **接口函数**

l **read()**

​	读取寄存器A,B电流有效值，电压有效值

参数：

​    无。

返回值：

| 名称      | 类型  | 说明                    |
| --------- | ----- | ----------------------- |
| (ia,ib,v) | tuple | IA_RMS,IB_RMS,V_RMS读数 |

 

l **current_a**

​	property方法，返回A电流有效值。

 

l **current_b**

​	property方法，返回A电流有效值。

 

l **voltage**

​	property方法，返回电压有效值。