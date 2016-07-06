# coding=utf-8
import configparser
import os,sys
from manage import expedition
from time import ctime
from base import net_time,tools
import datetime
import time
import traceback


conf = configparser.ConfigParser() 
conf.read("config.properties")
sections = conf.sections()

if __name__=="__main__":
    #software info
    softwire_info='\
===============================================================\n\
本脚本由Thus@baidu.com友情制作，禁止用于商业用途；\n\
娇喘判定脚本的机制未知，尽管本脚本按键位置和时长都随机，但不保证一定不会被ban；\n\
由使用本脚本所产生的各种问题，责任由使用者承担；\n\
配置远征请修改配置文件config.properties \n\
新版本发布、舰c交流群: 464544739 \n\
==============================================================='
    try:
        print(softwire_info)
        # time check
        stop_time="2019-05-1"
        stop_time= datetime.datetime.strptime(stop_time,"%Y-%m-%d")
        stop_time = time.mktime(stop_time.timetuple())
        net_time_now=net_time.get_net_time()
        if stop_time < net_time_now:
            tools.messege_exit("overdue,please download new version")
        # sleep time
        sleep_time=conf.get("script", "sleep.time")
        if sleep_time!="None":
            tools.time_print("sleep time is %s" % sleep_time)
            sleep_time=sleep_time.split("-")
            sleep_time=(sleep_time[0],sleep_time[1]) 
        else:
            sleep_time=None
        # expedition
        expedition_manager=expedition.expedition_manager(sleep_time=sleep_time)
        expedition_map_list={}
        random_interval_list=[]
        remain_list=[]
        if conf.get("expedition", "kan2.state") == "run":
            kan_num=2
            expedition_id=conf.getint("expedition", "kan2.id")
            remain=conf.getint("expedition", "kan2.remain")
            random_interval=conf.getint("expedition", "kan2.random_interval")
            remain_list.append(remain)
            random_interval_list.append(random_interval)
            expedition_map_list[kan_num]=expedition_id
        else:
            remain_list.append(0)
            random_interval_list.append(0)
        if conf.get("expedition", "kan3.state") == "run":
            kan_num=3
            expedition_id=conf.getint("expedition", "kan3.id")
            remain=conf.getint("expedition", "kan3.remain")
            random_interval=conf.getint("expedition", "kan3.random_interval")
            remain_list.append(remain)
            random_interval_list.append(random_interval)
            expedition_map_list[kan_num]=expedition_id
        else:
            remain_list.append(0)
            random_interval_list.append(0)
        if conf.get("expedition", "kan4.state") == "run":
            kan_num=4
            expedition_id=conf.getint("expedition", "kan4.id")
            remain=conf.getint("expedition", "kan4.remain")
            random_interval=conf.getint("expedition", "kan4.random_interval")
            remain_list.append(remain)
            random_interval_list.append(random_interval)
            expedition_map_list[kan_num]=expedition_id
        else:
            remain_list.append(0)
            random_interval_list.append(0)
        tools.time_print("expedition_map_list: %s" % expedition_map_list)
        expedition_manager.add_expedition_task(expedition_map_list,random_interval_list,remain_list)
        expedition_manager.start()
    except:
        tools.time_print(sys.exc_info())
        tools.time_print(traceback.format_exc())
        while True:
            time.sleep(3600)
    
    
    
        
        
