import random
import math
import time
import os,sys
from base import win
from base import tools
from state import state
import configparser

project_name="KancolleHelper"
path=os.path.abspath(sys.argv[0])
path=path[:path.index(project_name)+len(project_name)]
conf = configparser.ConfigParser() 
conf.read("%s/cfg/buttons.properties" % path)
#conf.read("../base/buttons.cfg")
sections = conf.sections()

class button:
    def __init__(self,type,center,attr):
        assert type in ["square","circle"]
        self.type = type
        self.center=center
        if type == "square":
            self.length=attr[0]
            self.hight=attr[1]
        if type == "circle":
            self.radius=attr
        
    def click(self):
        if(self.type == "circle"):
            x_range=self.radius
            x = self.center[0] + x_range - int(random.random()*x_range*2)
            y_range=int(math.sqrt(self.radius*self.radius - (self.center[0] - x)*(self.center[0] - x)))
            y = self.center[1] + y_range - int(random.random()*y_range*2)
        if(self.type == "square"):
            x_range=int(self.length/2)
            x = self.center[0] + x_range - int(random.random()*x_range*2)
            y_range=int(self.hight/2)
            y = self.center[1] + y_range - int(random.random()*y_range*2)
        win.click(x, y)

def get_button(button_name):
    assert button_name in sections
    type=conf.get(button_name,"type")
    assert type in ["square","circle"]
    if type == "circle":
        center=conf.get(button_name,"center").split(",")
        center=(int(center[0]),int(center[1]))
        radius=conf.get(button_name,"radius")
        return button("circle",center,int(radius))
    if type == "square":
        center=conf.get(button_name,"center").split(",")
        center=(int(center[0]),int(center[1]))
        length=conf.getint(button_name,"length")
        hight=conf.getint(button_name,"hight")
        return button("square",center,(length,hight))
            
if __name__ == "__main__":
    get_button("expedition_kan3").click()
    #get_button("home_attact").click()
    #get_button("expedition_kan3").click()
    #button.get_button("expedition_begin").click()
    #button.get_button("home").click()
    