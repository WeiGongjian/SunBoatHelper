import time

def messege_exit(msg):
    print(msg)
    while True:
        time.sleep(3600)
        
def time_print(msg):
    now = time.strftime("%H:%M:%S",time.localtime(time.time()))
    print("[%s] %s" % (now,msg))
    
    
if __name__ == "__main__":
    time_print("expedition_%s" % "kan3")