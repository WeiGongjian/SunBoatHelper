import configparser
from base import win

conf = configparser.ConfigParser() 
conf.read("../cfg/state.properties")
sections = conf.sections()

def generate_config_color(section):
    global sections
    print(sections)
    if section not in sections:
        exit(-1)
    points=conf.get(section,"point")
    point_list=points.split(":")
    color_list=[]
    for point in point_list:
        separator_index=point.find(",")
        x=int(point[1:separator_index])
        y=int(point[separator_index+1:len(point)-1])
        color_list.append(str(win.get_color(int(x),int(y))))
    colors=",".join(color_list)
    conf.set(section,"color",colors)
    conf.write(open("../cfg/state.properties", "w"))
 
if __name__ == "__main__":
    generate_config_color("expedition_begin")
    
