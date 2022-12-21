import os
import time
import pytesseract
import shutil
import phrases
from PIL import Image

baseaddr = "127.0.0.1"
port_min = 5555
port_max = 5560
sid = "127.0.0.1:5556"

speech_W = 360
speech_H = 335
speech_L = 720
speech_T = 315

nextcell_X = 1025
nextcell_Y = 1060
cell_X = 615
cell_Y = 1060
DELAY_NEXTCELL = 1000 / 1000
FAIL_THRESHOLD = 5
INTERROGATION_MIN = 10
INTERROGATION_MAX = 17

speech_vcdelta = 100
start_failed = False
reh_W = 516
reh_H = 80
reh_L = 294
reh_T = 1798

int_W = 407
int_H = 78
int_L = 341
int_T = 1317

pacify_X = 180
pacify_Y = 1513

communicate_X = 445
communicate_Y = 1593

punish_X = 706
punish_Y = 1612

intimidate_X = 908
intimidate_Y = 1511

skip_X = 996
skip_Y = 56

congrats_X = 545
congrats_Y = 685

refresh_X = 545
refresh_Y = 1550

refresh_conf_X = 735
refresh_conf_Y = 1184

recruit_X = 555
recruit_Y = 1611

M_DELAY = 5000
FAST_DELAY = 100

rehab_curr = -1
rehab_max = ""
inter_curr = -1
inter_max = -1

DELAY_SAVEFILE = 500 / 1000
DELAY_ACTION = 2000 / 1000
DELAY_PRESKIP = 1000 / 1000
DELAY_SKIP = 1000 / 1000
DELAY_REFRESH = 500 / 1000
DELAY_CONGRATS = 1500 / 1000
DELAY_RECRUIT = 1500 / 1000
DELAY_MID = 100 / 1000




def call(cmd):
    return os.popen('cmd /c "{command}"'.format(command=cmd)).read()
    

def connect_http():
    global sid
    for port in range(port_min, port_max):
        sid = "{}:{}".format(baseaddr, port)
        res = call("adb connect {sid}".format(sid=sid))
        if res.startswith("connected") or res.startswith("already"):
            print("Connected to [{}]".format(sid))
            return
    print("Could not find a local instance to connect to.")

def back():
    call("adb -s {sid} shell input keyevent 4".format(sid=sid))

def tap(x,y):
    call("adb -s {sid} shell input tap {x} {y}".format(sid=sid,x=x,y=y))

def next_prisoner():
    tap(nextcell_X, nextcell_Y)
    time.sleep(DELAY_NEXTCELL)
    tap(cell_X, cell_Y)
    time.sleep(DELAY_NEXTCELL)

def pacify():
    tap(pacify_X, pacify_Y)

def communicate():
    tap(communicate_X, communicate_Y)

def punish():
    tap(punish_X, punish_Y)

def intimidate():
    tap(intimidate_X, intimidate_Y)

def swipe(x1,y1,x2,y2,delay=M_DELAY):
    call("adb -s {sid} shell input swipe {x1} {y1} {x2} {y2} {delay}".format(sid=sid, x1=x1, x2=x2, y1=y1, y2=y2, delay=delay))

def capture_screen(name):
    call("adb -s {sid} exec-out screencap -p > {name}".format(sid=sid, name=name))

def crop(file_in, file_out, w, h, l, t):
    call("gm convert {f_in} -crop {w}x{h}+{l}+{t} {f_out}".format(f_in = file_in, f_out=file_out, w=w, h=h, l=l, t=t))

def crop_speech(file_in, file_out):
    crop(file_in, file_out, speech_W, speech_H, speech_L, speech_T)    

def crop_speech_more(file_in, file_out):
    crop(file_in, file_out, speech_W, speech_H-2*speech_vcdelta, speech_L, speech_T+speech_vcdelta)    

def crop_reh(file_in, file_out):
    crop(file_in, file_out, reh_W, reh_H, reh_L, reh_T)

def crop_inter(file_in, file_out):
    crop(file_in, file_out, int_W, int_H, int_L, int_T)

