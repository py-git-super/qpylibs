# ntp

#### 介绍
qpy平台ntp协议实现


#### 使用说明

1.  实例1
 

```
from usr.ntp import get_current_timestamp
current_timestamps = get_current_timestamp()#返回当前时间戳
```
2. 实例2

```
from usr.ntp import NTPClient
client = ntplib.NTPClient()
stats  = client.request()#request(host, version=2, port="ntp", timeout=5) host默认阿里云ntp服务器
print(stats.offset) #offset
print(stats.delay) #round-trip delay
print(stats.tx_time) #Transmit timestamp in system time.
print(stats.recv_time) #Receive timestamp in system time
print(stats.orig_time) #Originate timestamp in system time.
print(stats.dest_time) #Destination timestamp in system time.
print(stats.ref_time) #Reference timestamp in system time.



```




