from ctypes import *
from ctypes.wintypes import *
import psutil
import json
import datetime
import struct



# first get pid, see the 32-bit solution


'''
mem_info
pmem(rss=189407232, 
     vms=222834688, 
     num_page_faults=1957011, 
     peak_wset=229617664, 
     wset=189407232, 
     peak_paged_pool=625096, 
     paged_pool=553800, 
     peak_nonpaged_pool=38248, 
     nonpaged_pool=37296, 
     pagefile=222834688, 
     peak_pagefile=233480192, 
     private=222834688)

mem_info_ex
pmem(rss=143306752, 
     vms=223154176, 
     num_page_faults=1961048, 
     peak_wset=229617664, 
     wset=143306752, 
     peak_paged_pool=625096, 
     paged_pool=554056, 
     peak_nonpaged_pool=38248, 
     nonpaged_pool=37296, 
     pagefile=223154176, 
     peak_pagefile=233480192, 
     private=223154176)


'''

'''
game
  sha256:   34937741e0dbae5e3fa7fa92ecf8159b5b3fc9aba047a5dd8ae3c8cb1bcce345
  label:    SMI_Practice_Hack
  name:     SMI_Practice_Hack
  title:    Super Metroid
  region:   NTSC
  revision: 1.0
  board:    LOROM-RAM
    memory
      type: ROM
      size: 0X400000
      content: Program
    memory
      type: RAM
      size: 0X8000
      content: Save

board: LOROM-RAM
  memory
    type:ROM
    content:Program
    map
      address:00-7d,80-ff:8000-ffff
      mask:0X8000
  memory
    type:RAM
    content:Save
    map
      address:70-7d,f0-ff:0000-7fff
      mask:0X8000
'''
rooms = {None: None,
        "0X91F8" : "landingSite",
        "0X93AA" : "crateriaPowerBombRoom",
        "0X93FE" : "westOcean",
        "0X94CC" : "elevatorToMaridia",
        "0X95FF" : "crateriaMoat",
        "0X962A" : "elevatorToCaterpillar",
        "0X965B" : "gauntletETankRoom",
        "0X96BA" : "climb",
        "0X975C" : "pitRoom",
        "0X97B5" : "elevatorToMorphBall",
        "0X9804" : "bombTorizo",
        "0X990D" : "terminator",
        "0X9938" : "elevatorToGreenBrinstar",
        "0X99BD" : "greenPirateShaft",
        "0X99F9" : "crateriaSupersRoom",
        "0X9A90" : "theFinalMissile",
        "0X9AD9" : "greenBrinstarMainShaft",
        "0X9B5B" : "sporeSpawnSuper",
        "0X9BC8" : "earlySupers",
        "0X9C07" : "brinstarReserveRoom",
        "0X9D19" : "bigPink",
        "0X9D9C" : "sporeSpawnKeyhunter",
        "0X9DC7" : "sporeSpawn",
        "0X9E11" : "pinkBrinstarPowerBombRoom",
        "0X9E52" : "greenHills",
        "0X9E9F" : "morphBall",
        "0X9F64" : "blueBrinstarETankRoom",
        "0XA011" : "etacoonETankRoom",
        "0XA051" : "etacoonSuperRoom",
        "0XA0D2" : "waterway",
        "0XA107" : "alphaMissileRoom",
        "0XA15B" : "hopperETankRoom",
        "0XA1D8" : "billyMays",
        "0XA253" : "redTower",
        "0XA2CE" : "xRay",
        "0XA322" : "caterpillar",
        "0XA37C" : "betaPowerBombRoom",
        "0XA3AE" : "alphaPowerBombsRoom",
        "0XA3DD" : "bat",
        "0XA447" : "spazer",
        "0XA4B1" : "warehouseETankRoom",
        "0XA471" : "warehouseZeela",
        "0XA4DA" : "warehouseKiHunters",
        "0XA56B" : "kraidEyeDoor",
        "0XA59F" : "kraid",
        "0XA5ED" : "statuesHallway",
        "0XA66A" : "statues",
        "0XA6A1" : "warehouseEntrance",
        "0XA6E2" : "varia",
        "0XA788" : "cathedral",
        "0XA7DE" : "businessCenter",
        "0XA890" : "iceBeam",
        "0XA8F8" : "crumbleShaft",
        "0XA923" : "crocomireSpeedway",
        "0XA98D" : "crocomire",
        "0XA9E5" : "hiJump",
        "0XAA0E" : "crocomireEscape",
        "0XAA41" : "hiJumpShaft",
        "0XAADE" : "postCrocomirePowerBombRoom",
        "0XAB3B" : "cosineRoom",
        "0XAB8F" : "preGrapple",
        "0XAC2B" : "grapple",
        "0XAC5A" : "norfairReserveRoom",
        "0XAC83" : "greenBubblesRoom",
        "0XACB3" : "bubbleMountain",
        "0XACF0" : "speedBoostHall",
        "0XAD1B" : "speedBooster",
        "0XAD5E" : "singleChamber", # Exit room from Lower Norfair, also on the path to Wave
        "0XADAD" : "doubleChamber",
        "0XADDE" : "waveBeam",
        "0XAE32" : "volcano",
        "0XAE74" : "kronicBoost",
        "0XAEB4" : "magdolliteTunnel",
        "0XAF3F" : "lowerNorfairElevator",
        "0XAFA3" : "risingTide",
        "0XAFFB" : "spikyAcidSnakes",
        "0XB1E5" : "acidStatue",
        "0XB236" : "mainHall", # First room in Lower Norfair
        "0XB283" : "goldenTorizo",
        "0XB32E" : "ridley",
        "0XB37A" : "lowerNorfairFarming",
        "0XB40A" : "mickeyMouse",
        "0XB457" : "pillars",
        "0XB4AD" : "writg",
        "0XB4E5" : "amphitheatre",
        "0XB510" : "lowerNorfairSpringMaze",
        "0XB55A" : "lowerNorfairEscapePowerBombRoom",
        "0XB585" : "redKiShaft",
        "0XB5D5" : "wasteland",
        "0XB62B" : "metalPirates",
        "0XB656" : "threeMusketeers",
        "0XB698" : "ridleyETankRoom",
        "0XB6C1" : "screwAttack",
        "0XB6EE" : "lowerNorfairFireflea",
        "0XC98E" : "bowling",
        "0XCA08" : "wreckedShipEntrance",
        "0XCA52" : "attic",
        "0XCAAE" : "atticWorkerRobotRoom",
        "0XCAF6" : "wreckedShipMainShaft",
        "0XCC27" : "wreckedShipETankRoom",
        "0XCC6F" : "basement", # Basement of Wrecked Ship
        "0XCD13" : "phantoon",
        "0XCDA8" : "wreckedShipLeftSuperRoom",
        "0XCDF1" : "wreckedShipRightSuperRoom",
        "0XCE40" : "gravity",
        "0XCEFB" : "glassTunnel",
        "0XCFC9" : "mainStreet",
        "0XD055" : "mamaTurtle",
        "0XD13B" : "wateringHole",
        "0XD1DD" : "beach",
        "0XD2AA" : "plasmaBeam",
        "0XD30B" : "maridiaElevator",
        "0XD340" : "plasmaSpark",
        "0XD408" : "toiletBowl",
        "0XD48E" : "oasis",
        "0XD4EF" : "leftSandPit",
        "0XD51E" : "rightSandPit",
        "0XD5A7" : "aqueduct",
        "0XD5EC" : "butterflyRoom",
        "0XD617" : "botwoonHallway",
        "0XD6D0" : "springBall",
        "0XD78F" : "precious",
        "0XD7E4" : "botwoonETankRoom",
        "0XD95E" : "botwoon",
        "0XD9AA" : "spaceJump",
        "0XD9FE" : "westCactusAlley",
        "0XDA60" : "draygon",
        "0XDAAE" : "tourianElevator",
        "0XDAE1" : "metroidOne",
        "0XDB31" : "metroidTwo",
        "0XDB7D" : "metroidThree",
        "0XDBCD" : "metroidFour",
        "0XDC65" : "dustTorizo",
        "0XDC19" : "tourianHopper",
        "0XDDC4" : "tourianEyeDoor",
        "0XDCB1" : "bigBoy",
        "0XDD58" : "motherBrain",
        "0XDDF3" : "rinkaShaft",
        "0XDEDE": "tourianEscape4",
        "0XDF45" : "ceresElevator",
        "0XE06B" : "flatRoom", # Placeholder name for the flat room in Ceres Station
        "0XE0B5" : "ceresRidley" }
        
