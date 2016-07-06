import configparser
import time
import os,sys
from base import tools,win
from pip._vendor.requests.sessions import session

project_name="KancolleHelper"
path=os.path.abspath(sys.argv[0])
path=path[:path.index(project_name)+len(project_name)]
conf = configparser.ConfigParser() 
conf.read("%s/cfg/state.properties" % path)
sections = conf.sections()

def get_state():
    for section in sections:
        if judge_is_state(section):
            return section
    return None

def judge_is_state(section,precision=4):
    point_list_int=[]
    color_list_int=[]
    points=conf.get(section,"point")
    colors=conf.get(section,"color")
    for point in points.split(":"):
        separator_index=point.find(",")
        x=int(point[1:separator_index])
        y=int(point[separator_index+1:len(point)-1])
        point_list_int.append((int(x),int(y)))
    for color in colors.split(","):
        color_list_int.append(int(color))
    assert len(point_list_int) == 6
    assert len(color_list_int) == 6
    right = 0
    for index in range(6):
        index_color=-1
        try:
            index_color=win.get_color(point_list_int[index][0], point_list_int[index][1])
        except:
            time.sleep(1)
            tools.time_print("could not get color , retry after 1 second")
            index_color=win.get_color(point_list_int[index][0], point_list_int[index][1])    
        if index_color == color_list_int[index]:
            right+=1
    if right>=precision:
        return session
    return None 

def wait_for_wait_over():
    while True:
        if get_state() == "wait":
            time.sleep(0.5)
    
    
def wait_for_state(*args):
    while True:
        for section in sections:
            for section in args:
                if (get_state() == section):
                    time.sleep(0.5)
                    return
        time.sleep(1)
        tools.time_print("waiting for state %s" % str(args))
                
if __name__ == "__main__":
     tools.time_print(get_state())
     #base.time_print(wait_for_not_wait())
     #base.time_print(wait_for_state("attack","home"))