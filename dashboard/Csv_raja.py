import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.amazon.in/s?rh=n%3A5311359031%2Cp_8%3A70-100&tag=rnwap-20&utm_source=pocket_mylist"
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}

response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.content, "html.parser")

deals = soup.find_all("div", class_="s-card-container")

csv_file = open("amazon_deals.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)

csv_writer.writerow(["Product Name", "Price", "Discount Percentage", "Product URL", "MRP Price", "About this item", "Image URL", "Store Name", "Category"])

try:
    for deal in deals:
        try:
            # Extract product name
            name = deal.find("span", class_="a-size-medium a-color-base a-text-normal")
            if name is None:
                name = deal.find("span", class_="a-size-base-plus a-color-base a-text-normal")
            name = name.get_text().strip()

            # Extract product price
            price = deal.find("span", class_="a-price-whole")
            if price is not None:
                price = price.get_text().replace(",", "").strip()
            else:
                continue

            # Extract product discount percentage
            letter_space = deal.findAll('span', class_="a-letter-space")
            discount_percentage = None
            if len(letter_space) > 2:
                discount_percentage = letter_space[1].find_next('span').get_text()
            elif len(letter_space) != 1:
                discount_percentage = letter_space[-1].find_next('span').get_text()
            else:
                discount_percentage = letter_space[0].find_next('span').get_text()
            if discount_percentage is None:
                continue

            # Extract product URL
            product_url = deal.find("a", class_="a-link-normal s-no-outline")
            if product_url is not None:
                product_url = "https://www.amazon.in" + product_url['href']

            # Extract MRP price
            mrp_price = deal.find("span", class_="a-price a-text-price")
            if mrp_price is not None:
                mrp_price = mrp_price.find("span", class_="a-offscreen").get_text()

            # Extract "About this item" description
            about_this_item = deal.find("div", class_="a-section a-size-small")
            if about_this_item is not None:
                about_this_item = about_this_item.get_text().strip()

            # Extract image URL
            image_url = deal.find("img", class_="s-image")
            if image_url is not None:
                image_url = image_url['src']

            # Extract store name
            store_name = deal.find("span", class_="a-size-base a-color-secondary")
            if store_name is not None:
                store_name = store_name.get_text().strip()

            # Extract category
            category = deal.find("span", class_="a-size-base a-color-base")
            if category is not None:
                category = category.get_text().strip()

            csv_writer.writerow([str(name), str(price), str(discount_percentage), str(product_url), str(mrp_price),
                                 str(about_this_item), str(image_url), str(store_name), str(category)])

        except:
            pass
except:
    pass
finally:
    csv_file.close()
