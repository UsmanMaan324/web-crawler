import random
from queue import Queue
from urllib.parse import urlparse
from datetime import datetime
import time
TIME_STAMP = [None] * 3


def get_min_time_stamp():
    min = TIME_STAMP[0]
    index = 0;
    for i in range(len(TIME_STAMP)):
        if TIME_STAMP[i] < min:
            min = TIME_STAMP
            index = i
    return index


def intialization_of_time_stamp():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    for i in TIME_STAMP:
        i = current_time

def prioritizer(URL, f):
    """
    Take URL and returns priority from 1 to F
    Right now it like a stub function.
    It will return a random number from 1 to f for given inputs.
    """
    return random.randint(0, (f-1))


def tournament_selection(number_of_front_queue):
    tournament_size = random.randint(1, number_of_front_queue)
    tournament_element = [None] * number_of_front_queue
    for i in range(tournament_size):
        element = random.randint(0, number_of_front_queue - 1)
        tournament_element[element] = element
    for i in range(number_of_front_queue - 1, 0, -1):
        if tournament_element[i] is not None:
            return i
    return -1


class frontier:

    def __init__(self, number_of_front_queue, number_of_back_queue):
        self.front_queue = []
        for i in range(number_of_front_queue):
            self.front_queue.append(Queue(maxsize=50))

        self.back_queue = []
        for i in range(number_of_back_queue):
            self.back_queue.append(Queue(maxsize=50))
        intialization_of_time_stamp()

    def add_seed_URLs(self, urls_list=[]):
        for i in range(len(urls_list)):
            priority = prioritizer(urls_list[i], len(self.front_queue))
            self.front_queue[priority].put(urls_list[i])

    def add_url_in_front_queue(self, url):
        priority = prioritizer(url, len(self.front_queue))
        self.front_queue[priority].put(url)

    def is_empty_back_queue(self):
        counter = 0
        for i in self.back_queue:
            if i.qsize() == 0:
                return counter
            counter = counter + 1
        return -1

    def match_domain(self, url):
        for i in range(len(self.back_queue)):
            if self.back_queue[i].qsize() > 0:
                temp_url = self.back_queue[i].get()
                domain_of_back_queue_selected = urlparse(temp_url).netloc
                self.back_queue[i].put(temp_url)
                for j in range(self.back_queue[i].qsize() - 1):
                    temp_url = self.back_queue[i].get()
                    self.back_queue[i].put(temp_url)

                if domain_of_back_queue_selected == urlparse(url).netloc:
                    return i

        return -1

    def add_url_back_queue_first_time(self):
        while self.is_empty_back_queue() != -1:
            index_of_selected_element = tournament_selection(len(self.front_queue))
            if self.front_queue[index_of_selected_element].qsize() > 0:
                url = self.front_queue[index_of_selected_element].get()
                if self.match_domain(url) != -1:
                    if self.back_queue[self.match_domain(url)].full():
                        self.back_queue[self.match_domain(url)].put(url)
                else:
                    self.back_queue[self.is_empty_back_queue()].put(url)

    def add_url_back_queue(self):
        if self.is_empty_back_queue() != -1:
            index_of_selected_element = tournament_selection(len(self.front_queue))
            if self.front_queue[index_of_selected_element].qsize() > 0:
                url = self.front_queue[index_of_selected_element].get()
                if self.match_domain(url) != -1:
                    if self.back_queue[self.match_domain(self, url)].full():
                        self.back_queue[self.match_domain(self, url)].put(url)
                else:
                    self.back_queue[self.is_empty_back_queue()].put(url)

    def select_url_from_back_queue(self):
        index = get_min_time_stamp()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if TIME_STAMP[index] > current_time:
            time.sleep(TIME_STAMP[index] - current_time)
        url = self.back_queue[index].get()
        TIME_STAMP[index] = TIME_STAMP[index] + 15
        return url