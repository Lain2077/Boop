import pymem
import time
import win32api
from win32gui import GetWindowText, GetForegroundWindow
import contextlib
from os import getenv

#Dump every now and then with hazedumper when updates knock
dwForceJump = 86756744
dwLocalPlayer = 14596508
m_fFlags = 260

#logging.getLogger("pymem").disabled = True #Just to hide pymem logs. Import logging for this

class colors:
    """
    Colors for printing
    """
    PINK = "\033[35m"
    BOLD = "\033[1m"
    def __init__(self) -> None:
        if getenv("NO_COLOR"):
            self.HEADER = ""
            self.OKBLUE = ""
            self.OKCYAN = ""
            self.OKGREEN = ""
            self.WARNING = ""
            self.FAIL = ""
            self.ENDC = ""
            self.BOLD = ""

bcolors = colors()

def main():
    print(bcolors.PINK + bcolors.BOLD +
    '''
.----.  .----.  .----. .----. 
| {}  }/  {}  \/  {}  \| {}  }
| {}  }\      /\      /| .--' 
`----'  `----'  `----' `-'    
By Mina
    ''')
    with contextlib.redirect_stdout(None):
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        running = True
 
    while running:      
        if GetWindowText(GetForegroundWindow()) != "Counter-Strike: Global Offensive - Direct3D 9": #Might have to change to your window's name
            continue    

        if win32api.GetAsyncKeyState(ord(' ')): 
            force_jump = client + dwForceJump
            player = pm.read_int(client + dwLocalPlayer)
            if player:
                on_ground = pm.read_int(player + m_fFlags)
                if on_ground and on_ground == 257:
                    pm.write_int(force_jump, 5)
                    time.sleep(0.08)
                    pm.write_int(force_jump, 4)
                    #print("hop!")       
        #Panic close
        if win32api.GetAsyncKeyState(ord('à')):
            running = False
        time.sleep(0.002)

if __name__ == '__main__':
    main()