for proc in psutil.process_iter():
    if "bsnes" in proc.name():
        PROCESS_ID = proc.pid


PROCESS_HEADER_ADDR = 0XB16D7C  #0XB15D7C

STRLEN = 2

PROCESS_VM_READ = 0X0010 #0X079B


# Some/most of the below will/should be removed, but I don't feel like cleaning up at the moment.
k32 = WinDLL('kernel32')
k32.OpenProcess.argtypes = DWORD,BOOL,DWORD
k32.OpenProcess.restype = HANDLE
k32.ReadProcessMemory.argtypes = HANDLE, LPVOID, LPVOID, c_size_t, POINTER(c_size_t)
k32.ReadProcessMemory.restype = BOOL

process = k32.OpenProcess(PROCESS_VM_READ, 0, PROCESS_ID)
buf = create_string_buffer(STRLEN)
s = c_size_t()
#while True:
tmp_1 = ""
if k32.ReadProcessMemory(process,PROCESS_HEADER_ADDR + 0X079B, buf, STRLEN, byref(s)):
    #print(s.value, buf.raw)
    tmp_1 = buf.raw

def __alloc_mem( num_bytes):
        if num_bytes == 1:
            return c_ubyte()
        elif num_bytes == 2:
            return c_ushort()
        elif num_bytes == 4:
            return c_ulong()
        elif num_bytes == 8:
            return c_ulonglong()

