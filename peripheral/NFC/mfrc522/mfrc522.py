from machine import Pin
from machine import SPI
import utime
from machine import ExtInt
import _thread

MAX_LEN = 16

PCD_IDLE = 0x00         #取消当前命令
PCD_AUTHENT = 0x0E      #验证密钥
PCD_RECEIVE = 0x08      #接收数据
PCD_TRANSMIT = 0x04     #发送消息
PCD_TRANSCEIVE = 0x0C   #发送并接收数据
PCD_RESETPHASE = 0x0F   #复位
PCD_CALCCRC = 0x03      #CRC计算

#Mifare_One卡片命令字
PICC_REQIDL = 0x26      #寻天线区内未进入休眠状态的卡
PICC_REQALL = 0x52      #寻天线区内全部卡
PICC_ANTICOLL = 0x93    #防冲撞
PICC_SElECTTAG = 0x93   #寻卡
PICC_AUTHENT1A = 0x60   #验证A密钥
PICC_AUTHENT1B = 0x61   #验证B密钥
PICC_READ = 0x30        #读块
PICC_WRITE = 0xA0       #写块
PICC_DECREMENT = 0xC0   #扣款
PICC_INCREMENT = 0xC1   #充值
PICC_RESTORE = 0xC2     #调块数据到缓冲区
PICC_TRANSFER = 0xB0    #保存缓冲区数据
PICC_HALT = 0x50        #休眠

MI_OK = 0
MI_NOTAGERR = 1
MI_ERR = 2

#寄存器
Reserved00 = 0x00
CommandReg = 0x01
CommIEnReg = 0x02
DivlEnReg = 0x03
CommIrqReg = 0x04
DivIrqReg = 0x05
ErrorReg = 0x06
Status1Reg = 0x07
Status2Reg = 0x08
FIFODataReg = 0x09
FIFOLevelReg = 0x0A
WaterLevelReg = 0x0B
ControlReg = 0x0C
BitFramingReg = 0x0D
CollReg = 0x0E
Reserved01 = 0x0F

Reserved10 = 0x10
ModeReg = 0x11
TxModeReg = 0x12
RxModeReg = 0x13
TxControlReg = 0x14
TxAutoReg = 0x15
TxSelReg = 0x16
RxSelReg = 0x17
RxThresholdReg = 0x18
DemodReg = 0x19
Reserved11 = 0x1A
Reserved12 = 0x1B
MifareReg = 0x1C
Reserved13 = 0x1D
Reserved14 = 0x1E
SerialSpeedReg = 0x1F

Reserved20 = 0x20
CRCResultRegM = 0x21
CRCResultRegL = 0x22
Reserved21 = 0x23
ModWidthReg = 0x24
Reserved22 = 0x25
RFCfgReg = 0x26
GsNReg = 0x27
CWGsPReg = 0x28
ModGsPReg = 0x29
TModeReg = 0x2A
TPrescalerReg = 0x2B
TReloadRegH = 0x2C
TReloadRegL = 0x2D
TCounterValueRegH = 0x2E
TCounterValueRegL = 0x2F

Reserved30 = 0x30
TestSel1Reg = 0x31
TestSel2Reg = 0x32
TestPinEnReg = 0x33
TestPinValueReg = 0x34
TestBusReg = 0x35
AutoTestReg = 0x36
VersionReg = 0x37
AnalogTestReg = 0x38
TestDAC1Reg = 0x39
TestDAC2Reg = 0x3A
TestADCReg = 0x3B
Reserved31 = 0x3C
Reserved32 = 0x3D
Reserved33 = 0x3E
Reserved34 = 0x3F

