import requests
from urllib.request import Request, urlopen
from config import root
import db
from bs4 import BeautifulSoup
def crawl(link):
    response=validate(link) #validating the link
    links=extractlinks(link) #extracting the href links 
    db.save(links) #saving the each link in the database
def validate(crawlinglink) :
    try:
        response = requests.get(crawlinglink)
        return True
    except:
        return False
def extractlinks(link):
    global links
    req = Request(root)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page,"lxml")
    tag = soup.find_all('a')       #extract all anchor tags
    links=[]
    for link in tag:
     url = link.get('href')   
     if url.startswith('#'):    #invalid link
        continue
     elif url.startswith('/'): #for converting the relative link to absolute link
        url = root + url
        links.append(url)
     elif url.startswith('//'):
        url="https://"+url
        links.append(url)
     elif url.startswith('javascript:'):#invalid url
        continue 
     
     else:
        links.append(url)
                
    print(links)
    return links

        


