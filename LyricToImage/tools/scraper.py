import requests
import json
import logging
import sys
import time
import re
import random
import pandas as pd
import os

from pathlib import Path

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
        headers = {"content-type" : "text/html;charset=UTF-8", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}
        # 200코드일때 작업하도록
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
            # res1 = requests.get(f"https://www.melon.com/song/lyrics.htm?songId={songid}", headers=headers)
            res1 = requests.get(f"https://www.melon.com/song/detail.htm?songId={songid}", headers=headers)
            soup1 = bs(res1.content, "html.parser", from_encoding='utf-8')
            with open(f'../assets/data/stage1/scrapper/melon/top100/{genre}/melon_scrap_{time.strftime("%Y-%m-%d_%H%M%S", time.localtime())}_{genre}_{rank + 1:03d}_of_top100.html', 'w', encoding='utf-8') as file:
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
        headers = {"content-type" : "text/html;charset=UTF-8", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}
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
            with open(f'../assets/data/stage1/scrapper/genie/top100/{genre}/genie_scrap_{time.strftime("%Y-%m-%d_%H%M%S", time.localtime())}_{genre}_{rank + 1:03d}_of_top100.html', 'w', encoding='utf-8') as file:
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
        headers = {"content-type" : "text/html;charset=UTF-8", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}
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
            with open(f'../assets/data/stage1/scrapper/bugs/top100/{genre}/bugs_scrap_{time.strftime("%Y-%m-%d_%H%M%S", time.localtime())}_{genre}_{rank + 1:03d}_of_top100.html', 'w', encoding='utf-8' ) as file:
                file.write(soup1.prettify())            
            
            sleep1 = random.random() + 1
            time.sleep(sleep1)
            
            sleep_time += sleep1
    
    return sleep_time    

