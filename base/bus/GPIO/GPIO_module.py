from machine import Pin


gpio = Pin(GPIO.GPIO1, GPIO.OUT, GPIO.PULL_DISABLE, 0)
gpio.write(1)
gpio.read()
