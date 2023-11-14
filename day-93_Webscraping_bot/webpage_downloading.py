from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

# ask for product name
product_name = input("Enter the product name: ")

# add + sign between the words
product_name = product_name.replace(" ", "+")

# ask number of products to download
number_of_products = int(input("Enter the number of products to download: "))

# number of pages to download
number_of_pages = number_of_products // 35 + 1

# Set the options
options = Options()
options.add_argument("--headless")

# Set the service
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

final_products = []
print("Downloading the products...")
for i in range(1, number_of_pages + 1):
    driver.get(f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={product_name}&viewtype=G&page={i}")
    driver.minimize_window()

    # Get the page content
    for i in range(1, 50):
        product = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div[5]/div[3]/div/div/div/div[{i}]')
        product_li = product.text.split("\n")
        try:
            if len(product_li) >= 7:
                p_name = [product_li[0], product_li[1]]
                final_products.append({
                    "Product Name": [p_name[0] if len(p_name[0]) > len(p_name[1]) else p_name[1]][0],
                    "Product Price Range": [i for i in product_li if "US$" in i][0],
                    "Product Min Order": [i.split(':')[1] for i in product_li if "Min. order" in i][0],
                    "Seller Name": [i for i in product_li if "CN Supplier" in i][0],
                    "Product Link": product.find_element(By.TAG_NAME, "a").get_attribute("href"),
                })
            print(f"Product {i} downloaded successfully")
        except Exception as e:
            print("error while getting product, ", e)

driver.quit()

# Save the data
try:
    df = pd.DataFrame(final_products[:number_of_products])
except Exception as e:
    print("Error while creating dataframe, ", e)
    df = pd.DataFrame(final_products)
df.to_csv("products.csv", index=False)
print("Data saved successfully")