class MFRC522(object):
    '''
    RC522类
    开放接口：write(text)，read()，read_id(),MFRC522_Read(blockAddr),MFRC522_Write(blockAddr, writeData)
    '''


    serNum = []
    KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    BLOCK_ADDRS = [8, 9, 10]

    def __init__(self):

        self.MFRC522_Init()


    def _MFRC522_Reset(self):
        self._Write_MFRC522(CommandReg, PCD_RESETPHASE)

    def _Write_MFRC522(self, addr, val):
        # print("this bug write")
        raise NotImplementedError

    def _Read_MFRC522(self, addr):
        # print("this bug read")
        raise NotImplementedError

    def _Close_MFRC522(self):
        raise NotImplementedError

    def _SetBitMask(self, reg, mask):
        tmp = self._Read_MFRC522(reg)
        self._Write_MFRC522(reg, tmp | mask)

    def _ClearBitMask(self, reg, mask):
        '''
        寄存器清位
        '''
        tmp = self._Read_MFRC522(reg)
        self._Write_MFRC522(reg, tmp & (~mask))

    def AntennaOn(self):
        '''
        开启天线
        '''
        temp = self._Read_MFRC522(TxControlReg)
        if (~(temp & 0x03)):
            self._SetBitMask(TxControlReg, 0x03)

    def AntennaOff(self):
        '''
        关闭天线
        '''
        self._ClearBitMask(TxControlReg, 0x03)

    def _MFRC522_ToCard(self, command, sendData):
        '''
        通过RC522和ISO14443卡通讯
        @param command: RC522命令字
        @param sendData: 通过RC522发送到卡片的数据
        '''
        backData = []
        backLen = 0
        status = MI_ERR
        irqEn = 0x00
        waitIRq = 0x00
        if command == PCD_AUTHENT:  #验证密钥
            irqEn = 0x12
            waitIRq = 0x10
        if command == PCD_TRANSCEIVE:   #发送并接收数据
            irqEn = 0x77
            waitIRq = 0x30

        self._Write_MFRC522(CommIEnReg, irqEn | 0x80)   #中断请求传递的使能和禁能控制位
        self._ClearBitMask(CommIrqReg, 0x80)
        self._SetBitMask(FIFOLevelReg, 0x80)

        self._Write_MFRC522(CommandReg, PCD_IDLE)       #取消当前命令

        for i in range(len(sendData)):
            self._Write_MFRC522(FIFODataReg, sendData[i])

        self._Write_MFRC522(CommandReg, command)    #发送并接收数据

        if command == PCD_TRANSCEIVE:
            self._SetBitMask(BitFramingReg, 0x80)

        i = 2000
        while True:
            n = self._Read_MFRC522(CommIrqReg)
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & waitIRq)):
                break

        self._ClearBitMask(BitFramingReg, 0x80)

        if i != 0:
            if (self._Read_MFRC522(ErrorReg) & 0x1B) == 0x00:
                status = MI_OK
                if n & irqEn & 0x01:
                    status = MI_NOTAGERR
                if command == PCD_TRANSCEIVE:
                    n = self._Read_MFRC522(FIFOLevelReg)
                    lastBits = self._Read_MFRC522(ControlReg) & 0x07
                    if lastBits != 0:
                        backLen = (n - 1) * 8 + lastBits
                    else:
                        backLen = n * 8

                    if n == 0:
                        n = 1
                    if n > MAX_LEN:
                        n = MAX_LEN

                    for i in range(n):
                        backData.append(self._Read_MFRC522(FIFODataReg))
            else:
                status = MI_ERR

        return (status, backData, backLen)

    def MFRC522_Request(self, reqMode):
        '''
        寻卡
        '''
        TagType = []

        self._Write_MFRC522(BitFramingReg, 0x07)

        TagType.append(reqMode)
        (status, backData, backBits) = self._MFRC522_ToCard(
            PCD_TRANSCEIVE, TagType)        #模块和卡之间发送并接收数据

        if ((status != MI_OK) | (backBits != 0x10)):
            status = MI_ERR

        return (status, backBits)

    def MFRC522_Anticoll(self):
        '''
        防冲撞
        '''
        serNumCheck = 0

        serNum = []

        self._Write_MFRC522(BitFramingReg, 0x00)

        serNum.append(PICC_ANTICOLL)
        serNum.append(0x20)

        (status, backData, backBits) = self._MFRC522_ToCard(
            PCD_TRANSCEIVE, serNum)

        if (status == MI_OK):
            i = 0
            if len(backData) == 5:
                for i in range(4):
                    serNumCheck = serNumCheck ^ backData[i]
                if serNumCheck != backData[4]:
                    status = MI_ERR
            else:
                status = MI_ERR

        return (status, backData)

    def _CalulateCRC(self, pIndata):
        '''
        用MF522计算CRC16函数
        '''
        self._ClearBitMask(DivIrqReg, 0x04)
        self._SetBitMask(FIFOLevelReg, 0x80)

        for i in range(len(pIndata)):
            self._Write_MFRC522(FIFODataReg, pIndata[i])

        self._Write_MFRC522(CommandReg,PCD_CALCCRC)
        i = 0xFF
        while True:
            n = self._Read_MFRC522(DivIrqReg)
            i -= 1
            if not ((i != 0) and not (n & 0x04)):
                break
        pOutData = []
        pOutData.append(self._Read_MFRC522(CRCResultRegL))
        pOutData.append(self._Read_MFRC522(CRCResultRegM))
        return pOutData

    def MFRC522_SelectTag(self, serNum):
        '''
        选择卡片
        @param serNum: 卡片序列号
        :return: 成功返回卡容量
        '''
        backData = []
        buf = []
        buf.append(PICC_SElECTTAG)
        buf.append(0x70)

        for i in range(5):
            buf.append(serNum[i])

        pOut = self._CalulateCRC(buf)
        buf.append(pOut[0])
        buf.append(pOut[1])
        (status, backData, backLen) = self._MFRC522_ToCard(
            PCD_TRANSCEIVE, buf)

        if (status == MI_OK) and (backLen == 0x18):
            # print("Size: " + str(backData[0]))
            return backData[0]
        else:
            return 0

    def MFRC522_Auth(self, authMode, BlockAddr, Sectorkey, serNum):
        '''
        验证卡片密码
        @param authMode: 验证密码模式：0x60验证a密码，0x61验证b密码
        @param BlockAddr: 块地址
        @param Sectorkey: 密码
        @param serNum: 卡片序列号
        :return: 验证结果
        '''
        buff = []

        # First byte should be the authMode (A or B)
        buff.append(authMode)

        # Second byte is the trailerBlock (usually 7)
        buff.append(BlockAddr)

        # Now we need to append the authKey which usually is 6 bytes of 0xFF
        for i in range(len(Sectorkey)):
            buff.append(Sectorkey[i])

        # Next we append the first 4 bytes of the UID
        for i in range(4):
            buff.append(serNum[i])
        # print(buff)
        # Now we start the authentication itself
        (status, backData, backLen) = self._MFRC522_ToCard(PCD_AUTHENT, buff)
        # print("auth state {}".format(status))
        # Check if an error occurred
        if not (status == MI_OK):
            print("AUTH ERROR!!")
        if not (self._Read_MFRC522(Status2Reg) & 0x08):
            print("AUTH ERROR(status2reg & 0x08) != 0")

        # Return the status
        return status

    def MFRC522_StopCrypto1(self):
        self._ClearBitMask(Status2Reg, 0x08)

    def MFRC522_Read(self, blockAddr):
        '''
        读数据
        @param blockAddr: 块地址
        :return: 读取的数据，16字节
        '''
        recvData = []
        recvData.append(PICC_READ)  #读块
        recvData.append(blockAddr)
        pOut = self._CalulateCRC(recvData)  #用MF522计算CRC16函数
        recvData.append(pOut[0])
        recvData.append(pOut[1])
        (status, backData, backLen) = self._MFRC522_ToCard(
            PCD_TRANSCEIVE, recvData)
        if not (status == MI_OK):
            print("Error while reading!")

        if len(backData) == 16:
            print("Sector " + str(blockAddr) + " " + str(backData))
            return backData
        else:
            return None

    def MFRC522_Write(self, blockAddr, writeData):
        '''
        写数据到卡
        @param blockAddr: 块地址
        @param writeData: 写入的数据，16字节
        '''
        buff = []
        buff.append(PICC_WRITE)
        buff.append(blockAddr)
        crc = self._CalulateCRC(buff)
        buff.append(crc[0])
        buff.append(crc[1])
        (status, backData, backLen) = self._MFRC522_ToCard(
            PCD_TRANSCEIVE, buff)
        # print("status is {},backdata is {},backlen is {}".format(status,backData,backLen))
        if not (status == MI_OK) or not (backLen == 4) or not ((backData[0] & 0x0F) == 0x0A):
            status = MI_ERR
        # print("write status {}".format(status))
        # print("%s backdata &0x0F == 0x0A %s" % (backLen, backData[0] & 0x0F))
        if status == MI_OK:
            buf = []
            for i in range(16):
                buf.append(writeData[i])

            crc = self._CalulateCRC(buf)
            buf.append(crc[0])
            buf.append(crc[1])
            (status, backData, backLen) = self._MFRC522_ToCard(
                PCD_TRANSCEIVE, buf)
            if not (status == MI_OK) or not (backLen == 4) or not ((backData[0] & 0x0F) == 0x0A):
                print("Error while writing")
            if status == MI_OK:
                print("Data written")

    def MFRC522_DumpClassic1K(self, key, uid):
        for i in range(64):
            status = self.MFRC522_Auth(PICC_AUTHENT1A, i, key, uid)
            # Check if authenticated
            if status == MI_OK:
                self.MFRC522_Read(i)
            else:
                # print("Authentication error")
                pass


    def MFRC522_Init(self):
        self._MFRC522_Reset()

        self._Write_MFRC522(TModeReg, 0x8D)
        self._Write_MFRC522(TPrescalerReg, 0x3E)
        self._Write_MFRC522(TReloadRegL, 30)
        self._Write_MFRC522(TReloadRegH, 0)

        self._Write_MFRC522(TxAutoReg, 0x40)
        self._Write_MFRC522(ModeReg, 0x3D)
        self.AntennaOff()
        self.AntennaOn()
        self.M500PcdConfigISOType('A')

    def M500PcdConfigISOType(self, type):

        if type == 'A':
            self._ClearBitMask(Status2Reg, 0x08)
            self._Write_MFRC522(ModeReg, 0x3D)
            self._Write_MFRC522(RxSelReg, 0x86)
            self._Write_MFRC522(RFCfgReg, 0x7F)
            self._Write_MFRC522(TReloadRegL, 30)
            self._Write_MFRC522(TReloadRegH, 0)
            self._Write_MFRC522(TModeReg, 0x8D)
            self._Write_MFRC522(TPrescalerReg, 0x3E)
            utime.sleep_us(1000)
            self.AntennaOn()
        else:
            return 1

    def read(self):
        id, text = self.read_no_block()
        while not id:
            id, text = self.read_no_block()
        return id, text

    def read_id(self):
        '''
        200ms一次循环读id，直到读取到
        '''
        id = self.read_id_no_block()
        while not id:
            id = self.read_id_no_block()
            utime.sleep_ms(200)
        return id

    def read_id_no_block(self):
        (status, TagType) = self.MFRC522_Request(PICC_REQIDL)  #寻天线区内未进入休眠状态的卡
        if status != MI_OK:
            return None
        (status, uid) = self.MFRC522_Anticoll()
        if status != MI_OK:
            return None
        # print("uid=", uid)
        return self.uid_to_num(uid)

    def read_no_block(self):
        (status, TagType) = self.MFRC522_Request(PICC_REQIDL)  #寻天线区内未进入休眠状态的卡
        if status != MI_OK:
            return None, None
        (status, uid) = self.MFRC522_Anticoll()
        if status != MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.MFRC522_SelectTag(uid)
        status = self.MFRC522_Auth(
            PICC_AUTHENT1A, 11, self.KEY, uid)
        data = []
        text_read = ''
        if status == MI_OK:
            for block_num in self.BLOCK_ADDRS:
                block = self.MFRC522_Read(block_num)
                if block:
                    data += block
            if data:
                text_read = ''.join(chr(i) for i in data)
        self.MFRC522_StopCrypto1()
        return id, text_read

    def write(self, text):
        id, text_in = self.write_no_block(text)
        while not id:
            id, text_in = self.write_no_block(text)
        return id, text_in

    def write_no_block(self, text):
        (status, TagType) = self.MFRC522_Request(PICC_REQIDL)  #寻天线区内未进入休眠状态的卡
        if status != MI_OK:
            # print("cannot find the card!")
            return None, None
        (status, uid) = self.MFRC522_Anticoll()
        if status != MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.MFRC522_SelectTag(uid)
        status = self.MFRC522_Auth(
            PICC_AUTHENT1A, 11, self.KEY, uid)
        self.MFRC522_Read(11)
        if status == MI_OK:
            data = bytearray()
            data.extend(bytearray(text.ljust(
                len(self.BLOCK_ADDRS) * 16).encode('ascii')))
            i = 0
            for block_num in self.BLOCK_ADDRS:
                self.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
                i += 1
        self.MFRC522_StopCrypto1()
        return id, text[0:(len(self.BLOCK_ADDRS) * 16)]

    def uid_to_num(self, uid):
        n = 0
        for i in range(0, 5):
            n = n * 256 + uid[i]
        return n

    def _irq_callback(self, para):
        # print("irq call:", para)
        self.read_id_no_block()

    def _irq_set(self, pin_irq, irq_cb):
        if pin_irq is None:
            # print("Interrupt pin is not set")
            return

        regVal = 0
        # self._Write_MFRC522(CommIEnReg, regVal)
        self._Write_MFRC522(CommIEnReg, regVal | 0x20)
        self._Write_MFRC522(DivlEnReg, 0x90)

        if irq_cb is None:
            self._irq_fun = self._irq_callback
        else:
            self._irq_fun = irq_cb

        self._irq = ExtInt(pin_irq, ExtInt.IRQ_FALLING,
                           ExtInt.PULL_PU, self._irq_fun)


