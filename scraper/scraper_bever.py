import requests
import json
from bs4 import BeautifulSoup
import csv


url = "https://www.bever.nl/c/uitrusting/tenten.html?size=48&page=0&filter=%2526filter%253Dnl_camping_equipment_type%253A%2528tents%2529"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
links = []

page_text = soup.find(class_="as-m-pagination")
pages = int(page_text.findAll(class_="as-a-btn__text")[-1].text)
productID = None

for page in range(1, pages + 1):
        url = "https://www.bever.nl/c/uitrusting/tenten.html?size=48&page={page}&filter=%2526filter%253Dnl_camping_equipment_type%253A%2528tents%2529"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        product_tiles = soup.find_all('div', class_='as-m-product-tile')
        
        for tile in product_tiles:
            product_tile_link = tile.find("a")["href"]
            product_link = "https://www.bever.nl" + product_tile_link
            # print(product_tile_link)
            links.append(product_link)
    # links.append("https://www.bever.nl/p/nomad-blazer-limited-slaapzak-G4HB3L0006.html?colour=2530") 

# links = product_tiles.find_all(class_= "as-a-link as-a-link--container as-m-product-tile__link")  
with open("bever.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ['name', 'price', 'reviews']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
            
    for link in links:
        product = requests.get(link)
        soupproduct  = BeautifulSoup(product.text, 'html.parser')
        
        name = soupproduct.find(class_="as-a-text as-a-text--title")
        brand = name.parent.text
        
        prijs = soupproduct.find(class_="as-a-price__value as-a-price__value--sell").text.replace('€', '')
        
        productID = link.split("-")[-1].split(".")[0]
        
        string = "https://widgets.reevoo.com/api/product_reviews?per_page=3&trkref=BEV&sku=" + productID + "&locale=nl-NL&display_mode=embedded&page=1"
        review_page = requests.get(string).text
        
        json_data = json.loads(review_page)
        
        body = json_data["body"]
        reviews = body["reviews"]
        allReviews = []
        
        for element in reviews:
            review = str(element["text"]).replace("{", "").replace("}", "").replace("'", "")
            # print(review)
            allReviews.append(review)
        # print(allReviews)
        
        writer.writerow({'name': brand,'price': prijs, 'reviews': allReviews})
        print(brand)
        

    

    
    # with open("temp.json", "w") as file:
    #     json.dump(json_data,file)
    #     # file.write(review_page)
    
    # with open("temp.json", "r") as f:
    #     content = f.read()
    #     # if "reviews" in content:
    #     content.split("review")[-1]
    #     print(content)  
    
    # reviews = []
    # print(review_page)
    # good_points = review_page.find("text")
    
    # for good_point in review_page:
    #     review = good_point.find("text")
    #     print(review)
        
    # review_page_placeholder = review_page
    # print(good_points)
    # csvfile.write(soupproduct.text)
            
    
    # for item in product_tiles: 


# https://widgets.reevoo.com/api/product_reviews?per_page=3&trkref=BEV&sku={productID}&locale=nl-NL&display_mode=embedded&page=1


