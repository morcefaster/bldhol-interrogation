import re


success_pts = 30

pacify = ["routine", # Karg M
    "Hardly worth", # Karg F    
    "that was going to work", # Yivnian M
    "trust you so", # Yivnian F
    "placate", # Luxuriant M
    "lower my guard", # Luxuriant F
    "meaning of this", # Ugrull M
    "resort to", # Ugrull F
    "time on your", # Tidestorm M
    "that will work on me", # Tidestorm F
    "comforting", # Gryphon M
    "sincere" # Gryphon F
    ]

communicate = [
    "nothing you say",
    "perhaps",
    "nothing to say",
    "sincerity",
    "jabbering",
    "trip me",
    "with honor",
    "not completely",
    "enough",
    "problems",
    "proper talk",
    "considering" ]

punish = [
     "judge",
     "trample",
     "far worse",
     "no effect",
     "pay for that",
     "accusations",
     "throats out",
     "recrimination",
     "make me cave",
     "guard the dragon",
     "companions",
     "pain will never"
     ]

intimidate = [
    "hollow",
    "fancy",
    "empty words",
    "have no trust",
    "convince",
    "luck with me",
    "weaklings like you",
    "pathetic terms",
    "hold fast",
    "ulterior",
    "meaningless",
    "fruitless",    
]


def lo(str):
    str = str.lower()
    return re.sub(r'[^a-z]','',str)

def do(str):
    return re.sub(r'[^0-9]','',str)

def action(str):    
    str = lo(str)
    match = [s for s in pacify if lo(s) in str]    
    if match:
        return "pacify"
    match = [s for s in communicate if lo(s) in str]
    if match:
        return "communicate"
    match = [s for s in punish if lo(s) in str]
    if match:
        return "punish"
    match = [s for s in intimidate if lo(s) in str]
    if match:
        return "intimidate"
    return "failed to match"

#def action(str):    
#    str = lo(str)
#    match = [s for s in pacify if str.startswith(lo(s))]    
#    if match:
#        return "pacify"
#    match = [s for s in communicate if str.startswith(lo(s))]
#    if match:
#        return "communicate"
#    match = [s for s in punish if str.startswith(lo(s))]
#    if match:
#        return "punish"
#    match = [s for s in intimidate if str.startswith(lo(s))]
#    if match:
#        return "intimidate"
#    return "failed to match"

    
recruit_breakpoints = {
    "300":[80, 150, 200, 300],
    "500":[100,200,300,400,500],
    "1000":[100,250,500,1000]
    }

def is_skip(reh_c, reh_m):
    rc = int(reh_c)
    for bp in recruit_breakpoints[str(reh_m)]:
        if bp > rc:
            return rc + success_pts >= bp
    return False
    

def is_recruit(reh_c, reh_m):
    return int(reh_c)+30 >= int(reh_m)
        

