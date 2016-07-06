import ntplib
from time import ctime
from base import tools
import datetime
import time

NTP_LIST=[
          's2c.time.edu.cn',
          's2m.time.edu.cn',
           'pool.ntp.org',
           'cn.ntp.org.cn',
           'us.ntp.org.cn',
           'sgp.ntp.org.cn',
           'kr.ntp.org.cn',
           'jp.ntp.org.cn'
          ]

def get_net_time():
    ntp_client = ntplib.NTPClient()
    for NTP in NTP_LIST:
        response=None
        try:
            response = ntp_client.request(NTP,timeout=0.5)
        except:
            print("None Responce")
        if response:
            return response.tx_time
    tools.messege_exit("please connect to Internet")

if __name__ == '__main__':
    stop_time="2016-09-1"
    stop_time= datetime.datetime.strptime(stop_time,"%Y-%m-%d")
    stop_time = time.mktime(stop_time.timetuple())
    print(stop_time)