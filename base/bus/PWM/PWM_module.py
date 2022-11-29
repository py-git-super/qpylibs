from misc import PWM
pwm = PWM(PWM.PWM1, PWM.ABOVE_MS, 100, 200)
pwm.open()  # 开启PWM输出
pwm.close() # 关闭PWM输出