# ADC

#### 介绍
ADC 读取通道电压

#### 参数说明

'''
ADC通道
EC100Y平台对应引脚如下
ADC0 – 引脚号39
ADC1 – 引脚号81
EC600S/EC600N平台对应引脚如下
ADC0 – 引脚号19
EC800N/BC25PA平台对应引脚如下
ADC0 – 引脚号9
EC600U平台对应引脚如下
ADC0 – 引脚号19
ADC1 – 引脚号20
ADC2 – 引脚号113
ADC3 – 引脚号114
EC200U平台对应引脚如下
ADC0 – 引脚号45
ADC1 – 引脚号44
ADC2 – 引脚号43
'''


#### 使用说明

1.  实例1
 

```
from usr.ADC import ADCclass as ADC

adc = ADC()
adc.open()              # ADC 功能初始化
adc.read(ADC.ADC0)      # 读取ADC0电压
adc.close()             # 关闭ADC
```
