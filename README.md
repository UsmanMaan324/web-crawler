# web-crawler

# Frontier
Frontier is a web crawling framework consisting of crawl frontier https://nlp.stanford.edu/IR-book/html/htmledition/the-url-frontier-1.html , and distribution/scaling primitives, allowing to build a large scale online web crawler.

Frontier takes care of the logic and policies to follow during the crawl. It stores and prioritises links extracted by the crawler to decide which pages to visit next, and capable of doing it in distributed manner.

Frontier is mainly used to select the link that should be procceed.

# crawler_thread_task

It is a function that actually that scrape web page by using urllib library. After scraping the web page parsing is done with the help of BeautifulSoup and get all the url. After it the we filter the url and exract all link that can be accessed. These exracted link is added in forntier.

We used parrallel programing and created many thread to crawle the web pages and saved it in text file.
