import requests
import json
from bs4 import BeautifulSoup
import csv

url = "https://www.bol.com/nl/nl/s/?searchtext=zakmes"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
links = []

page_text = soup.find(class_= "pagination")
pages = int(page_text.findAll(class_= "js_pagination_item")[-2].text)
# print(pages)

for number in range(1, 
                    # pages + 1
                    2 ):
    url = "https://www.bol.com/nl/nl/s/?page=" + str(number) +"&searchtext=zakmes&view=list"
    link = requests.get(url)
    soup = BeautifulSoup(link.text, 'html.parser')
    ul = soup.find(class_= "list-view product-list js_multiple_basket_buttons_page")
    li = ul.find_all(class_="product-item--row js_item_root")
    for link in li:
        linkurl = "https://www.bol.com" + link.find('a')['href']
        links.append(linkurl)
        print(linkurl)
        
for link in links:
    product = requests.get(link)
    soupproduct = BeautifulSoup(product.text, "html.parser")
    
    name = soupproduct.find(class_= "page-heading").text
    
    reviewDiv = soupproduct.find(class_= "reviews")
    print(reviewDiv)
    
    
