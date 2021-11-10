from typing import Text
from bs4 import BeautifulSoup
from urllib.request import urlopen

itemsPageUrl = "https://riskofrain2.fandom.com/wiki/Items"
ItemsPage = urlopen(itemsPageUrl)
itemsPageHTML = ItemsPage.read().decode("utf-8")
itemsPageSoup = BeautifulSoup(itemsPageHTML, "html.parser")

def getItemLinks():
    itemLinks = []

    for item in itemsPageSoup.findAll(class_="thumb tright thumbinner"):
        for link in item.find_all('a'):
            if (len(itemLinks) < 1):
                #print(link.get('href'))
                itemLinks.append(link.get('href'))
            elif (link.get('href') != itemLinks[-1]):
                itemLinks.append(link.get('href'))
                #print(link.get('href'))

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
    #print(soup)

    itemInfo = {'name': '',
                'imageUrl': '',
                'effect': '',
                'rarity': '',
                'category': [],
                'id': '',
                'unlock': '',
                'stats': [],
                'cooldown': '',
                }
    # to get stats, return all tr in the infobox, and get text after the Stats [add], add them to the statsdict by index, then when index reaches 3, make a new statsdict

    for result in soup.findAll("table", class_="infoboxtable"):
        #print(result)
        #print(''.join(result.find("th", class_="infoboxname").findAll(text=True)))
        itemInfo['name'] = ''.join(result.find("th", class_="infoboxname").findAll(text=True))
        if result.find("td", class_="infoboxdesc") is None:
            break
        else:
            itemInfo['effect'] = ''.join(result.find("td", class_="infoboxdesc").findAll(text=True)).rstrip()
        #print(result.find("img").get('src'))
        itemInfo['imageUrl'] = result.find("img").get('src')
        tempVal = ''
        for td in result.findAll("td"):
            if td.has_attr("class") == False:
                #print(td.findAll(text=True)[0])
                if (td.findAll(text=True)[0].lower() in itemInfo.keys()):
                    #print(td.findAll(text=True)[0])
                    tempVal = td.findAll(text=True)[0].lower()
                    #print(tempVal)
                elif (tempVal != ''):
                    if (td.findAll(text=True)[0] == '\n'):
                        break
                    elif tempVal == id:
                        itemInfo[tempVal] = td.findAll(text=True)[0][:-2]
                        tempVal = ''
                    elif tempVal == 'category':
                        #print(td.findAll(text=True))
                        itemInfo[tempVal] = td.findAll(text=True)[:-1]
                        tempVal = ''
                    elif tempVal == 'cooldown':
                        itemInfo[tempVal] = td.findAll(text=True)[0].strip()
                        tempVal = ''
                    else:
                        itemInfo[tempVal] = td.findAll(text=True)[0]
                        tempVal = ''
                    #print(td.findAll(text=True)[0])
                #if (len(td.findAll(text=True)) == 2) or (td.findAll(text=True)):
                #    print(td.findAll(text=True))

        statsInfoBool = False
        for tr in result.findAll("tr"):
            if (tr.findAll(text=True)[-1] == 'Add\n'):
                statsInfoBool = True
            elif statsInfoBool:
                #print(tr.findAll(text=True)[1:])
                tempArr = removeNL(tr.findAll(text=True)[1:])
                #print(tempArr)
                itemInfo['stats'].append({
                    'stat': tempArr[0][:-1],
                    'value': tempArr[1][:-1],
                    'stack': tempArr[2],
                    'add': tempArr[-1][:-1],
                })
            
        itemInfo['name'] = itemInfo['name'][:-1]
        itemInfo['id'] = itemInfo['id'][:-1]
        for key in itemInfo.keys():
            print(key, ": ", itemInfo[key])
            #print(itemInfo)

itemLinks = getItemLinks()
#print(len(itemLinks))

#print(itemLinks[0])
for item in itemLinks:
    extractItemInfo(createItemSoup(item))