import Frontier as fr
import pandas as pd
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.robotparser as urobot
import threading
# Crawler Parameters
BACKQUEUES= 3
THREADS= BACKQUEUES*3
FRONTQUEUES= 5
WAITTIME= 15;
USED_URL = []


def remove_duplicate(url_list):
    for i in range(len(url_list)):
        if url_list[i] in USED_URL:
            url_list.remove(url_list[i])
    return url_list


def filter_url(url):
    obtained_list_url = []
    rp = urobot.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    rp.read()
    if rp.can_fetch("*", url):
        site = urllib.request.urlopen(url)
        sauce = site.read()
        soup = BeautifulSoup(, "html.parser")
        actual_url = site.geturl()[:site.geturl().rfind('/')]

        my_list = soup.find_all("a", href=True)
        for i in my_list:
            # rather than != "#" you can control your list before loop over it
            if i != "#":
                newurl = str(actual_url) + "/" + str(i)
                try:
                    if rp.can_fetch("*", newurl):
                        None
                    else:
                        obtained_list_url.append(newurl)
                except:
                    pass
    else:
        print("cannot scrap")
    return obtained_list_url



def crawler_thread_task(thread_name, fr_obj):
    if len(USED_URL) >999:
        thread_name.exit()
    url = fr_obj.select_url_from_back_queue()
    USED_URL.append(url)
    try:
        url_obj = urllib.request.urlopen(url)
        html = url_obj.read()
        domain_of_back_queue_selected = urlparse(url).geturl()
        with open(domain_of_back_queue_selected + ".txt", mode="wb") as d:
            d.write(html)

        soup = BeautifulSoup(html, 'html.parser')
        obtained_list = []
        for link in soup.find_all('a'):
            if link.get('href') != '#':
                obtained_list.append(link.get('href'))
        removed_duplicate_url_list = remove_duplicate(obtained_list)
        return_filtered_url_list = filter_url(url)
        for i in range(len(removed_duplicate_url_list)):
            if removed_duplicate_url_list[i] in return_filtered_url_list:
                removed_duplicate_url_list.remove(return_filtered_url_list[i])
        fr_obj.add_seed_URLs(removed_duplicate_url_list)
        fr_obj.add_url_back_queue_first_time()

    # Catching the exception generated
    except Exception as e:
        print(str(e))


class myThread (threading.Thread):
   def __init__(self, threadID, name, fr_obj):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.fr_obj = fr_obj
   def run(self):
      print("Starting " + self.name)
      crawler_thread_task(self.name, self.fr_obj)
      print("Exiting " + self.name)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    df = pd.read_csv("Seed URLS.csv")
    print("hello")
    seed_url_list = df['0'].tolist()
    fr_obj = fr.frontier(FRONTQUEUES, BACKQUEUES)
    fr_obj.add_seed_URLs(seed_url_list)
    fr_obj.add_url_back_queue_first_time()
    t_list = []
    for i in range(THREADS):
        t_list.append(myThread(i, "Thread-{i}", fr_obj))
    for i in range(THREADS):
        t_list[i].start()

    while len(USED_URL) <1000:
        None

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
