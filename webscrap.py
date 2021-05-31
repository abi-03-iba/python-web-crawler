import time
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup 
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
client = MongoClient("")#creating mongodb connection # put the connection link of mongodb here
db = client.get_database('WebScrap')#connect to the specific db called webscrap
collection = db.webscrap # connect to the specific connection
#validate an URL by checking whether a particular url returns a valid response or not
def validate(crawlinglink) :
    try:
        response = requests.get(crawlinglink)
        return True
    except:
        return False

#function to check whether particular link already exists or not
def insertedalready(lnk):
    criteria = { '$and' : [{"Linkcrawled":lnk},{"createdAt": {"$gte": time24HoursAgo()}}] }     # '$and' operator joins two or more queries with a logical AND and returns the documents that match all the conditions.
    if (collection.count_documents(criteria) > 0) :                                               
        return True
    else :
        return False
    
def scrape() :
    for i in store: # the links which stored in the store list
        count = 0            
        if (i != ' '):                
                if (validate(i) and  not insertedalready(i)):       #Function calls to validate url as well as check whether url previously exists        
                    collection.insert_one({"Linkcrawled": i, "createdAt":datetime.today().replace(microsecond=0)})
                    print("Inserted link")                  
        if (count==0):
            print("All links crawled already")
        
        if collection.count_documents({}) >= 5000:
            print("Maximum limit has reached")
    time.sleep(5)

def time24HoursAgo() : #it calculates time for 24 hrs back
        today = datetime.today()                                   
        BackTo24Hours = today - timedelta(days=1)                   
        return BackTo24Hours                

if __name__ == '__main__' :
        root="whatever the website you want to crawl paste the url"-->www.google.com
        req = Request(root)
        html_page = urlopen(req)
        soup = BeautifulSoup(html_page,"lxml")
        links = soup.find_all('a')#extract all anchor tags
        store=[]
        for link in links:
            url = link.get('href')   
            if url.startswith('#'):
                continue
            elif url.startswith('/'): #for converting the relative link to absolute link
                url = root + url
                store.append(url)
            else:
                store.append(url)
        print(store)
        while True:        
                with ThreadPoolExecutor(max_workers = 3) as execution:   # thread pool will only have 3 concurrent threads that can process any jobs                     
                    execution.submit(scrape()) #calling scrape cycle
