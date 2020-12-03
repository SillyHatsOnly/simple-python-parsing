import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

def get_html(url):
    response = requests.get(url)
    return response.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('tbody').find_all('td', class_="cmc-table__cell--sort-by__name")
    links = []
    for td in tds:
        a = td.find('a', class_='cmc-link').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('title').text.split('price')[0].strip()
    except:
        name = ''
    try:
        price = soup.find('span', class_='cmc-details-panel-price__price').text.split('USD')[0].strip()
    except:
        price = ''
    data = {'name': name,
            'price': price}
    return data

def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
                         data['price']))

def make_all(link):
    html = get_html(link)
    data = get_page_data(html)
    write_csv(data)
    
def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all'
    all_links = get_all_links(get_html(url))
    with Pool(40) as p:
        p.map(make_all, all_links)
    end = datetime.now()
    total = end - start
    print(str(total))

if __name__ == '__main__':
    main()
