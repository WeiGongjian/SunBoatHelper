from state import state
from manage import supply
from base import button,tools
import time
import threading
import configparser
import random
import os,sys

project_name="KancolleHelper"
path=os.path.abspath(sys.argv[0])
path=path[:path.index(project_name)+len(project_name)]
conf = configparser.ConfigParser() 
conf.read("%s/cfg/expedition.properties" % path)

class expedition_manager:
    def __init__(self,sleep_time=None):
        self.expedition_map={2:expedition(2),3:expedition(3),4:expedition(4)}
        self.sleep_time=sleep_time
    
    def add_expedition_task(self,task_map,random_interval_list,remain_list):
        for key in task_map.keys():
            assert key in [2,3,4]
            assert task_map.get(key) in range(40)
            self.expedition_map.get(key).expedition_id=task_map.get(key)
            self.expedition_map.get(key).page=int(task_map.get(key)/8)+1
            self.expedition_map.get(key).num=task_map.get(key)%8
            self.expedition_map.get(key).state="wait"
            self.expedition_map.get(key).random_interval=random_interval_list[key-2]
            self.expedition_map.get(key).remain=remain_list[key-2]
    
    def start(self):
        while True:
            wait_kan_num_list=[]
            back_kan_num_list=[]
            now = time.strftime("%H:%M",time.localtime(time.time()))
            if self.sleep_time and self.cmp_time(now,self.sleep_time[0]) and not self.cmp_time(now,self.sleep_time[1]):
                tools.time_print("[%s]during sleep time %s-%s , script will not work" % (now,self.sleep_time[0],self.sleep_time[1]))
                time.sleep(5)
                continue
            for key in self.expedition_map.keys():
                remain = self.expedition_map.get(key).remain
                if remain:
                    expedition_time_counter(self.expedition_map.get(key),remain=remain).start()
                    self.expedition_map.get(key).remain=0
                state = self.expedition_map.get(key).state
                if state == "wait":
                    wait_kan_num_list.append(key)
                elif state == "back":
                    back_kan_num_list.append(key)
            if wait_kan_num_list:
                expedition_list=wait_kan_num_list+back_kan_num_list
                tools.time_print("now start to expediton: %s" % expedition_list)
                self.expedition_run_list(expedition_list)
            time.sleep(5)    
                
    def expedition_run_list(self,kan_num_list):
        self.ensure_back()
        supply.supply(kan_num_list)
        state.wait_for_state("home")
        button.get_button("home_attact").click()
        state.wait_for_state("attack")
        button.get_button("home_choose_expedition").click()
        state.wait_for_state("expedition_not")
        for kan_num in kan_num_list:
            state.wait_for_state("expedition_not","expedition_ing")
            expedition=self.expedition_map.get(kan_num)
            if expedition.page != 1:
                button.get_button("expedition_page%s" % str(expedition.page)).click()
                time.sleep(0.5)
            button.get_button("expedition_num%s" % str(expedition.num)).click()   
            while state.get_state() not in ["expedition_ing","expedition_decide"]:
                time.sleep(0.5)
                if expedition.page != 1:
                    button.get_button("expedition_page%s" % str(expedition.page)).click()
                    time.sleep(0.5)
                button.get_button("expedition_num%s" % str(expedition.num)).click()   
            if state.get_state()=="expedition_ing":
                expedition=self.expedition_map.get(kan_num)
                expedition.state="expedition"
                expedition_time_counter(expedition).start()
            elif state.get_state()=="expedition_decide":
                button.get_button("expedition_decide").click()
                time.sleep(0.5+random.random()*0.5)
                button.get_button("expedition_kan%s" % str(kan_num)).click()
                retry = 0
                while state.get_state() != "expedition_begin":
                    retry=retry+1
                    button.get_button("expedition_kan%s" % str(kan_num)).click()
                    time.sleep(0.5)
                    if retry==10:
                        break
                button.get_button("expedition_begin").click()
                time.sleep(5.5)
                expedition=self.expedition_map.get(kan_num)
                expedition.state="running"
                expedition_time_counter(expedition).start()
                time.sleep(1)
                state.wait_for_wait_over()
        button.get_button("home").click()
        
    def ensure_back(self):
        state.wait_for_state("home","home_expedition_back")
        if state.get_state() == "home":
            button.get_button("home_supply").click()
            state.wait_for_state("supply")
            button.get_button("home").click()
            state.wait_for_state("home","home_expedition_back")
            if state.get_state() == "home_expedition_back":
                self.ensure_back()
        else:
            while True:
                button.get_button("all_screen").click()
                state_now = state.get_state()
                if state_now != "home" and state_now !="home_expedition_back":
                    button.get_button("all_screen").click()
                    time.sleep(2)
                else:
                    break
            if state.get_state() == "home_expedition_back":
                self.ensure_back()
    
    def cmp_time(self,src,dst):
        src=int(src.replace(":",""))
        dst=int(dst.replace(":",""))
        return src > dst and True or False

class expedition:
    def __init__(self,kan_id):
        self.kan_id=kan_id
        self.supply=False
        self.state="stop"
        self.remain=0
        self.random_interval=0
    
    def run(self):
        None
        
class expedition_time_counter(threading.Thread):
    def __init__(self, expedition, remain=0):
        threading.Thread.__init__(self)
        self.expedition = expedition
        self.remain=remain*60
        self.random_interval=expedition.random_interval*60
        self.expedition_interval=int(conf.get("expedition", "kan%s" % self.expedition.expedition_id))*60
       # base.time_print(self.expedition_interval)
        
    def run(self):
        self.expedition.state="expedition"
        sleep_time= self.remain or self.expedition_interval
        for i in range(0, sleep_time, 10):
            tools.time_print("kan%s will be back after %s second" % (self.expedition.kan_id,(sleep_time-i)))
            time.sleep(10)
        
        self.expedition.state="back"
        tools.time_print("kan%s state change to : %s" % (self.expedition.kan_id,self.expedition.state))
        tools.time_print("kan%s is back" % self.expedition.kan_id)
        if self.random_interval:
            random_interval=int(random.random()*self.random_interval)
            tools.time_print("now wait random interval %s second" % random_interval)
            time.sleep(random_interval)
        if self.expedition.state == "back":
            self.expedition.state="wait"
            tools.time_print("kan%s state change to : %s" % (self.expedition.kan_id,self.expedition.state))
        
        
if __name__ == "__main__":
    
    expedition_manager=expedition_manager(sleep_time=None)
    expedition_manager.add_expedition_task({2:2, 3:6,4:38},[0,0,0],[0,0,0])
    expedition_manager.start()
#     expedition=expedition(2)
#     expedition.expedition_id=38
#     expedition.page=5
#     expedition.num=6
#     expedition.state="back"  
#     expedition_time_counter(expedition).start()  
#     while True:
#         base.time_print(expedition.state)
#         time.sleep(2)