@process_time
def melon_parser():
    # top 100 페이지 전처리

    current_folder = Path.cwd() # 현재 폴더
    parent_folder = current_folder.parent # 상위 폴더 이동
    melon_folder = os.path.join(str(parent_folder) + '\\assets\data\stage1\scrapper\melon') # 크롤링한 Html 폴더 이동
    Path(f'{melon_folder}\\result').mkdir(parents=True, exist_ok=True) # 결과 폴더 생성

    ranking_data_html = os.listdir(melon_folder)[:-1] # result 폴더 제외한 html파일

    for genre_rank_html in ranking_data_html: # 장르별 html파일 처리
        if genre_rank_html.find(".html") != -1: # html 파일만 처리
            
            # csv 파일명 포매팅
            file_name = re.search(r'\d{4}-\d{2}-\d{2}', genre_rank_html).group() # 날짜부분 추출
            genre_name = re.search(r'([a-zA-Z&]+)\.html$', genre_rank_html).group(1) # 장르부분 추출
            with open(f'{melon_folder}\{genre_rank_html}', 'r') as file:
                soup = bs(file, 'html.parser')
                top100 = soup.find_all("tr", {"class": "lst50"}) + soup.find_all("tr", {"class": "lst100"}) # 100위까지 정보 합침
                             
                with open(f'{melon_folder}\\result\{file_name}_{genre_name}.csv', 'w') as f:
                    f.write("genre,rank,songid,songname,artistid,artistname,albumid,albumname\n")
                    for row in top100:
                        rank = row.find("span", {"class": "rank"}).text.strip()
                        songid = row.attrs['data-song-no']
                        songname = f'\"{row.find("div", {"class": "ellipsis rank01"}).text.strip()}\"'
                        artistid = re.sub(r'[^0-9]', '', row.find("div", {"class": "ellipsis rank02"}).find("a").attrs['href'])
                        artistname = row.find("div", {"class": "ellipsis rank02"}).find("a").text.strip()
                        albumid = re.sub(r'[^0-9]', '', row.find("div", {"class": "ellipsis rank03"}).find("a").attrs['href'])
                        albumname = f'\"{row.find("div", {"class": "ellipsis rank03"}).text.strip()}\"'
                        f.write(f'{genre_name},{rank},{songid},{songname},{artistid},{artistname},{albumid},{albumname}\n')
                  
    # top 100에 등록된 곡 상세정보 전처리

    top100_folder_path = os.path.join(melon_folder) + '\\top100' # c:\Users\Harvey\Desktop\Codes\Python\NLP\LyricToImage\assets\data\stage1\scrapper\melon\top100
    top100_folders = os.listdir(top100_folder_path) # ['ballad', 'dance', 'ost', 'pop', 'rap&hiphop', 'trot']


    for genre_folder in top100_folders: # 장르별 처리
        song_data_htmls = os.listdir(os.path.join(top100_folder_path) + f"\{genre_folder}") # Html 파일 검색

        with open(f'{melon_folder}\\result\{file_name}_{genre_folder}_songdata.csv', 'w') as f:
            # f.write("genre,songid,songname,artistid,artistname,albumid,albumname,release,flac,lyric,lyricist,composer,arranger\n")
            f.write("genre,songid,songname,artistid,artistname,albumid,albumname,release,flac,lyric\n")
            for song_data_html in song_data_htmls: # Html 파일별 처리
                song_data_path = os.path.join(top100_folder_path + f'\{genre_folder}\{song_data_html}')

                # Html 문서 읽기
                with open(song_data_path, 'r') as file:
                    d_soup = bs(file, 'html.parser')
                    # 음악 id
                    d_songid = d_soup.find("button", {"class": "button_etc like type02"}).attrs['data-song-no'] 
                    
                    # 제목
                    d_songname_tag = d_soup.find("div", {"class": "song_name"})
                    strong_tag = d_songname_tag.find("strong")
                    strong_tag.decompose()
                    d_songname = f'\"{d_songname_tag.text.strip()}\"'
        
                    # 아티스트 id, 이름
                    d_artistid_n_name = d_soup.find("a", {"class": "artist_name"}).attrs 
                    d_artistid = re.sub(r'[^0-9]', '', d_artistid_n_name['href']) 
                    d_artistname = f'\"{d_artistid_n_name["title"]}\"'
                    
                    # 앨범 id, 앨범 제목, 발매일, 장르, FLAC 정보
                    metadata = d_soup.find("dl", {"class": "list"}).find_all("dd")
                    datum = []
                    for idx, data in enumerate(metadata):
                        if idx == 0:
                            a_id = data.find("a").attrs['href']
                            a_id = re.sub(r'[^0-9]', '', a_id)
                            datum.append(a_id)
                        datum.append(data.text.strip())    
                    d_albumid, d_albumname, d_releasedate, d_genre  = datum[0], f'\"{datum[1]}\"', datum[2], f'\"{datum[3]}\"'
                    if len(datum) == 5:
                        d_flactype = datum[4]
                    else:
                        d_flactype = ""
                    # print(*datum)
                    
                    # 가사 정보
                    try:
                        lyric = d_soup.find("div", {"class": "lyric"}).text.replace("\n", " ").strip()
                        lyric = lyric.replace(",", "").strip()
                        lyric = re.sub(r"\s+", " ", lyric)
                    except:
                        lyric = ""
                    lyric = f'\"{lyric}\"'
                    
                    # # 작사가, 작곡가, 편곡가 정보
                    # l_c_a_data = []
                    # l_c_a_s = d_soup.find("ul", {"class": "list_person clfix"}).find_all("li")
                    # for l_c_a in l_c_a_s:
                    #     l_c_a_data.append(l_c_a.find("div", {"class": "ellipsis artist"}).text.strip())
                    
                    # d_lyricist, d_composer = l_c_a_data[0], l_c_a_data[1]
                    # if len(l_c_a_data) == 3:
                    #     d_arranger = l_c_a_data[2]
                    # else:
                    #     d_arranger = ""
                        
                f.write(f"{d_genre},{d_songid},{d_songname},{d_artistid},{d_artistname},{d_albumid},{d_albumname},{d_releasedate},{d_flactype},{lyric}\n")
                # f.write(f"{d_genre},{d_songid},{d_songname},{d_artistid},{d_artistname},{d_albumid},{d_albumname},{d_releasedate},{d_flactype},{lyric},{d_lyricist},{d_composer},{d_arranger}\n")