def read_room_name(length_of_data):
    room_id = None
    out_val = __alloc_mem(length_of_data)
    bytesRead = c_ulonglong()
    
    r = windll.kernel32.ReadProcessMemory(process, PROCESS_HEADER_ADDR + 0X079B, byref(out_val), sizeof(out_val), byref(bytesRead))
    room_id = str(hex(out_val.value)).upper()
    room = rooms.get(room_id, "Room Not Found")
    if room is None:
        print (room_id, "Not Found")
    return room

def read_enemy_hp(length_of_data):
    out_val = __alloc_mem(length_of_data)
    bytesRead = c_ulonglong()
    r = windll.kernel32.ReadProcessMemory(process, PROCESS_HEADER_ADDR + 0X0f8c, byref(out_val), sizeof(out_val), byref(bytesRead))
    room_id = out_val.value
    return room_id


def read_samus_hp(length_of_data):
    out_val = __alloc_mem(length_of_data)
    bytesRead = c_ulonglong()
    
    r = windll.kernel32.ReadProcessMemory(process, PROCESS_HEADER_ADDR + 0x09C2, byref(out_val), sizeof(out_val), byref(bytesRead))
    room_id = out_val.value
    return room_id
   
def read_samus_missiles(length_of_data):
    out_val = __alloc_mem(length_of_data)
    bytesRead = c_ulonglong()
    
    r = windll.kernel32.ReadProcessMemory(process, PROCESS_HEADER_ADDR + 0x09C6, byref(out_val), sizeof(out_val), byref(bytesRead))
    room_id = out_val.value
    return room_id
    
last_room = 0
last_hp = 0
samus_hp = 0
change = False
last_missiles = 0
while True:
    current_room = read_room_name(2)
    if last_room != current_room:
       print (current_room)
       last_room = current_room
       change = True
    current_hp = read_enemy_hp(2)
    if last_hp != current_hp:
        print (current_hp)
        last_hp = current_hp
        change = True
    current_samus_hp = read_samus_hp(1)
    if samus_hp != current_samus_hp:
        print (current_samus_hp)
        samus_hp = current_samus_hp
        change = True
    current_missiles = read_samus_missiles(2)
    if last_missiles != current_missiles:
        print (current_missiles)
        last_missiles = current_missiles
        change = True
    if change:
        # write to disk
        f = open("activity_tracker.txt", 'a')
        f.write(json.dumps({"room" : current_room,"missiles" : current_missiles, "bosshp" : current_hp, "samushp" : current_samus_hp, "date" : str(datetime.datetime.now())}) + "\n")
        f.close()
        change = False


# Check for room id

# Enemy HP offset: offset + 0X0F8C
# Room ID: offset + 0X079B
# I want to do something like the below
#if room["kraid"] == RoomID or room["phantoon"] == RoomID or
#   room["ridley"] == RoomID or room["draygon"] == RoomID or 
#   room["crocomire"] == RoomID or room["sporespawn"] == RoomID or
#   room["Golden Torizo"] == RoomID or room["botwoon"] == RoomID: # Makesure we are in a boss fight
#    append_to_file.write(json.dumps({"datetime" : datetime, "boss" : room_lookup[RoomID], "hp" : hp}))
