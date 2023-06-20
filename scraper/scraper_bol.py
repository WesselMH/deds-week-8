import requests
import json
from bs4 import BeautifulSoup
import csv
import io
from PIL import Image

url = "https://www.bol.com/nl/nl/s/?searchtext=zakmes"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
links = []

page_text = soup.find(class_= "pagination")
pages = int(page_text.findAll(class_= "js_pagination_item")[-2].text)
# print(pages)

for number in range(1, 
                    # pages + 1
                    25 ):
    url = "https://www.bol.com/nl/nl/s/?page=" + str(number) +"&searchtext=zakmes&view=list"
    link = requests.get(url)
    soup = BeautifulSoup(link.text, 'html.parser')
    ul = soup.find(class_= "list-view product-list js_multiple_basket_buttons_page")
    li = ul.find_all(class_="product-item--row js_item_root")
    for link in li:
        linkurl = "https://www.bol.com" + link.find('a')['href']
        links.append(linkurl)
        # print(linkurl)

with open("bol.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ['name', 'price', 'reviews']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
            
    for link in links:
        product = requests.get(link)
        soupproduct = BeautifulSoup(product.text, "html.parser")
        
        print(link)
        if (soupproduct.find("div", {"data-test": "brand"})):
            name = soupproduct.find(class_= "page-heading").text
            brand = soupproduct.find("a", {"data-role": "BRAND"}).get_text().strip()
        else:
            brand = "no brand"
        
        if not(soupproduct.find("div", {"data-test": "outofstock-buy-block"})):
            prijsdeel = soupproduct.find(class_= "price-block").find(class_= "price-block__price").get_text().strip()
            prijs = ','.join(prijsdeel.splitlines())    
        else:
            prijs = "niet leverbaar"
        print(prijs)
        
        img = soupproduct.find(class_="image-slot").find("img").get('src')
        img_content = requests.get(img).content
        image_file = io.BytesIO(img_content)
        image = Image.open(image_file)
        print(image)
        file_path = "images/bol/" + img.split("/")[-2] + ".jpeg"
        # print(file_path)
        with open(file_path, 'wb') as f:
            image.save(f,"JPEG")
        # print(img_URL)
        
        # print(img)
        
        allReviews = []
        if not (soupproduct.find("section", {"id":"no-reviews"}) ):
            reviewDiv = soupproduct.find(class_= "reviews")
            review = reviewDiv.find_all(class_= "review")
            
            for body in review:
                body_review = body.find(class_= "review__body")
                p_review = body_review.find("p", {"data-test": "review-body"}).get_text()
                # print(p_review)
                
                allReviews.append(p_review)
            # print(allReviews)
        else:
            allReviews.append("")
        
        writer.writerow({'name': brand,'price': prijs, 'reviews': allReviews})
    
    
