import pandas as pd
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

#url = "https://www.grubhub.com/restaurant/cast-iron-waffles-9604-longstone-ln-charlotte/1444707"

#html = urlopen(url)
import codecs
htmlfile = './Cast Iron Waffles Delivery - 9604 Longstone Ln Charlotte _ Order Online With Grubhub (12_09_2020 03_06_15).html'
file = codecs.open(htmlfile, "r", "utf-8")


soup = BeautifulSoup(file.read(),'lxml')

section= soup.find_all('section',{'class':'cb-expansion-panel'})

data = []
for main in section:
    
    header = main.find('div', {'class': 'menuSection-headerTitle u-flex u-flex-justify-xs--between'}).getText()
    item_div = main.find_all('div',{'class':'s-card-wrapper'})
    
    for menu in item_div:

        div = menu.find('div',{'class':'u-inset-squished-3'})
        name = div.find('a',{'class':'menuItem-name'}).getText()
        descp = div.find('p',{'class':'u-text-secondary'}).getText()
        p = soup.find('span', {'itemprop':'price'}).getText()

        data.append([header,name,descp,p])

        
df = pd.DataFrame(data,columns=['categories','menu', 'description', 'price'])

df.to_excel('sitemenu.xlsx', index = False)

