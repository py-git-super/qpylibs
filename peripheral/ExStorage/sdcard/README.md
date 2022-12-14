### sdcard

**类引用：**

```python
from usr.sdcard_module import Sdcard
```

 

**实例化参数：**

| 名称     | 必填 | 类型 | 说明                                                         |
| -------- | ---- | ---- | ------------------------------------------------------------ |
| spi_port | 否   | int  | 通道选择[0,1]，默认1                                         |
| spimode  | 否   | int  | SPI 的工作模式(模式0最常用)，默认0                           |
| spiclk   | 否   | int  | 时钟频率 0 : 812.5kHz 1 :  1.625MHz 2 : 3.25MHz 3 : 6.5MHz 4 : 13MHz，默认4 |
| spics    | 否   | int  | CS片选，GPIOn，默认35（600N通道1 ）                          |

```
sd = Sdcard()
```

**接口函数：**

l **listdir(path)**

​	列出‘/sd’目录文件，否则列出‘/sd’下给定目录的文件。path为可选参数，表示目录名，默认为空。

参数：

| 名称 | 必填 | 类型 | 说明                     |
| ---- | ---- | ---- | ------------------------ |
| path | 否   | str  | sd卡目录下目录，默认为空 |

返回值：

| 名称           | 类型 | 说明                           |
| -------------- | ---- | ------------------------------ |
| 文件（夹）列表 | list | 所选目录下所有文件及文件夹列表 |

l **mkdir(path)**

​	创建目录，默认在’/sd/’下，若嵌套目录请确定路径合法。

参数：

| 名称 | 必填 | 类型 | 说明           |
| ---- | ---- | ---- | -------------- |
| path | 是   | str  | 创建的目录路径 |

l **remove(path)**

​	删除文件，文件路径为相对’/sd/’，请确定文件路径合法。

参数：

| 名称 | 必填 | 类型 | 说明           |
| ---- | ---- | ---- | -------------- |
| path | 是   | str  | 删除的文件路径 |

l **rmdir(path)**

​	删除文件夹，文件夹路径为相对’/sd/’，请确定文件路径合法。

参数：

| 名称 | 必填 | 类型 | 说明             |
| ---- | ---- | ---- | ---------------- |
| path | 是   | str  | 删除的文件夹路径 |

 

l **touch(file_path)**

​	创建文件，文件夹路径为相对’/sd/’，请确定文件路径合法。

 

参数：

| 名称      | 必填 | 类型 | 说明         |
| --------- | ---- | ---- | ------------ |
| file_path | 是   | str  | 创建的文件名 |

l **stat()**

​	获取sdcard根目录下文件或目录的状态。

返回值：

| 名称  | 类型 | 说明                                                         |
| ----- | ---- | ------------------------------------------------------------ |
| mode  | int  | inode保护模式                                                |
| ino   | int  | inode节点号                                                  |
| dev   | int  | inode驻留的设备                                              |
| nlink | int  | inode的链接数                                                |
| uid   | int  | 所有者的用户id                                               |
| gid   | int  | 所有者的组id                                                 |
| size  | int  | 文件大小，单位字节                                           |
| atime | int  | 上次访问的时间                                               |
| mtime | int  | 最后一次修改的时间                                           |
| ctime | int  | 操作系统报告的“ctime”，在某些系统上是最新的元数据更改的时间，在其它系统上是创建时间，详细信息参见平台文档 |

l **statvfs()**

​	获取sdcard文件系统状态信息。

返回值：

| 名称      | 类型 | 说明                     |
| --------- | ---- | ------------------------ |
| f_bsize   | int  | 文件系统块大小，单位字节 |
| f_frsize  | int  | 分栈大小，单位字节       |
| f_blocks  | int  | 文件系统数据块总数       |
| f_bfree   | int  | 可用块数                 |
| f_bavai   | int  | 非超级用户可获取的块数   |
| f_files   | int  | 文件结点总数             |
| f_ffree   | int  | 可用文件结点数           |
| f_favail  | int  | 超级用户的可用文件结点数 |
| f_flag    | int  | 挂载标记                 |
| f_namemax | int  | 最大文件长度，单位字节   |