import requests
import json
import logging
import sys
import time
import re
import random
import pandas as pd

from bs4 import BeautifulSoup as bs

def process_time(func):
    def wrapper():
        start = time.time()
        start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info(f"start scrapping {func.__name__} function at {start_time_str}")
        
        sleep_t = func()
        
        end = time.time()
        end_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info(f"end scrapping {func.__name__} funtion at {end_time_str}")
        logger.info(f"process_time : {end - start: .4f} s")
        logger.info(f"process_time without sleep : {end - start - sleep_t: .4f} s\n")
        
    return wrapper

@process_time
def scrap_melon():
    category = {"ballad": "0100", "dance": "0200", "rap&hiphop": "0300", "trot": "0700", "pop": "0900", "ost": "1500"}
    sleep_time = 0
    for genre, code in zip(category.keys(), category.values()):
        headers = {"content-type" : "application/json;charset=UTF-8", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}
        res = requests.get(f"https://www.melon.com/chart/day/index.htm?classCd=GN{code}", headers=headers)
        soup = bs(res.content, "html.parser", from_encoding='utf-8')
        with open(f'../assets/data/stage1/scrapper/melon/melon_scrap_{time.strftime("%Y-%m-%d_%H%M%S", time.localtime())}_{genre}.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        
        top50 = soup.find_all("tr", id="lst50")
        top100 = top50 + soup.find_all("tr", id="lst100")
        song_rank = []
        
        sleep = random.random() + 1
        time.sleep(sleep)
        sleep_time += sleep
        
        for song in top100:
            song_rank.append(song.attrs['data-song-no'])
        
        for rank, songid in enumerate(song_rank):
            res1 = requests.get(f"https://www.melon.com/song/detail.htm?songId={songid}", headers=headers)
            soup1 = bs(res1.content, "html.parser", from_encoding='utf-8')
            with open(f'../assets/data/stage1/scrapper/melon/top100/{genre}/melon_scrap_{time.strftime("%Y-%m-%d_%H%M%S", time.localtime())}_{genre}_{rank + 1: 03d}_of_top100.html', 'w', encoding='utf-8') as file:
                file.write(soup1.prettify())            
            
            sleep1 = random.random() + 1
            time.sleep(sleep1)
            
            sleep_time += sleep1
    
    return sleep_time

@process_time
def scrap_genie():
    category = {"kpop": "0100", "trot": "0107", "pop": "0200", "ost": "0300"}
    sleep_time = 0
    for genre, code in zip(category.keys(), category.values()):
        headers = {"content-type" : "application/json;charset=UTF-8", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}
        ymd = str(int(time.strftime("%Y%m%d")) - 1)
        
        song_rank = []
        for page in range(2): 
            res = requests.get(f"https://www.genie.co.kr/chart/genre?ditc=D&ymd={ymd}&genrecode=M{code}&pg={page+1}", headers=headers)
            soup = bs(res.content, "html.parser", from_encoding='utf-8')
            
            songid_list = soup.find_all("tr", "list")
            for song in songid_list:
                song_rank.append(song.attrs['songid'])
                
            with open(f'../assets/data/stage1/scrapper/genie/genie_scrap_{time.strftime("%Y-%m-%d_%H%M%S", time.localtime())}_{genre}_page{page+1}.html', 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
            
            sleep = random.random() + 1
            time.sleep(sleep)
            sleep_time += sleep
                    
        for rank, songid in enumerate(song_rank):
            res1 = requests.get(f"https://www.genie.co.kr/detail/songInfo?xgnm={songid}", headers=headers)
            soup1 = bs(res1.content, "html.parser", from_encoding='utf-8')
            with open(f'../assets/data/stage1/scrapper/genie/top100/{genre}/genie_scrap_{time.strftime("%Y-%m-%d_%H%M%S", time.localtime())}_{genre}_{rank + 1: 03d}_of_top100.html', 'w', encoding='utf-8') as file:
                file.write(soup1.prettify())            
            
            sleep1 = random.random() + 1
            time.sleep(sleep1)
            
            sleep_time += sleep1
    
    return sleep_time

@process_time
def scrap_bugs():
    category = {"ballad": "nb", "dance": "ndp", "rap&hiphop": "nrh", "trot": "ntrot", "pop": "nfpop", "ost": "nost"}
    sleep_time = 0
    for genre, code in zip(category.keys(), category.values()):
        headers = {"content-type" : "application/json;charset=UTF-8", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}
        ymd = str(int(time.strftime("%Y%m%d")) - 1)
        res = requests.get(f"https://music.bugs.co.kr/chart/track/day/{code}?chartdate={ymd}", headers=headers)
        soup = bs(res.content, "html.parser", from_encoding='utf-8')
        with open(f'../assets/data/stage1/scrapper/bugs/bugs_scrap_{time.strftime("%Y-%m-%d_%H%M%S", time.localtime())}_{genre}.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        
        tbody = soup.find('tbody')
        top100 = tbody.find_all('tr')
        song_rank = []
        
        sleep = random.random() + 1
        time.sleep(sleep)
        sleep_time += sleep
        
        for song in top100:
            song_rank.append(song.attrs['trackid'])
        
        for rank, songid in enumerate(song_rank):
            res1 = requests.get(f"https://music.bugs.co.kr/track/{songid}?wl_ref=list_tr_08_chart", headers=headers)
            soup1 = bs(res1.content, "html.parser", from_encoding='utf-8')
            with open(f'../assets/data/stage1/scrapper/bugs/top100/{genre}/bugs_scrap_{time.strftime("%Y-%m-%d_%H%M%S", time.localtime())}_{genre}_{rank + 1: 03d}_of_top100.html', 'w', encoding='utf-8' ) as file:
                file.write(soup1.prettify())            
            
            sleep1 = random.random() + 1
            time.sleep(sleep1)
            
            sleep_time += sleep1
    
    return sleep_time    

def scrap_data(logger):
    try:
        logger.info('-'*150)
        scrap_melon()
        scrap_genie()
        scrap_bugs()
        logger.info('-'*150)
    except:
        log_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
        logger.exception(f"{sys._getframe().f_code.co_name} function at {log_time_str}")
        logger.info('-'*150)

if __name__ == "__main__":
    logger = logging.getLogger("scraper.py")
    logging.basicConfig(filename='logging_test.log', filemode='a', level=logging.INFO, encoding='utf-8')
    scrap_data(logger)
    
    