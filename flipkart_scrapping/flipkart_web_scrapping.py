
import pandas as pd
import requests
from bs4 import BeautifulSoup

search_key = input('what you want to find:-  ')
url = f'https://www.flipkart.com/search?q={search_key}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'


def pages_count(url):
    webpage = requests.get(url)
    webdata = webpage.content
    soup = BeautifulSoup(webdata)
    pages = int(soup.find('div',{'class':'_2MImiq'}).find('span').text.split()[3].replace(',', ''))
    return min(pages, 10)



# In[103]:


pages


# In[104]:


def urls(url, pages = pages_count(url)):
    urls = []
    for i in range(1, pages+1):
        urls.append(f'{url}&page={i}')
    return urls


# In[105]:


urls = urls(url)


# In[106]:


urls


# In[112]:


def get_data(urls, sort = None):
    items = {}
    for url in urls:
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
                    item_rating = 'not rated'
                try:  
                    item_price = item.find('div', {'class':"_30jeq3"}).text.replace('₹', '').replace(',', '')
                except AttributeError:
                    item_price = item.find('div', {'class':"_3utEwz"})
                try:
                    item_mrp = item.find('div', {'class':"_3I9_wc"}).text.replace('₹', '').replace(',', '')
                except AttributeError:
                     item_mrp = item_price
                        
                image_url = item.find('img')['src']
                items[item_name] = [item_rating, item_price, item_mrp, image_url]
                
        else:
            item_box = outer_div.find_all('div',{'class':"_13oc-S"})
            for item in item_box:
                item_name = item.find('div',{'class':"_4rR01T"}).text
                try:
                    item_rating = item.find('div', {'class':"_3LWZlK"}).text
                except AttributeError:
                    item_rating = 'not rated'
                try:  
                    item_price = item.find('div', {'class':"_30jeq3 _1_WHN1"}).text.replace('₹', '').replace(',', '')
                except AttributeError:
                    item_price = 'price not avilable'
                try:
                    item_mrp = item.find('div', {'class':"_3I9_wc _27UcVY"}).text.replace('₹', '').replace(',', '')
                except AttributeError:
                     item_mrp = item_price
                image_url = item.find('img')['src']
                items[item_name] = [item_rating, item_price, item_mrp, image_url]
            
            
            
            
            
    dataframe = pd.DataFrame.from_dict(items, orient = 'index', columns = ['rating', 'current_price', 'mrp', 'image_url']).reset_index().rename(columns = {'index':'item'})
    return dataframe

        
    


# In[113]:


ans = get_data(urls)


# In[115]:


print(ans)

