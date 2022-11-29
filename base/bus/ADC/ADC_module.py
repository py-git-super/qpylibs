from misc import ADC
import utime
read_time = 5
adc = ADC() 
while read_time:  
    adc.open()  # ADC 功能初始化
    read_data0 = adc.read(ADC.ADC0)  # 读取ADC0电压
    print(read_data0)
    read_data1 = adc.read(ADC.ADC1)  # 读取ADC0电压
    print(read_data1)
    adc.close()  # 关闭ADC
    read_time -= 1  
    utime.sleep(1)  # 延时1S

