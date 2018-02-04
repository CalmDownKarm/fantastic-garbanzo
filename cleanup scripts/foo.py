import os
import json
import pandas as pd
import pprint
import collections

listoffiles = os.listdir("./Data/Fights")
errors = set()
counterrors = 0
jsonerrors = []

def count_prev(foo):
  if foo==[]:
    return 0
  else:
    return len(foo)

def count_consecutive(foo):
  if foo == []:
    return 0
  else:
    count = 0
    for x in foo[::1]:
      if x == 1:
        count +=1
      else:
        count = 0
    return count

def flatten(d, parent_key='', sep='_'):
    try:
      items = []
      for k, v in d.items():
          new_key = parent_key + sep + k if parent_key else k
          if isinstance(v, collections.MutableMapping):
              items.extend(flatten(v, new_key, sep=sep).items())
          else:
              items.append((new_key, v))
      return dict(items)
    except:
      return {}


def create_dict(indict):
  try:
    # pprint.pprint(indict)
    return {
        'Event_ID': indict['FMLiveFeed']['EventID'],
        'Fight_ID': indict['FMLiveFeed']['FightID'],
        'Max_round': indict['FMLiveFeed']['MaxRounds'],
        'Last_round' : indict['FMLiveFeed']['CurrentRound'],
        'B_ID': indict['FMLiveFeed']['Fighters']['Blue']['FighterID'],
        'B_Name': indict['FMLiveFeed']['Fighters']['Blue']['Name'],
        'R_ID': indict['FMLiveFeed']['Fighters']['Red']['FighterID'],
        'R_Name': indict['FMLiveFeed']['Fighters']['Red']['Name'],
        'Date': indict['Timestamp'].split(' ')[1],
        'Accolades': indict['FMLiveFeed']['Accolade'],
        'Weight Class': indict['FMLiveFeed']['WeightClass']
    }
  except:
    global counterrors
    counterrors+=1
    jsonerrors.append(indict)


def readfile(inputstr, header,flag=False):
    print ("in readFile")
  # try:
    with open(header + inputstr) as datafile:
      herp = json.load(datafile)
      if(flag==True):
        event_fight = inputstr.split('_')
        herp['Event_id'] = event_fight[0]
        herp['Fight_id'] = event_fight[1].split('.')[0]
        boobs = herp['Fighter']
      return herp
  # except:
    # errors.add(header+inputstr)
    # return

def EditDict(indict):
  try:
    print ("in EditDict")
    print(indict)
    bluefighterstring = str(indict['Event_ID'])+str('_')+str(indict['Fight_ID'])+str('_')+ str(indict['B_ID'])+'.json'
    redfighterstring = str(indict['Event_ID'])+str('_')+str(indict['Fight_ID'])+str('_')+ str(indict['R_ID'])+'.json'
    blue_fighter_dict = readfile(bluefighterstring,'./Data/Fights_Fighter/')
    
    
    blue_fighter_statstring = str(indict['B_Name'])+'.json'
    #fixing name error
    foo_name = blue_fighter_statstring.split()[0].lower()+'-'+blue_fighter_statstring.split()[1].lower()
    # print(blue_fighter_statstring)
    # print(foo_name)
    blue_fighter_statdict = readfile(foo_name,'./Data/fighters/')
    if(blue_fighter_statdict):
      blue_fighter_dict['B_Weight'] = blue_fighter_statdict['weight_kg']
      blue_fighter_dict['B_Height'] = blue_fighter_statdict['height_cm']
      blue_fighter_dict['B_HomeTown'] = blue_fighter_statdict['hometown']
      blue_fighter_dict['B_Location'] = blue_fighter_statdict['location']
      blue_fighter_dict['B_Age'] = blue_fighter_statdict['age']
    
    red_fighter_statstring = str(indict['R_Name'])+'.json'
    red_fighter_dict = readfile(redfighterstring,'./Data/Fights_Fighter/')
    foo_name = red_fighter_statstring.split()[0].lower()+'-'+red_fighter_statstring.split()[1].lower()
    red_fighter_statdict = readfile(foo_name,'./Data/fighters/')
    if(red_fighter_statdict):
      red_fighter_dict['R_Weight'] = red_fighter_statdict['weight_kg']
      red_fighter_dict['R_Height'] = red_fighter_statdict['height_cm']
      red_fighter_dict['R_HomeTown'] = red_fighter_statdict['hometown']
      red_fighter_dict['R_Location'] = red_fighter_statdict['location']
      red_fighter_dict['R_Age'] = red_fighter_statdict['age']
    
    val = blue_fighter_dict['Fighter_stats']
    blue_fighter_dict['B_'] = val
    val = blue_fighter_dict['Record']
    blue_fighter_dict['BRecord'] = val
    blue_fighter_dict['BPrev'] = count_prev(blue_fighter_dict['BRecord'])
    blue_fighter_dict['BStreak'] = count_consecutive(blue_fighter_dict['BRecord'])
    blue_fighter_dict.pop('Fighter',None)
    blue_fighter_dict.pop('Fighter_stats',None)
    blue_fighter_dict.pop('Record',None)
    blue_fighter_dict.pop('BRecord',None)
    indict.update(blue_fighter_dict)
    
    val = red_fighter_dict['Fighter_stats']
    red_fighter_dict['R_'] = val
    val = red_fighter_dict['Record']
    red_fighter_dict['RRecord'] = val
    red_fighter_dict['RPrev'] = count_prev(red_fighter_dict['RRecord'])
    red_fighter_dict['RStreak'] = count_consecutive(red_fighter_dict['RRecord'])
    red_fighter_dict.pop('Record',None)
    red_fighter_dict.pop('RRecord',None)
    red_fighter_dict.pop('Fighter',None)
    red_fighter_dict.pop('Fighter_stats',None)
    indict.update(red_fighter_dict)
    
    fightstring = str(indict['Event_ID'])+'_'+str(indict['Fight_ID'])
    if winners[fightstring][0] == '11111':
      indict['winner'] = 'draw'
    elif winners[fightstring][0] == '00000':
      indict['winner'] = 'no contest'
    elif (winners[fightstring][0]== indict['R_ID']):
      indict['winner'] = 'red'
    else:
      indict['winner'] = 'blue'
    indict['winby'] = winners[fightstring][1]
    # print('out EDIT DICT-------------------------------------')
    return indict
  except:
    return {}
pp = pprint.PrettyPrinter(indent=2)

jsons = [readfile(x,"./Data/Fights/") for x in listoffiles]
# pprint.pprint(jsons)
FighterAndEventDic = list(map(create_dict, jsons))
print(len(jsonerrors))
print(counterrors)
# exit()
df = pd.DataFrame(jsonerrors)
df.to_csv("Errors.csv",index=None,encoding="utf-8")
# pp.pprint(FighterAndEventDic[:2]) 
# # At this point I have a list of dict with Event ID, Fight ID 
# # and both red and blue fighter IDs
# # Now iterate through this dict and edit the members. 

winners = readfile("result.json","./Data/")
# print(winners)
# exit()
pprint.pprint(FighterAndEventDic.count(None))
# exit()
updatedDicts = map(EditDict,FighterAndEventDic)
# exit()
flatteneddicts = map(flatten,updatedDicts)

df = pd.DataFrame.from_records(flatteneddicts)

df.to_csv('./Data/finalout.csv',index=False, encoding='utf-8')
for x in errors:
  print(x)