@process_time
def genie_parser():
    current_folder = Path.cwd() # 현재 폴더
    parent_folder = current_folder.parent # 상위 폴더 이동
    genie_folder = os.path.join(str(parent_folder) + '\\assets\data\stage1\scrapper\genie') # 크롤링한 Html 폴더 이동
    Path(f'{genie_folder}\\result').mkdir(parents=True, exist_ok=True) # 결과 폴더 생성

    ranking_data_html_origin = os.listdir(genie_folder) # result 폴더 제외한 html파일
    ranking_data_html = []
    for i in range(0, len(ranking_data_html_origin), 2):
        ranking_data_html.append(ranking_data_html_origin[i:i+2])
  
    for genre_rank_htmls in ranking_data_html[:-1]: # 장르별 html파일 처리
        # csv 파일명 포매팅
        file_name = re.search(r'\d{4}-\d{2}-\d{2}', genre_rank_htmls[0]).group() # 날짜부분 추출
        genre_name = re.search(r'([a-zA-Z&]+)_page([0-9])\.html$', genre_rank_htmls[0]).group(1) # 장르부분 추출
        
        with open(f'{genie_folder}\\result\{file_name}_{genre_name}.csv', 'w') as f:
            f.write(f'genre,rank,songid,songname,artistid,artistname,albumid,albumname\n')
            for genre_rank_html in genre_rank_htmls:
                if genre_rank_html.find(".html") != -1: # html 파일만 처리                
                    with open(f'{genie_folder}\{genre_rank_html}', 'r') as file:
                        soups = bs(file, 'html.parser').find_all("tr", {"class": "list"})
                        for soup in soups:
                            rank_tag = soup.find("td", {"class": "number"})
                            # 내부 공백 제거
                            span_tag = rank_tag.find("span", {"class": "rank"})
                            span_tag.decompose()
                            rank = f'{rank_tag.text.strip()}'
                            
                            songid = soup.attrs['songid']
                            songname = soup.find("a", {"class": "title ellipsis"}).text.strip()
                            # 19 금 글자 제거
                            songname = re.sub(r"\s+", " ", songname).replace("19 금 ", "")
                            artistid = re.sub(r'[^0-9]', '', soup.find("a", {"class": "artist ellipsis"}).attrs['ontouchend'])
                            artistname = soup.find("a", {"class": "artist ellipsis"}).text.strip()
                            albumid = re.sub(r'[^0-9]', '', soup.find("a", {"class": "albumtitle ellipsis"}).attrs['ontouchend'])
                            albumname = soup.find("a", {"class": "albumtitle ellipsis"}).text.strip()
                            
                            # 음악 제목이나 앨범제목에 콤마가 들어간 경우 ""로 감싸서 하나의 문자열로 입력
                            f.write(f"{genre_name},{rank},{songid},\"{songname}\",{artistid},{artistname},{albumid},\"{albumname}\"\n")
    
    # top 100에 등록된 곡 상세정보 전처리

    top100_folder_path = os.path.join(genie_folder) + '\\top100' # c:\Users\Harvey\Desktop\Codes\Python\NLP\LyricToImage\assets\data\stage1\scrapper\genie\top100
    top100_folders = os.listdir(top100_folder_path) # ['kpop', 'ost', 'pop', 'trot']

    for genre_folder in top100_folders: # 장르별 처리
        song_data_htmls = os.listdir(os.path.join(top100_folder_path) + f"\{genre_folder}") # Html 파일 검색
        with open(f'{genie_folder}\\result\{file_name}_{genre_folder}_songdata.csv', 'w') as f:
            # f.write("genre,songid,songname,artistid,artistname,albumid,albumname,release,flac,lyric,lyricist,composer,arranger\n")
            f.write("genre,songid,songname,artistid,artistname,albumid,albumname,playtime,playcnt,listencnt,likecnt,lyric\n")
            for song_data_html in song_data_htmls: # Html 파일별 처리
                song_data_path = os.path.join(top100_folder_path + f'\{genre_folder}\{song_data_html}')
                
                # Html 문서 읽기
                with open(song_data_path, 'r') as file:
                    d_soup_org = bs(file, 'html.parser')
                    d_soup = d_soup_org.find("div", {"class": "song-main-infos"})
                    d_songid = d_soup_org.find("p", {"class": "song-button-zone"}).find_all("a")[1].attrs['songid']
                    d_songname = d_soup.find("h2", {"class": "name"}).text.strip()
                    d_songname = re.sub(r"\s+", " ", d_songname).replace("19금 ", "")
                    info_data = d_soup.find("ul", {"class": "info-data"}).find_all("span", {"class": "value"})
                    info_list = [] #아티스트, 앨범명, 장르, 재생시간, 작사가, 작곡가, 편곡자
                    for idx, data in enumerate(info_data):
                        if idx == 0:
                            d_artistid = re.sub(r'[^0-9]', '', data.find('a').attrs['onclick'])
                        elif idx == 1:
                            d_albumid = re.sub(r'[^0-9]', '', data.find('a').attrs['onclick']) 
                        info_list.append(data.text.strip().replace("\n", "").replace(" ", ""))
                    
                    play_listen = d_soup.find("div", {"class": "total"}).find_all("p")
                    playcnt = int(play_listen[0].text.replace(",", "").strip())
                    listencnt = int(play_listen[1].text.replace(",", "").strip())
                    likecnt = int(d_soup.find("em", {"id": "emLikeCount"}).text.replace(",", "").strip())
                    try:
                        lyric = d_soup_org.find("pre", {"id": "pLyrics"}).find("p").text.replace("\n", "").replace(",", "").strip()
                    except:
                        lyric = "성인 이용자만 볼 수 있는 가사입니다."
                        
                    f.write(f'\"{info_list[2]}\",{d_songid},\"{d_songname}\",{d_artistid},{info_list[0]},{d_albumid},\"{info_list[1]}\",{info_list[3]},{playcnt},{listencnt},{likecnt},\"{lyric}\"\n')
