# # imported required liabrary's

import pandas as pd
import requests
from bs4 import BeautifulSoup
import gspread


# # Function's
def base_url(search_key, sorting = 1):
    sorting = int(sorting)
    if sorting == 1:
        i = '&sort=popularity'
    elif sorting == 2:
        i = '&sort=relevance'
    elif sorting == 3:
        i = '&sort=price_asc'
    elif sorting == 4:
        i = '&sort=price_desc'
    else:
        i = '&sort=recency_desc'
    return f'https://www.flipkart.com/search?q={search_key}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off{i}'

def get_pages_count(url):
    webpage = requests.get(url)
    webdata = webpage.content
    soup = BeautifulSoup(webdata)
    try:
        pages = int(soup.find('div',{'class':'_2MImiq'}).find('span').text.split()[3].replace(',', ''))
    except AttributeError:
        pages = 1
    return min(pages, 10)

def get_urls(url, pages):
    urls = []
    for i in range(1, pages+1):
        urls.append(f'{url}&page={i}')
    return urls

def get_data(search_key, sorting):
    url = base_url(search_key, sorting)
    pages = get_pages_count(url)
    url_list = get_urls(url, pages)
    items = {}
    
    for url in url_list:
        webpage = requests.get(url)
        webdata = webpage.content
        soup = BeautifulSoup(webdata)
        outer_div = soup.find('div',{'class':"_1YokD2 _3Mn1Gg"})
        if len(outer_div.find_all('div',{'class':"_4ddWXP"})) > 0:
            item_box = outer_div.find_all('div',{'class':"_4ddWXP"})
            for item in item_box:
                item_name = item.find('a',{'class':"s1Q9rs"}).text
                try:
                    item_rating = item.find('div', {'class':"_3LWZlK"}).text
                except AttributeError:
                    item_rating = None
                try:  
                    item_price = float(item.find('div', {'class':"_30jeq3"}).text.replace('₹', '').replace(',', ''))
                except AttributeError:
                    item_price = item.find('div', {'class':"_3utEwz"}).text
                try:
                    item_mrp = item.find('div', {'class':"_3I9_wc"}).text.replace('₹', '').replace(',', '')
                except AttributeError:
                     item_mrp = item_price
                link = f'flipkart.com{item.find("a", {"class":"_2rpwqI"})["href"]}'
                        
                image_url = item.find('img')['src']
                
                items[item_name] = [item_rating, item_price, item_mrp, link, image_url]
                
        else:
            item_box = outer_div.find_all('div',{'class':"_13oc-S"})
            for item in item_box:
                item_name = item.find('div',{'class':"_4rR01T"}).text
                try:
                    item_rating = item.find('div', {'class':"_3LWZlK"}).text
                except AttributeError:
                    item_rating = None
                try:  
                    item_price = float(item.find('div', {'class':"_30jeq3 _1_WHN1"}).text.replace('₹', '').replace(',', ''))
                except AttributeError:
                    item_price = 'price not avilable'
                try:
                    item_mrp = item.find('div', {'class':"_3I9_wc _27UcVY"}).text.replace('₹', '').replace(',', '')
                except AttributeError:
                     item_mrp = item_price
                link = f'flipkart.com{item.find("a", {"class":"_1fQZEK"})["href"]}'
                image_url = item.find('img')['src']
                items[item_name] = [item_rating, item_price, item_mrp, link, image_url]
                      
    dataframe = pd.DataFrame.from_dict(items, orient = 'index', columns = ['rating', 'current_price', 'mrp', 'item_url', 'image_url']).reset_index().rename(columns = {'index':'item'})
    return dataframe

def push_to_google_sheet(df):
    sa = gspread.service_account()
    sh = sa.open('scrapped_data')
    try:
        worksheet = sh.worksheet(search_key)
    except:
        worksheet = sh.add_worksheet(title=search_key, rows = 1000, cols = 20)
    worksheet.add_rows([df.columns.values.tolist()] + df.values.tolist())

search_key = input('what you want to find:-  ')
sorting = input('how you want to sort output - \n1 - popularity\n2 - relevance\n3 - Price -- low to high\n4 - Price -- high to low\n5 - Newest First\nplease select a No -- \n')

ans = get_data(search_key, sorting)
push_to_google_sheet(ans)
