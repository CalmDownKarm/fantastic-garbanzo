import os
import json
import pandas as pd
listoffiles = os.listdir("./Data/Fights")
new_list = []
for file in listoffiles:
  new_list.append("./Data/Fights/"+file)
listoffiles = new_list

def readfile(inputstr):
  with open(inputstr) as datafile:
    return json.load(datafile) 

new_list = map(readfile,listoffiles)

def create_dict(indict):
  Data = {
    'Event_ID': indict['FMLiveFeed']['EventID'],
    'Fight_ID': indict['FMLiveFeed']['FightID'],
    'Blue_fighter_id': indict['FMLiveFeed']['Fighters']['Blue']['FighterID'],
    'Blue_name': indict['FMLiveFeed']['Fighters']['Blue']['Name'],
    'Red_fighter_id': indict['FMLiveFeed']['Fighters']['Red']['FighterID'],
    'Red_name': indict['FMLiveFeed']['Fighters']['Red']['Name']
  }
  return Data

listofDicts = map(create_dict,new_list)


df = pd.DataFrame.from_records(listofDicts)
print df.head()