from machine import ExtInt
import utime

def fun1(args):  
    print(args)  
    print("key1 extint")   
def fun2(args):  
    print(args)  
    print("key2 extint")   
def fun3(args):  
    print(args)  
    print("key3 extint")  
# PULL_DISABLE – 浮空模式
# PULL_PU – 上拉模式
# PULL_PD – 下拉模式
extint1 = ExtInt(ExtInt.GPIO12, ExtInt.IRQ_FALLING, ExtInt.PULL_DISABLE, fun1) 
extint2 = ExtInt(ExtInt.GPIO12, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, fun2) 
extint2 = ExtInt(ExtInt.GPIO12, ExtInt.IRQ_FALLING, ExtInt.PULL_PD, fun3) 
extint1.enable()
extint2.enable()
extint3.enable()   # 使能中断
while True:  
    utime.sleep_ms(200)