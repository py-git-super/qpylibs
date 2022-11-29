import utime
from machine import I2C
from usr.common_except import CustomError

# I2C address of the device
DEFAULT_ADDRESS = 0x19

DEVICE_ID = 0xf9

# BMA250 Register Map
CHIP_ID_REG = 0x00  # Chip ID Register

X_AXIS_LSB_REG = 0x02  # X-Axis Data LSB
X_AXIS_MSB_REG = 0x03  # X-Axis Data MSB
Y_AXIS_LSB_REG = 0x04  # Y-Axis Data LSB
Y_AXIS_MSB_REG = 0x05  # Y-Axis Data MSB
Z_AXIS_LSB_REG = 0x06  # Z-Axis Data LSB
Z_AXIS_MSB_REG = 0x07  # Z-Axis Data MSB

TEMP_RD_REG = 0x08  # Temperature Data

STATUS1_REG = 0x09  # Interrupt Status Register
STATUS2_REG = 0x0A  # New Data Status Register
STATUS_TAP_SLOPE_REG = 0x0B  # Tap and Hold Interrupt Status Register 点击和hold
STATUS_ORIENT_HIGH_REG = 0x0C  # Flat and Orientation Status Register 平面和方位状态
RANGE_SEL_REG = 0x0F  # 范围选择寄存器
BW_SEL_REG = 0x10  # 带宽寄存器
MODE_CTRL_REG = 0x11  # Mode Control Register
DATA_CTRL_REG = 0x13  # Data Control Register
RESET_REG = 0x14  # Reset Register
INT_EN1_REG = 0x16  # 中断使能寄存器1
INT_EN2_REG = 0x17  # 中断使能寄存器2
LATCH_INT_REG = 0x21  # 锁存中断寄存器
HIGH_LOW_MODE_REG = 0x24    #异常重力中断模式寄存器
SLOPE_TH_REG = 0x28  # 倾斜阈值寄存器
RESET_CMD = 0xB6  # Reset Register

# BMA250范围选择寄存器配置
RANGE_SEL_2G = 0x03  # Range = +/-2G
RANGE_SEL_4G = 0x05  # Range = +/-4G
RANGE_SEL_8G = 0x08  # Range = +/-8G
RANGE_SEL_16G = 0x0C  # Range = +/-16G

# BMA250带宽寄存器配置
BW_SEL_7_81 = 0x08  # Bandwidth = 7.81Hz
BW_SEL_15_63 = 0x09  # Bandwidth = 15.63Hz
BW_SEL_31_25 = 0x0A  # Bandwidth = 31.25Hz
BW_SEL_62_5 = 0x0B  # Bandwidth = 62.5Hz
BW_SEL_125 = 0x0C  # Bandwidth = 125Hz
BW_SEL_250 = 0x0D  # Bandwidth = 250Hz
BW_SEL_500 = 0x0E  # Bandwidth = 500Hz
BW_SEL_1000 = 0x0F  # Bandwidth = 1000Hz

#中断使能配置
#int1配置
slope_en_x = 0x01
slope_en_y = 0x02
slope_en_z = 0x04
slope_en_xyx = 0x07
d_tap_en = 0x10
s_tap_en = 0x20
orient_en = 0x40
flat_en = 0x80
#int2配置
low_g_en = 0x04     #低重力，可用于ff中断
high_g_en_x = 0x01
high_g_en_y = 0x02
high_g_en_z = 0x04
high_g_en_xyx = 0x07

