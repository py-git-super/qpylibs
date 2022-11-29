import camera
from usr.common_except import CustomError,error_put

class CommonCamera(object):
    '''
    camera通用类
    提供接口：prev_open(), scan_open, cap_open, prev_close(), scan_close(), cap_close(),
    scan_start(), scan_stop(), scan_pause(), scan_resume(), start(name,wide,height)
    '''
    def __init__(self,model,pre_level=2,decode_level=1,scan_callback=None,capt_callback=None,lcd_w=240,lcd_h=240):
        '''
        :param model: camera型号
        :param pre_level: 预览等级[1,2]。等级越高，图像越流畅,消耗资源越大,默认2
        :param decode_level: 解码等级[1,2]，等级越高，识别效果越好但资源消耗越大,默认1
        :param scan_callback: 扫码回调函数
        :param capt_callback: 拍照回调函数
        :param lcd_w: lcd屏幕宽度
        :param lcd_h: lcd屏幕高度
        '''
        self._model = model
        self._pre_level = pre_level
        self._decode_level = decode_level
        self._lcd_w = lcd_w
        self._lcd_h = lcd_h

        # 0: gc032a spi
        if self._model == 0:
            self._cam_w = 640
            self._cam_h = 480
        # 1: bf3901 spi
        elif self._model == 1:
            self._cam_w = 320
            self._cam_h = 240
        else:
            raise CustomError("This type of camera is not supported")

        self._preview = camera.camPreview(self._model, self._cam_w, self._cam_h, self._lcd_w, self._lcd_h,
                                          self._pre_level)
        self._scan = camera.camScandecode(self._model, self._decode_level, self._cam_w, self._cam_h, self._pre_level,
                                          self._lcd_w, self._lcd_h)
        self._cap = camera.camCapture(self._model, self._cam_w, self._cam_h, self._pre_level,self._lcd_w, self._lcd_h)

        #scan callback
        if scan_callback is None:
            self._scan_callback = self._scan_callback_l
        else:
            self._scan_callback = scan_callback
        self._scan.callback(self._scan_callback)

        # capture callback
        if capt_callback is None:
            self._capt_callback = self._capt_callback_l
        else:
            self._capt_callback = None

        self._cap.callback(self._capt_callback)

    def prev_open(self):
        '''
        开启预览功能,使用该方法前，需要初始化LCD。
        '''
        ret = self._preview.open()
        error_put(ret, "preview function failed to open")

    def scan_open(self):
        '''
        开启扫码功能,使用该方法前，需要初始化LCD。
        '''
        ret = self._scan.open()
        error_put(ret, "Code scanning function failed to open")

    def cap_open(self):
        '''
        开启相机功能,使用该方法前，需要初始化LCD。
        '''
        ret = self._cap.open()
        error_put(ret, "Code scanning function failed to open")

    def prev_close(self):
        '''
        关闭相机功能
        '''
        ret = self._preview.close()
        error_put(ret, "preview function failed to close")

    def scan_close(self):
        '''
        关闭相机功能
        '''
        ret = self._scan.close()
        error_put(ret, "Code scanning function failed to close")

    def cap_close(self):
        '''
        关闭相机功能
        '''
        ret = self._cap.close()
        error_put(ret, "capture function failed to close")

    def scan_start(self):
        '''
        开始扫码
        '''
        ret = self._scan.start()
        error_put(ret, "Code scanning function failed to open")

    def scan_stop(self):
        '''
        停止扫码
        '''
        ret = self._scan.stop()
        error_put(ret, "Code scanning function failed to close")

    def scan_pause(self):
        '''
        暂停扫码
        '''
        ret = self._scan.pause()
        error_put(ret, "Code scanning function pause failed")

    def scan_resume(self):
        '''
        继续扫描
        '''
        ret = self._scan.resume()
        error_put(ret, "Code scanning function recovery failed")

    def start(self, name=None,img_w=None, img_h=None):
        '''
        :param name: 保存为图片名
        :param img_w: 图片水平分辨率
        :param img_h: 图片竖直分辨率
        '''
        if name is None:
            error_put(-1, "Please confirm the picture file name")
        if img_w is None:
            img_w = self._cam_w
        if img_h is None:
            img_h = self._cam_h
        ret = self._cap.start(img_w, img_h, name)
        error_put(ret, "Failed to take photos")

    def _scan_callback_l(self,para):
        print("scan success:",para)

    def _capt_callback_l(self,para):
        print("capture success:",para)





