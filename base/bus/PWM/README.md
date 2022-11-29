# PWM

#### 介绍
PWM开启和关闭输出

#### 常量说明

| 常量     | 说明 | 使用平台                                      |
| -------- | ---- | --------------------------------------------- |
| PWM.PWM0 | PWM0 | EC600S / EC600N / EC100Y/EC600U/EC200U/EC800N |
| PWM.PWM1 | PWM1 | EC600S / EC600N / EC100Y/EC800N               |
| PWM.PWM2 | PWM2 | EC600S / EC600N / EC100Y/EC800N               |
| PWM.PWM3 | PWM3 | EC600S / EC600N / EC100Y/EC800N               |


#### 使用说明

1.  实例1
 

```
from usr.PWM import PWMclass as PWM

'''
* 参数1(int)：PWM号
        注：EC100YCN平台，支持PWM0 ~ PWM3，对应引脚如下：
        PWM0 – 引脚号19
        PWM1 – 引脚号18
        PWM2 – 引脚号23
        PWM3 – 引脚号22

        注：EC600SCN平台，支持PWM0 ~ PWM3，对应引脚如下：
        PWM0 – 引脚号52
        PWM1 – 引脚号53
        PWM2 – 引脚号70
        PWM3 – 引脚号69
* 参数2(int)：ABOVE_xx
        EC600SCN/EC600N/EC800N平台:
        ABOVE_MS ms级取值范围：(0,1023]
        ABOVE_1US us级取值范围：(0,157]
        ABOVE_10US us级取值范围：(1,1575]
        ABOVE_BELOW_US ns级 取值(0,1024]

        EC200U/EC600U平台:
        ABOVE_MS ms级取值范围：(0,10]
        ABOVE_1US us级取值范围：(0,10000]
        ABOVE_10US us级取值范围：(1,10000]
        ABOVE_BELOW_US ns级 取值[100,65535]
* 参数3(int)：high_time
        高电平时间，单位ms
* 参数4(int)：cycle_time
        pwm整个周期时间，单位ms
'''

pwm = PWM(PWM.PWM1, PWM.ABOVE_MS, 100, 200)
pwm.open() # 开启PWM输出
pwm.close() # 关闭PWM输出
```