def moveR(delay=M_DELAY):
    swipe(MR_X1, MR_Y, MR_X2, MR_Y, delay)

def moveD(delay=M_DELAY):
    swipe(MU_X, MU_Y1, MU_X, MU_Y2, delay)

def moveL(delay=M_DELAY):
    swipe(MR_X2, MR_Y, MR_X1, MR_Y, delay)

def merge(dir, file_out):        
    call("gm montage -geometry {gw}x{gh} -borderwidth 0 -tile {gx}x{gy} ./{dir}/*.png -quality 90 {f_out}".format(gw=C_W, gh=C_H, gx=GRID_X, gy=GRID_Y, dir=dir, f_out = file_out))

def mono(file_in, file_out):
    call("gm convert -monochrome {f_in} {f_out}".format(f_in=file_in, f_out=file_out))

def negate(file_in, file_out, mono=True):
    if (mono):
        call("gm convert -monochrome -negate {f_in} {f_out}".format(f_in=file_in, f_out=file_out))
    else: 
        call("gm convert -negate {f_in} {f_out}".format(f_in=file_in, f_out=file_out))


def get_inter(fn):
    global inter_curr, inter_max
    fn_inter = "./inter/inter.png"
    fn_interneg = "./inter/interneg.png"
    print("Editing...",end='')
    crop_inter(fn, fn_inter)
    negate(fn_inter, fn_interneg, False)
    print("done.")
    print("OCR...",end="")
    inter = pytesseract.image_to_string(Image.open(fn_interneg))
    print("done.")
    inter_sp = inter.split('/')
    try:
        if len(inter_sp) > 1:
            inter_max = int(phrases.do(inter_sp[1]))
            if (inter_max > INTERROGATION_MAX or inter_max < INTERROGATION_MIN):
                print("Interrogations out of range: "+inter)
                return False
            left = inter_sp[0].split(':')
            if len(left) > 1:            
                inter_curr = int(phrases.do(left[1]))
                if (inter_curr > INTERROGATION_MAX):
                    print("Interrogations out of range: "+inter)
                    return False
            else:
                print("Could not parse interrogations: "+inter)
                return False
                #raise "Could not parse interrogations: "+inter
        else:
            print("Could not parse interrogations: "+inter)
            return False
            #raise "Could not parse interrogations: "+inter
    except:
        return False
    return True

def get_rehab(fn):
    global rehab_curr, rehab_max
    fn_reh = "./inter/rehab.png"
    fn_rehneg = "./inter/rehabneg.png"
    print("Editing...",end='')
    crop_reh(fn, fn_reh)
    negate(fn_reh, fn_rehneg)
    print("done.")
    print("OCR...",end="")
    reh = pytesseract.image_to_string(Image.open(fn_rehneg))
    print("done.")
    reh_sp = reh.split('/')
    if len(reh_sp) > 1:
        rehab_max = int(phrases.do(reh_sp[1]))
        left = reh_sp[0].split(':')
        if len(left)>1:
            rehab_curr = int(phrases.do(left[1]))            
        else:
            print("Could not parse rehabilitation: "+reh)
            return False
            #raise "Could not parse rehabilitation: "+reh
    else:
        print("Could not parse rehabilitation: "+reh)
        return False
        #raise "Could not parse rehabilitation: "+reh
    return True

def print_state():
    global inter_curr, inter_max, rehab_curr, rehab_max
    print("Interrogations: {curr}/{max}".format(curr=inter_curr,max=inter_max))
    print("Rehabilitation: {curr}/{max}".format(curr=rehab_curr,max=rehab_max))


def do_action(speech):
    match = phrases.action(speech)
    print("Appropriate action: "+match)
    acted = True
    print("Acting...",end="")
    if match == "pacify":
        pacify()
    elif match =="communicate":
        communicate()
    elif match == "punish":
        punish()
    elif match == "intimidate":
        intimidate()
    else:
        print("\nUnknown action. Cannot do. Retrying.")
        acted = False
    if acted:
        print("done.")
    
    return acted

