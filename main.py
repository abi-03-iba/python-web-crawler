from db import connectdb,getPendingLinks
from crawler import crawl
from config import root
from concurrent.futures import ThreadPoolExecutor
#connect to the database
#crawl the root URl
if __name__=='__main__':
    connectdb()
    crawl(root)
    while True:
        links=getPendingLinks()
        with ThreadPoolExecutor(max_workers = 5) as execution:   # thread pool will only have 5 concurrent threads that can process any jobs
            execution.map(crawl,links) #calling crawling cycle
            
