from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool, cpu_count

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 "
                  "Safari/537.36"
}


def parse_page(page_url):
    response = requests.get(url=page_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('li', class_='catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted')
    results = []
    for item in items:
        title = item.find('a', class_='product-link goods-tile__heading').text.strip()
        try:
            price = item.find('div', class_='goods-tile__prices').find('p', class_='ng-star-inserted').text.strip()
        except:
            price = '[ERROR] Price not found'
        link = item.find('a', class_='product-link goods-tile__heading').get('href').strip()
        status = item.find('div', class_='goods-tile__availability').text.strip()
        results.append({
            'title': title,
            'price': price,
            'link': link,
            'status': status,
        })
    return results


def collect_product(url: str = "https://rozetka.com.ua/protein/c273294/"):
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    page_count = int(soup.find('div', class_="pagination ng-star-inserted")
                     .find_all('li', class_='pagination__item ng-star-inserted')[-1].text.strip())
    print(f'Was founded {page_count} pages ...')

    products = []
    urls = [f'https://rozetka.com.ua/protein/c273294/page={page}/' for page in range(1, page_count + 1)]

    with Pool(cpu_count()) as pool:
        results = pool.map(parse_page, urls)
        for result in results:
            products.extend(result)

    return products