class MFRC522_SPI(MFRC522):
    def __init__(self, spi=None, *, spi_no=1, spi_mode=0, spi_clk=0, pin_rst, pin_irq=None, irq_cb=None):
        if spi is None:
            self._spi = SPI(spi_no, spi_mode, spi_clk)
        else:
            self._spi = spi
        self._rst = Pin(pin_rst, Pin.OUT, Pin.PULL_DISABLE, 0)
        utime.sleep(1)
        self._rst.write(1)
        if pin_irq != None:
            self._irq_set(pin_irq, irq_cb)

        super().__init__()

    def _Write_MFRC522(self, addr, val):
        write_buf = bytearray([(addr << 1) & 0x7E, val])
        # print("write_buf:",write_buf)
        self._spi.write(write_buf, len(write_buf))

    def _Read_MFRC522(self, addr):
        write_buf = bytearray([((addr << 1) & 0x7E) | 0x80, 0])
        read_buf = bytearray(len(write_buf))
        self._spi.write_read(read_buf, write_buf, len(write_buf))
        # print("read_buf:",read_buf)
        return read_buf[1]

    def _Close_MFRC522(self):
        pass

def rc522_test():
    reader = MFRC522_SPI(pin_rst=Pin.GPIO12, pin_irq=Pin.GPIO11)
    print("init finish.")
    utime.sleep(1)
    w_data = bytearray([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
    while 1:
        utime.sleep_ms(200)
        status, data = reader.MFRC522_Request(0x26)  # 先寻卡
        if not status:
            print("寻卡完成")
            status, id = reader.MFRC522_Anticoll()  # 防冲撞
            if not status:
                print(id)
                if reader.MFRC522_SelectTag(id):  # 选卡
                    print("选卡完成")
                    status = reader.MFRC522_Auth(
                        PICC_AUTHENT1A, 7, reader.KEY, id)  # 认证
                    if status == 0:
                        print("认证完成")
                        reader.MFRC522_Write(8, w_data)  # 往块写数据
                        data = reader.MFRC522_Read(2)  # 读数据
                        print(data)
                        break

    '''
    while 1:
    utime.sleep_ms(200)
    status, data = reader.MFRC522_Request(0x26)  # 先寻卡
    if not status:
        print("寻卡完成")
        status, id = reader.MFRC522_Anticoll()  # 防冲撞
        if not status:
            print(id)
            if reader.MFRC522_SelectTag(id):  # 选卡
                print("选卡完成")
                status = reader.MFRC522_Auth(
                    PICC_AUTHENT1A, 7, reader.KEY, id)  # 认证
                if status == 0:
                    print("认证完成")
                    reader.MFRC522_Write(8, w_data)  # 往块写数据
                    data = reader.MFRC522_Read(2)  # 读数据
                    print(data)
                    break
    '''


    '''
    read,read_id demo:
    id = reader.read_id() #read id包含了寻卡防冲撞过程
    print('card id is {0}'.format(id))
    '''




if __name__ == '__main__':
    _thread.start_new_thread(rc522_test, ())
