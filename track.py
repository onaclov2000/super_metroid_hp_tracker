from ctypes import *
from ctypes.wintypes import *
import psutil
import json
import datetime
import struct
# Lots of help from: 
# https://jathys.zophar.net/supermetroid/kejardon/RAMMap.txt
# https://raw.githubusercontent.com/UNHchabo/AutoSplitters/master/SuperMetroid/LiveSplit.SuperMetroid.asl
# https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-readprocessmemory
# https://docs.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights (PROCESS_VM_READ (0x0010)	Required to read memory in a process using ReadProcessMemory.)
# https://wiki.supermetroid.run/index.php?title=List_of_rooms_by_SMILE_ID
# https://github.com/Stashiocat/stashiobot/blob/master/utils/supermetroid.py

SAMUS_HP = 0x09C2 # Samus's HP, useful for comparing samus HP vs enemy HP over a gameplay.
ENEMY_HP =  0X0f8c # Where to find the enemy HP (This doesn't support MB and whatnot, so I'll want to improve that at some point.)
ROOMID = 0X079B # Location of Room identifiers
MISSILES = 0x09C6
SUPER_MISSILES = 0x09CA
POWER_BOMBS = 0x09CE

rooms = {"0X91F8" : "landingSite",
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
        "0XE0B5" : "ceresRidley",
        "0X9FBA" : "noobbridge" }

# Find the process we care about.        
for proc in psutil.process_iter():
    if "bsnes" in proc.name(): # This really only works if there is a single instance of bsnes, now we *could* set it up so it creates a whole thing for each one it finds, and then we print out which one was which (by pid)
        PROCESS_ID = proc.pid
# Setup the base address we care about
PROCESS_HEADER_ADDR = 0XB16D7C # Wanna use a different emulator? Pick out the second of the tuple found in the .asl link above (if you search for bsnes you should see it)
# This value is so we can read the memory
PROCESS_VM_READ = 0X0010 

# Found this on stack overflow, so yea, I'm not 100% sure what is what, and what is necessary
k32 = WinDLL('kernel32')
k32.OpenProcess.argtypes = DWORD,BOOL,DWORD
k32.OpenProcess.restype = HANDLE
k32.ReadProcessMemory.argtypes = HANDLE, LPVOID, LPVOID, c_size_t, POINTER(c_size_t)
k32.ReadProcessMemory.restype = BOOL
# We need to open the process, so we pick the permissions, and the pid. (I don't recall what the middle parameter is)
process = k32.OpenProcess(PROCESS_VM_READ, 0, PROCESS_ID)

# Depending on how many bytes need to be read, we pick the appropriate datatype.
def __alloc_mem( num_bytes):
        if num_bytes == 1:
            return c_ubyte()
        elif num_bytes == 2:
            return c_ushort()
        elif num_bytes == 4:
            return c_ulong()
        elif num_bytes == 8:
            return c_ulonglong()

def read_memory(offset, length_of_data):
    out_val = __alloc_mem(length_of_data)
    bytesRead = __alloc_mem(8) # No idea why it's c_ulonglong() here vs the earlier is a variable amount, but oh well.
    
    r = windll.kernel32.ReadProcessMemory(process, PROCESS_HEADER_ADDR + offset, byref(out_val), sizeof(out_val), byref(bytesRead))
    return out_val.value

def read_enemy_hp(room):
    # Do some checking which room we are in, if we are in certain rooms we will care about mother brain segments, etc
    out_val = read_memory(ENEMY_HP, 2)
    pass

def read_room_name():
    out_val = read_memory(ROOMID, 2)
    room_id = str(hex(out_val)).upper()
    room = rooms.get(room_id, "Room Not Found: " + room_id)
    # The below is for tracking purposes.
    #if room == "Room Not Found":
    #    print (room_id, "Not Found")
    return room


last_room = 0
last_hp = 0
samus_hp = 0
change = False
last_missiles = 0
last_super_missiles = 0
last_pb = 0
while True:
    current_room = read_room_name()
    if last_room != current_room:
       print ("Room: ",current_room)
       last_room = current_room
       change = True
    current_hp = read_memory(ENEMY_HP, 2)
    if last_hp != current_hp:
        print ("Enemy HP", current_hp)
        last_hp = current_hp
        change = True
    current_samus_hp = read_memory(SAMUS_HP, 1)
    if samus_hp != current_samus_hp:
        print ("Samus HP", current_samus_hp)
        samus_hp = current_samus_hp
        change = True
    current_missiles = read_memory(MISSILES ,2)
    if last_missiles != current_missiles:
        print ("Missile Count: ", current_missiles)
        last_missiles = current_missiles
        change = True

    current_super_missiles = read_memory(SUPER_MISSILES,2)
    if last_super_missiles != current_super_missiles:
        print ("Super Missile Count: ", current_super_missiles)
        last_super_missiles = current_super_missiles
        change = True

    current_pb = read_memory(POWER_BOMBS,2)
    if last_pb != current_pb:
        print ("PB Count: ", current_pb)
        last_pb = current_pb
        change = True

    if change:
        # write to disk
        f = open("activity_tracker.txt", 'a')
        f.write(json.dumps({"room" : current_room,"missiles" : current_missiles, "bosshp" : current_hp, "samushp" : current_samus_hp, "powerbombs" : current_pb,"supermissiles" : current_super_missiles, "date" : str(datetime.datetime.now())}) + "\n")
        f.close()
        change = False