class Bma250(object):
    '''
    BMA250三轴加速度传感器类
    开放接口：set_range(range),set_hz(hz),read_accl(),int_enable(int_code),int_check()
    '''
    def __init__(self,i2c,dev_addr=0x19):
        self._i2c = i2c
        self._dev_addr = dev_addr
        self._read_data(RESET_REG,1)
        self.reset()
        id_read = self._read_data(CHIP_ID_REG,1)[0]
        if id_read != DEVICE_ID:
            raise CustomError("device id err")
        self._read_data(CHIP_ID_REG, 1)
        self.set_range()
        self.set_hz()
        self._int_latch() #初始化latch_level默认是50ms
        utime.sleep_ms(20)
        # print('init suceess! ')

    def reset(self):
        self._write_data(RESET_REG,RESET_CMD)

    def _read_data(self, regaddr, datalen):
        '''
        i2c读数据
        :param regaddr: 寄存器地址
        :param datalen: 读取的长度
        :return: 列表类型的data
        '''
        r_data = bytearray(datalen)
        reg_addres = bytearray([regaddr])
        self._i2c.read(self._dev_addr, reg_addres, 1, r_data, datalen, 1)
        ret_data = list(r_data)
        return ret_data

    def _write_data(self, regaddr, data):
        '''
        i2c写数据
        :param regaddr: 寄存器地址
        :param datalen: 写入的数据
        '''
        addr = bytearray([regaddr])
        w_data = bytearray([data])
        self._i2c.write(self._dev_addr, addr, len(addr), w_data, len(w_data))

    def set_range(self,range=RANGE_SEL_2G):
        '''
        配置传感器量程
        :param range: 加速度范围，默认2g
        '''
        if range in (RANGE_SEL_2G,RANGE_SEL_4G,RANGE_SEL_8G,RANGE_SEL_16G):
            if self._write_data(RANGE_SEL_REG,range):
                raise CustomError("range select failed.")
            # print("量程寄存器 {}".format(self._read_data(RANGE_SEL_REG, 1)[0]))
        else:
            raise CustomError("range select err")

    def set_hz(self,hz=BW_SEL_7_81):
        """
        配置传感器频率
        :param bwidth: 带宽，默认7.81Hz
        """
        if hz in (BW_SEL_7_81,BW_SEL_15_63,BW_SEL_31_25,BW_SEL_62_5,
                     BW_SEL_125,BW_SEL_250,BW_SEL_500,BW_SEL_1000):
            if self._write_data(BW_SEL_REG,hz):
                raise CustomError("bandwidth select failed.")
            # print("频率寄存器 {}".format(self._read_data(BW_SEL_REG,1)[0]))
        else:
            raise CustomError("bandwidth select err")

    def _int_latch(self,latch_level=0x0E):
        if self._write_data(LATCH_INT_REG, latch_level):
            raise CustomError("int latch set failed.")
        # print("锁存寄存器 {}".format(self._read_data(LATCH_INT_REG, 1)[0]))
        # print('latch set suceess! ')

    @property
    def _resolution(self):
        """
        获取加速度计的range.
        :return: range_2_G, range_4_G, range_8_G,, range_16_G.
        """
        return self._read_data(RANGE_SEL_REG,1)[0]

    def read_acceleration(self):
        """
        从X_AXIS_LSB_REG（0x02）读回数据，6字节
        X轴LSB，X轴MSB，Y轴LSB，Y轴MSB，Z轴LSB，Z轴MSB
        @return x,y,z轴加速度值的三元组，单位g
        """
        data = self._read_data(X_AXIS_LSB_REG,6)
        #print(data)
        accel_range = self._resolution
        # Convert the data to 10 bits
        if accel_range == 12:        #range_16_G
            # print("16G量程下")
            divider = 8
        elif accel_range == 8:      #range_8_G
            # print("8G量程下")
            divider = 16
        elif accel_range == 5:      #range_4_G
            # print("4G量程下")
            divider = 32
        elif accel_range == 3:      #range_2_G
            # print("2G量程下")
            divider = 64
        else:
            return (0,0,0)

        x = (data[1] * 256 + (data[0] & 0xC0)) / (divider * 256)
        y = (data[3] * 256 + (data[2] & 0xC0)) / (divider * 256)
        z = (data[5] * 256 + (data[4] & 0xC0)) / (divider * 256)

        if accel_range == 12:       #range_16_G
            x = x if x <= 16 else x - 32
            y = y if y <= 16 else y - 32
            z = z if z <= 16 else z - 32
        elif accel_range == 8:      #range_8_G
            x = x if x <= 8 else x - 16
            y = y if y <= 8 else y - 16
            z = z if z <= 8 else z - 16
        elif accel_range == 5:      #range_4_G
            x = x if x <= 4 else x - 8
            y = y if y <= 4 else y - 8
            z = z if z <= 4 else z - 8
        elif accel_range == 3:      #range_2_G
            x = x if x <= 2 else x - 4
            y = y if y <= 2 else y - 4
            z = z if z <= 2 else z - 4

        return (x, y, z)

    def int_enable(self,int_code,tap_thr=0x03, tap_dur=0x04,slop_thr=0x14,slop_dur=0x03,flat_hold_time=0x10):
        '''
        中断使能,单双击，倾斜，朝向，水平中断配置
        @param int_code:写入中断使能寄存器的值，要使能的中断种类
        @return:  -1:fail  0:success
        '''
        r_data = self._read_data(INT_EN1_REG, 1)[0]
        # print(r_data)
        w_data = r_data | int_code
        #单击中断
        if int_code == s_tap_en:
            #设置阈值和shock和quiet，敲击轴和锁存设置
            self._write_data(0x2B, tap_thr)  #默认阈值设置
            # self._int_latch(latch_level=0x02)       #锁存500ms
            # print('single_tap set suceess! ')
        #双击中断
        elif int_code == d_tap_en:
            # 设置阈值,dur,敲击轴,延迟和窗口
            self._write_data(0x2B, tap_thr)  #默认阈值设置
            self._write_data(0x2A, tap_dur)  # 默认dur设置
            # self._int_latch(latch_level=0x02)  # 锁存500ms
            # print('double_tap set suceess! ')
        #slope倾斜中断
        elif int_code in range(1,8):
            #设置阈值
            self._write_data(SLOPE_TH_REG, slop_thr)  # 默认阈值设置0x14
            self._write_data(0x27, slop_dur)  # 默认设置0x03
            # print('slop int set suceess! ')
        #orient朝向中断
        elif int_code == orient_en:
            #设置锁存中断模式
            self._int_latch(latch_level=0x0E)  # datasheet建议不锁存或锁存50ms
            # print('orient_int set suceess! ')
        #flat中断
        elif int_code == flat_en:
            self._write_data(0x2f, flat_hold_time)  # 默认保持时间设置0x10 ：512ms
            # print('inact_int set suceess! ')
        else:
            # print('int enable failed.check int_code.')
            return -1
        if self._write_data(INT_EN1_REG,w_data):
            raise CustomError("int enable failed.")
        # print("使能寄存器1: {}".format(self._read_data(INT_EN1_REG,1)[0]))
        return 0

    def int2_enable(self,int_code,low_mode=0x81,low_th=0x30,low_dur=0x09,high_th=0xc0,high_dur=0x0f):
        '''
        中断使能,高重力，低重力中断配置
        @param int_code:写入中断使能寄存器的值，要使能的中断种类
        @return:  -1:fail  0:success
        '''
        r_data = self._read_data(INT_EN2_REG, 1)[0]
        w_data = r_data | int_code
        #low_g中断 0x04
        if int_code == low_g_en:
            #设置低重力模式,阈值和dur
            self._write_data(0x24, low_mode)  # 默认设置
            self._write_data(0x22, low_dur) #默认0x09
            self._write_data(0x23, low_th)  #默认0x30
            # print('low_g中断 set suceess! ')
        #high_g中断 0x01-0x07
        elif int_code in range(1,8):
            # 设置阈值和dur
            self._write_data(0x25, high_dur)  #默认0x0f
            self._write_data(0x26, high_th)  #默认0xc0
            # print('high_g中断 set suceess! ')
        else:
            # print('int enable failed.check int_code.')
            return -1
        if self._write_data(INT_EN2_REG,w_data):
            raise CustomError("int enable failed.")
        # print("使能寄存器2 {}".format(self._read_data(INT_EN2_REG,1)[0]))
        return 0

    def process_single_tap(self):
        while 1:
            r_data = self._read_data(STATUS1_REG, 1)[0]
            if r_data & (1<<5):
                return 1
            utime.sleep_ms(5)

    def process_double_tap(self):
        while 1:
            r_data = self._read_data(STATUS1_REG, 1)[0]
            if r_data & (1<<4):
                return 1
            utime.sleep_ms(5)

    def process_slope(self):
        while 1:
            r_data = self._read_data(STATUS1_REG, 1)[0]
            if r_data & (1<<2):
                return 1
            utime.sleep_ms(20)

    def process_orient(self):
        while 1:
            r_data = self._read_data(STATUS1_REG, 1)[0]
            # print(r_data)
            if r_data & (1<<6):
                return 1
            utime.sleep_ms(20)

    def process_flat(self):
        while 1:
            r_data = self._read_data(STATUS1_REG, 1)[0]
            if r_data & (1<<7):
                return 1
            utime.sleep_ms(20)

    def process_low_g(self):
        while 1:
            r_data = self._read_data(STATUS1_REG, 1)[0]
            if r_data & 1:
                return 1
            utime.sleep_ms(20)

    def process_high_g(self):
        while 1:
            r_data = self._read_data(STATUS1_REG, 1)[0]
            if r_data & (1<<1):
                return 1
            utime.sleep_ms(20)


if __name__ == "__main__":
    i2c_dev = I2C(I2C.I2C1,I2C.STANDARD_MODE)
    bma250 = Bma250(i2c_dev)
    bma250.set_range(RANGE_SEL_2G)
    bma250.set_hz(BW_SEL_1000)
    bma250.int_enable(orient_en)
    for i in range(10):
        utime.sleep(1)
        bma250.process_orient()
        x, y, z = bma250.read_acceleration()
        print("Acceleration in X-Axis : {} g".format(x))
        print("Acceleration in Y-Axis : {} g".format(y))
        print("Acceleration in Z-Axis : {} g".format(z))
        print(" ************************************* ")


