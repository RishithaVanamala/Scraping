import requests
from bs4 import BeautifulSoup
import csv
import json
import os

def scrape_crate_and_barrel(url):
    # Set a User-Agent header to simulate a request from a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Use a session to persist headers across requests
    with requests.Session() as session:
        response = session.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract JSON data from the script tag
            script_tag = soup.find('script', {'type': 'application/ld+json', 'data-testid': 'schema-product-collection'})
            json_data = json.loads(script_tag.string)

            # # Create a dictionary to store SKU-color mapping
            # sku_color_mapping = {}

            # # Loop through each product in the second code
            # for product_container in soup.select('.main-wrap .product-card'):
            #     try:
            #         sku = product_container['id']
            #         color_container = product_container.select_one('.product-colorbar-container')
            #         colors = [label['title'] for label in color_container.select('.colorbar-label')] if color_container else []

            #         # Add SKU-color mapping to the dictionary
            #         sku_color_mapping[sku] = colors
            #     except AttributeError as e:
            #         print(f"Error processing a product in the second code. {e}")

            # Creating a CSV file in the 'csv' folder
            csv_folder = os.path.join('..', 'csv')
            csv_file_path = os.path.join(csv_folder, 'Coffee Tables.csv')  # Use os.path.join to create the correct file path

            # Creating the 'csv' folder if it doesn't exist
            os.makedirs(csv_folder, exist_ok=True)  # Create the folder if it doesn't exist

            # Creating a CSV file to store the scraped data
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Product Id', 'Product Name', 'Price', 'Link of the product', 'Scraped Image Link']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write the header row in the CSV file
                writer.writeheader()

                # Loop through each product in the first code
                for product_data in json_data['hasOfferCatalog']['itemListElement']:
                    sku = product_data['sku']
                    name = product_data['name']
                    price = f"${product_data['price']}"  # Append $ to the price
                    original_link = product_data['url']

                    # Check if the SKU is in the mapping dictionary
                    # if sku in sku_color_mapping:
                    #     colors = sku_color_mapping[sku]
                    # else:
                    #     colors = []

                    # Extract the 'Scrape' attribute directly from the JSON data
                    scrape_image = product_data['image']

                    # Write the data to the CSV file
                    writer.writerow({
                        'Product Id': sku,
                        'Product Name': name,
                        'Price': price,
                        'Link of the product': original_link,
                        'Scraped Image Link': scrape_image
                    })

        else:
            print('Failed to retrieve the page. Status code:', response.status_code)

# URL of the Crate and Barrel website
crate_and_barrel_url = 'https://www.crateandbarrel.com/furniture/coffee-tables/1'

# Call the function to scrape and save the data
scrape_crate_and_barrel(crate_and_barrel_url)
