from typing import Text
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pprint
from dbManager import dbManager

itemsPageUrl = "https://riskofrain2.fandom.com/wiki/Items"
ItemsPage = urlopen(itemsPageUrl)
itemsPageHTML = ItemsPage.read().decode("utf-8")
itemsPageSoup = BeautifulSoup(itemsPageHTML, "html.parser")

def getItemLinks():
    itemLinks = []

    for item in itemsPageSoup.findAll(class_="thumb tright thumbinner"):
        for link in item.find_all('a'):
            if (len(itemLinks) < 1):
                itemLinks.append(link.get('href'))
            elif (link.get('href') != itemLinks[-1]):
                itemLinks.append(link.get('href'))

    return itemLinks
    
def createItemSoup(itemUrl):
    itemPageUrl = "https://riskofrain2.fandom.com" + itemUrl
    ItemPage = urlopen(itemPageUrl)
    itemPageHTML = ItemPage.read().decode("utf-8")
    itemPageSoup = BeautifulSoup(itemPageHTML, "html.parser")

    return itemPageSoup;

def removeNL(arr):
    arr.remove('\n')
    for val in arr:
        if val == '\n':
            arr.remove('\n')
    return arr

def extractItemInfo(soup):

    itemInfo = {'name': '',
                'imageUrl': '',
                'effect': '',
                'rarity': '',
                'category': [],
                'id': -1,
                'unlock': '',
                'stats': [],
                'cooldown': '',
                }

    for result in soup.findAll("table", class_="infoboxtable"):
        itemInfo['name'] = ''.join(result.find("th", class_="infoboxname").findAll(text=True))
        if result.find("td", class_="infoboxdesc") is None:
            break
        else:
            itemInfo['effect'] = ''.join(result.find("td", class_="infoboxdesc").findAll(text=True)).rstrip()
        itemInfo['imageUrl'] = result.find("img").get('src')
        tempVal = ''
        for td in result.findAll("td"):
            if td.has_attr("class") == False:
                if (td.findAll(text=True)[0].lower() in itemInfo.keys()):
                    tempVal = td.findAll(text=True)[0].lower()
                elif (tempVal != ''):
                    if (td.findAll(text=True)[0] == '\n'):
                        break
                    elif tempVal == id:
                        itemInfo[tempVal] = td.findAll(text=True)[0][:-2]
                        tempVal = ''
                    elif tempVal == 'category':
                        itemInfo[tempVal] = td.findAll(text=True)[:-1]
                        tempVal = ''
                    elif tempVal == 'cooldown':
                        itemInfo[tempVal] = td.findAll(text=True)[0].strip()
                        tempVal = ''
                    else:
                        itemInfo[tempVal] = td.findAll(text=True)[0]
                        tempVal = ''

        statsInfoBool = False
        for tr in result.findAll("tr"):
            if (tr.findAll(text=True)[-1] == 'Add\n'):
                statsInfoBool = True
            elif statsInfoBool:
                tempArr = removeNL(tr.findAll(text=True)[1:])
                itemInfo['stats'].append({
                    'stat': tempArr[0][:-1],
                    'value': tempArr[1][:-1],
                    'stack': tempArr[2],
                    'add': tempArr[-1][:-1],
                })

        return itemInfo

notRequiredKeys = []

def cleanDict(dict):
    keysToPop = []
    for key in dict.keys():
        if (dict[key] == -1) or (dict[key] == '') or (dict[key] == []):
            keysToPop.append(key)

    for key in keysToPop:
        dict.pop(key)

    dict['name'] = dict['name'][:-1]
    for key in dict.keys():
        if key == 'id':
            dict['id'] = dict['id'][:-1]


    return dict, keysToPop

itemLinks = getItemLinks()

allData = []
n = 1
for item in itemLinks:
    itemInfo, tempNotRequiredKeys = cleanDict(extractItemInfo(createItemSoup(item)))
    print(f'Item: {n}')
    n += 1
    allData.append(itemInfo)
    for tempKey in tempNotRequiredKeys:
        if tempKey not in notRequiredKeys:
            notRequiredKeys.append(tempKey)

    #pprint.pprint(itemInfo)

print(notRequiredKeys)

with open('db-credentials.txt') as f:
    credURL = f.readline()

db = dbManager(allData, credURL)
db.capNewCollection()