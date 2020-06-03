# modules
import os
import json
import datetime

# to fill
json_file = 'exported.json' # the json file to parse
customFieldHoursName = "Spent(h)"
useList = True
listName = "" # If empty the list used will be the last month full name (January, February)

# open json
with open(json_file) as data_file:
    data = json.load(data_file)

# Get list id
listId = ""
if(useList):
    if(listName == ""):
        # Get previous month -> This is the name of the list to compute time of
        today = datetime.date.today()
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        listName = lastMonth.strftime("%B")
    
    for list in data["lists"]:
        if(list["name"] == listName):
            listId = list["id"]

    if(listId == ""):
        raise Exception("List id for -" + listName + "- not found")

    print("Computing time on list:" + listName)

# Look for our custom field name containing the hours spent
customFieldHoursId = ""
for customField in data["customFields"]:
    if(customField["name"] == customFieldHoursName):
        customFieldHoursId = customField["id"]

if(customFieldHoursId == ""):
        raise Exception("Field id for -" + customFieldHoursName + "- not found")

print("Found custom field id for " + customFieldHoursName)

# Look for hours on the cards and fill dictionary
hoursDict = {}
cards = data["cards"]
for card in cards:
    if(useList):
        if(card["idList"] != listId):
            continue

    print("Working on: " + card["name"])
    
    #Compose dictionary key -> labels.name concatenated
    hoursKey = ""
    for label in card["labels"]:
        hoursKey += label["name"]

    # Get spent time
    hours = 0
    for customField in card["customFieldItems"]:
        if(customField["idCustomField"] == customFieldHoursId):
            hours = float(customField["value"]["number"])
            print("Found " + customFieldHoursName + ":" + str(hours))

    # Compute it into dict
    if(hours > 0):
        if hoursKey in hoursDict:
            hoursDict[hoursKey] += hours
        else:
            hoursDict[hoursKey] = hours

print(hoursDict)