@process_time                    
def bugs_parser():
    # top 100 페이지 전처리

    current_folder = Path.cwd() # 현재 폴더
    parent_folder = current_folder.parent # 상위 폴더 이동
    bugs_folder = os.path.join(str(parent_folder) + '\\assets\data\stage1\scrapper\\bugs') # 크롤링한 Html 폴더 이동
    Path(f'{bugs_folder}\\result').mkdir(parents=True, exist_ok=True) # 결과 폴더 생성

    ranking_data_html = os.listdir(bugs_folder)[:-1] # result 폴더 제외한 html파일
    for genre_rank_html in ranking_data_html: # 장르별 html파일 처리
        if genre_rank_html.find(".html") != -1: # html 파일만 처리

            # csv 파일명 포매팅
            file_name = re.search(r'\d{4}-\d{2}-\d{2}', genre_rank_html).group() # 날짜부분 추출
            genre_name = re.search(r'([a-zA-Z&]+)\.html$', genre_rank_html).group(1) # 장르부분 추출
            with open(f'{bugs_folder}\\result\{file_name}_{genre_name}.csv', 'w') as f:
                f.write("genre,rank,songid,songname,artistid,artistname,albumid,albumname\n")
                with open(f'{bugs_folder}\{genre_rank_html}', 'r') as file:
                    soup = bs(file, 'html.parser')
                    top100 = soup.find("tbody").find_all("tr")
                    
                    for row in top100:
                        rank = row.find("div", {"class": "ranking"}).find("strong").text.strip()
                        songid = row.attrs['trackid']
                        songname = row.find("th", {"scope": "row"}).find("a").attrs['title']
                        artistid = row.attrs['artistid']
                        artistname = row.find_all("td", {"class": "left"})[0].find("a").attrs['title']
                        albumid = row.attrs['albumid']
                        albumname = row.find_all("td", {"class": "left"})[1].find("a").attrs['title']
                        f.write(f'{genre_name},{rank},{songid},{songname},{artistid},{artistname},{albumid},{albumname}\n')

    # top 100에 등록된 곡 상세정보 전처리

    top100_folder_path = os.path.join(bugs_folder) + '\\top100' 
    top100_folders = os.listdir(top100_folder_path) # ['ballad', 'dance', 'ost', 'pop', 'rap&hiphop', 'trot']                  
                                
    for genre_folder in top100_folders: # 장르별 처리
        song_data_htmls = os.listdir(os.path.join(top100_folder_path) + f"\{genre_folder}") # Html 파일 검색
        
        with open(f'{bugs_folder}\\result\{file_name}_{genre_folder}_songdata.csv', 'w') as f:
            f.write("genre,songid,songname,artistid,artistname,albumid,albumname,playtime,likecnt,flac,lyric\n")
            for song_data_html in song_data_htmls:
                song_data_path = os.path.join(top100_folder_path + f'\{genre_folder}\{song_data_html}')
                with open(song_data_path, 'r') as file:
                    soup = bs(file, 'html.parser')
                    songid = soup.find("section", {"class": "commentsCommon sectionPadding"}).attrs['cmt_target_id']
                    songname = soup.find("article").find("header").find("h1").text.strip()
                    artistid = re.search(r'/artist/(\d+)\?', soup.find("tbody").find("td").find("a").attrs["href"]).group(1)
                    albumid = re.search(r'/album/(\d+)\?', soup.find("li", {"class": "big"}).find("a").attrs["href"]).group(1)
                    meta_data = soup.find("tbody").find_all("td")
                    
                    
                    # print(artistname, songname)              
                    if len(meta_data) == 3:
                        artistname = re.sub(r"\s+", " ", meta_data[0].text.replace("\n", "").replace("CONNECT 아티스트", "").strip())
                        albumname = re.sub(r"\s+", " ", meta_data[2].text.replace(",", "").strip())
                        playtime = re.sub(r"\s+", " ", meta_data[-1].text.replace("\n", "").strip())
                    elif len(meta_data) == 4:
                        artistname = re.sub(r"\s+", " ", meta_data[0].text.replace("\n", "").replace("CONNECT 아티스트", "").strip())
                        if "작곡" in meta_data[1].text or "보컬" in meta_data[1].text: # 참여 정보가 있는 경우
                            albumname = re.sub(r"\s+", " ", meta_data[len(meta_data)-2].text.strip())
                            playtime = re.sub(r"\s+", " ", meta_data[len(meta_data)-1].text.replace("\n", "").strip())
                        else:
                            albumname = re.sub(r"\s+", " ", meta_data[len(meta_data)-3].text.strip())
                            playtime = re.sub(r"\s+", " ", meta_data[len(meta_data)-2].text.replace("\n", "").strip())
                    else:
                        artistname = re.sub(r"\s+", " ", meta_data[0].text.replace("\n", "").replace("CONNECT 아티스트", "").strip())
                        albumname = re.sub(r"\s+", " ", meta_data[len(meta_data)-3].text.strip())
                        playtime = re.sub(r"\s+", " ", meta_data[len(meta_data)-2].text.replace("\n", "").strip())
                        
                        
                    try:
                        flac = re.search(r"FLAC 16bit(?:, 24bit)?", meta_data[-1].text.replace("\n", "").strip()).group()
                    except:
                        flac = ""
                    try:
                        lyric = re.sub(r"\s+", " ", soup.find("xmp").text.replace("\n", " ").replace(",", " ").strip())
                    except:
                        lyric = ""
                    likecnt = int(soup.find("em").text.replace(",", "").strip())
                    f.write(f'{genre_folder},{songid},\"{songname}\",{artistid},\"{artistname}\",{albumid},\"{albumname}\",{playtime},{likecnt},\"{flac}\",\"{lyric}\"\n')
                    
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
        
def parse_data(logger):
    try:
        logger.info('-'*150)
        melon_parser()
        genie_parser()
        bugs_parser()
        logger.info('-'*150)
    except:
        log_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
        logger.exception(f"{sys._getframe().f_code.co_name} function at {log_time_str}")
        logger.info('-'*150)  
                  
if __name__ == "__main__":
    logger = logging.getLogger("scraper.py")
    logging.basicConfig(filename='logging_test.log', filemode='a', level=logging.INFO, encoding='utf-8')
    scrap_data(logger)
    parse_data(logger)
    
    