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


def extractItemInfo(soup):
    #print(soup)

    #if rarity = equiptment, don't include
    itemInfo = {'name': '',
                'imageURL': '',
                'effect': '',
                'rarity': '',
                'category': [],
                'id': 0,
                'unlock': ''
                }

    for result in soup.findAll("table", class_="infoboxtable"):
        #print(result)
        print(''.join(result.find("th", class_="infoboxname").findAll(text=True)))
        itemInfo['name'] = ''.join(result.find("th", class_="infoboxname").findAll(text=True))
        print(result.find("img").get('src'))
        itemInfo['imageUrl'] = result.find("img").get('src')
        tempVal = ''
        for td in result.findAll("td"):
            if td.has_attr("class") == False:
                print(td.findAll(text=True)[0])
                if (td.findAll(text=True)[0].lower() in itemInfo.keys()):
                    #print(td.findAll(text=True)[0])
                    tempVal = td.findAll(text=True)[0].lower()
                elif (tempVal != ''):
                    if tempVal == id:
                        itemInfo[tempVal] = td.findAll(text=True)[0][:-2]
                        tempVal = ''
                    else:
                        itemInfo[tempVal] = td.findAll(text=True)[0]
                        tempVal = ''
        
                
                #if (len(td.findAll(text=True)) == 2) or (td.findAll(text=True)):
                #    print(td.findAll(text=True))
        print(itemInfo)

itemLinks = getItemLinks()
#print(len(itemLinks))

print(itemLinks[0])
extractItemInfo(createItemSoup(itemLinks[0]))