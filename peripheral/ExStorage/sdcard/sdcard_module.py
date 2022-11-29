'''
@Author: Stephen.Gao
@Date: 2022-04-2
@Description: sdcard class

Copyright 2022 - 2022 quectel
'''
import uos

class Sdcard(object):
    '''
    目前仅EC600N/EC800N平台支持
    '''
    def __init__(self,spi_port=1,spimode=0,spiclk=4,spics=35):
        self._sdcard = uos.VfsFat(spi_port, spimode, spiclk, spics)
        uos.mount(self._sdcard,'/sd')

    def listdir(self,path=""):
        print(uos.listdir('/sd/'+path.lstrip('/')))

    def mkdir(self,path):
        uos.mkdir('/sd/'+path.lstrip('/'))

    def remove(self,path):
        uos.remove('/sd/'+path.lstrip('/'))

    def rmdir(self,path):
        uos.rmdir('/sd/'+path.lstrip('/'))

    def stat(self):
        return uos.stat('/sd')

    def statvfs(self):
        return uos.statvfs('/sd')

    def touch(self,file_path):
        f = open("/sd/"+file_path.lstrip('/'),'w+')
        f.close()

if __name__=="__main__":
    sd = Sdcard()
    print("sdcard init success. ")
    sd.listdir()
    sd.mkdir("new")
    sd.listdir()
    sd.touch("new_file")
    sd.listdir()
    sd.remove("new_file")
    sd.rmdir("new")
    sd.listdir()
    sd.stat()
    sd.statvfs()