def act(first_time):
    global rehab_max, rehab_curr, inter_curr, inter_max, start_failed
    ts = time.time()
    shutil.rmtree("./inter/")
    os.mkdir("./inter/")

    fn = "./inter/{}.png".format(ts)
    fn_inter = "./inter/{}_inter.png".format(ts)
    fn_reh = "./inter/{}_reh.png".format(ts)
    fn_interneg = "./inter/{}_interneg.png".format(ts)
    fn_rehneg = "./inter/{}_rehneg.png".format(ts)
    fn_speech = "./inter/{}_speech.png".format(ts)
    fn_speechmono = "./inter/{}_speechmono.png".format(ts)
    print("Capturing screen...", end='')
    capture_screen(fn)
    print("done.")
    print("Waiting for FS...", end='')
    time.sleep(DELAY_SAVEFILE)
    print("done.")
    if first_time:
        fail_count = 0
        print("[Reading interrogation status]")
        while not get_inter(fn) and fail_count < FAIL_THRESHOLD:
            fail_count += 1
            capture_screen(fn)
            time.sleep(DELAY_SAVEFILE)
            print("Retrying...")
        if (fail_count >= FAIL_THRESHOLD):
            start_failed = True
            print("Failed to start.")
            return True
        print("[Reading rehabilitation status]")
        while not get_rehab(fn):
            capture_screen(fn)
            time.sleep(DELAY_SAVEFILE)
            print("Retrying...")

    print_state()

    print("[Reading speech]")
    print("Editing...",end='')    
    crop_speech(fn, fn_speech)    
    mono(fn_speech, fn_speechmono)    
    print("done.")    
    print("OCR...",end="")
    speech = pytesseract.image_to_string(Image.open(fn_speech))
    print("done.")
    print("Speech: ",end="")
    print(speech.replace('\n',' '))
    
    acted = do_action(speech)
    if not acted:
        speech = pytesseract.image_to_string(Image.open(fn_speechmono))
        acted = do_action(speech)
        if not acted:
            crop_speech_more(fn, fn_speech)
            speech = pytesseract.image_to_string(Image.open(fn_speech))
            acted = do_action(speech)
            if not acted:
                mono(fn_speech, fn_speechmono)
                speech = pytesseract.image_to_string(Image.open(fn_speechmono))
                acted = do_action(speech)    

    print("Waiting...",end="")
    time.sleep(DELAY_ACTION)
    print("done.")
    
    if acted:
        inter_curr -= 1
        if phrases.is_skip(rehab_curr, rehab_max):
            print("[Skipping cutscene]")
            time.sleep(DELAY_PRESKIP)
            skip()                        
        if phrases.is_recruit(rehab_curr, rehab_max):
            print("[Recruit]")
            recruit()
            return True
        if inter_curr==0:
            print("[Using interrogation potion]")
            refresh()
        rehab_curr+=30

    return False
       

def skip():
    print("tap -> skip")
    tap(skip_X, skip_Y)
    time.sleep(DELAY_SKIP)
    print("tap -> anywhere")
    tap(congrats_X, congrats_Y)
    time.sleep(DELAY_CONGRATS)

def refresh():
    global inter_curr, inter_max
    print("tap -> refresh")
    tap(refresh_X, refresh_Y)
    time.sleep(DELAY_REFRESH)
    print("tap -> confirm")
    tap(refresh_conf_X, refresh_conf_Y)
    inter_curr = inter_max
    time.sleep(DELAY_REFRESH)

def recruit():
    print("tap -> recruit")
    tap(recruit_X, recruit_Y)
    time.sleep(DELAY_RECRUIT)
    skip()
    print("<- back")
    back()


def prompt(query):
    str = input(query).lower()
    while str not in ["y","n"]:
        str = input(query).lower()
    return str == "y"

connect_http()

multiple = prompt("Multi-cell drifting? [y/n]:")

another = True
while another:
    ft = True
    while not act(ft):
        ft = False
        time.sleep(DELAY_MID)
    if not multiple:
        another = prompt("Another? [y/n]:")
    else:              
        another = not start_failed
        if another:
            time.sleep(DELAY_NEXTCELL)
            next_prisoner()
        
        


