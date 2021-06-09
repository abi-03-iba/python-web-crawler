from pymongo import MongoClient
from datetime import datetime, timedelta
from time import sleep
from config import maxcount,root
from crawler import root,validate

def connectdb():
    global linkcollection # for using this variable to another functions
    cluster=MongoClient("  #your mongodb connection url    ")
    db=cluster["WebScrap"]  #establishng the db connection
    linkcollection=db["webscrap"] # establishing a connection to the collection
    return linkcollection
def getPendingLinks():
    connectdb()  # for using the linkcollection
    return linkcollection.find({})
    
def time24HoursAgo() : #it calculates time for 24 hrs back
        today = datetime.today()                                   
        BackTo24Hours = today - timedelta(days=1)                   
        return BackTo24Hours  

def insertedalready(link):
    
    criteria = { '$and' : [{"Linkcrawled":link},{"createdAt": {"$gte": time24HoursAgo()}}] }     # '$and' operator joins two or more queries with a logical AND and returns the documents that match all the conditions.
    if (linkcollection.count_documents(criteria) > 0) :                                               
        return True
    else :
        return False
def save(links):
    connectdb()
    for i in links:
        count=0            
        if (i != ' '):                
                if (validate(i) and  not insertedalready(i)):       #Function calls to validate url as well as check whether url previously exists        
                    linkcollection.insert_one({"Linkcrawled": i, "createdAt":datetime.today().replace(microsecond=0)})
                    count+=1
                    print("Inserting link")
        if(count==0):
            print("already inserted") # if the link is already inserted
        
        if linkcollection.count_documents({}) >=maxcount :
            print("Maximum limit has reached") # if it reached the maximum limit 
            time.sleep(100)



    
