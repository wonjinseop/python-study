
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time as t
from datetime import datetime
import codecs
from bs4 import BeautifulSoup

'''
# 순위
# 가수명
# 앨범명
# 노래 제목

멜론일간차트순위_2024년_5월_31일_11시기준.txt
'''

d = datetime.today()

file_path = f'C:/myWorkSpace/upload/멜론일간차트순위_{d.year}_{d.month}_{d.day}_{d.hour}시기준.txt'

# 셀레늄 사용 중 브라우저 꺼짐 현상 방지 옵션
option = webdriver.ChromeOptions()
option.add_experimental_option('detach', True)

# 크롬 드라이버를 별도로 설치하지 않고 버전에 맞는 드라이버를 사용하게 해 주는 코드
service = webdriver.ChromeService(ChromeDriverManager().install())

# 크롬 드라이버를 활용하여 웹 브라우저를 제어할 수 있는 객체를 리턴
driver = webdriver.Chrome(options=option, service=service)

# 멜론 홈페이지 이동
driver.get('https://www.melon.com/chart/index.htm')

t.sleep(2)

with codecs.open(file_path, mode='w', encoding='utf-8') as f:
    src = driver.page_source

    soup = BeautifulSoup(src, 'html.parser')

    rank = 1

    tr_list = soup.select('tr.lst50') + soup.select('tr.lst100')

    for tr in tr_list:
        div_list = tr.select('div.ellipsis')

        title = div_list[0].select_one('a').text.strip()
        artist = div_list[1].select_one('a').text.strip()
        album = div_list[2].select_one('a').text.strip()

        f.write(f'\n# 순위: {rank}위\n')
        f.write(f'# 가수: {artist}\n')
        f.write(f'# 앨범명: {album}\n')
        f.write(f'# 제목: {title}\n')
        f.write('\n' + ('-' * 40)+'\n')
        rank += 1
    del soup

    # for cnt in [50, 100]:

    #     # 곡 정보가 있는 tr 리스트를 지목해서 얻어오자 (lst50, lst100으로 나누어져 있음.)
    #     song_tr_list = soup.select(f'.lst{cnt}')

    #     for song_tr in song_tr_list:

    #         # 순위 찾기
    #         rank = song_tr.select_one('div.wrap.t_center').text.strip()
    #         print(rank)

    #         # 가수 이름 찾기
    #         artist_name = song_tr.select_one('div.wrap div.ellipsis.rank02 > a').text.strip()
    #         print(artist_name)

    #         # 앨범명 찾기
    #         album_name = song_tr.select_one('div.wrap div.ellipsis.rank03 > a').text.strip()
    #         print(album_name)

    #         # 노래명 찾기
    #         song_name = song_tr.select_one('div.wrap div.ellipsis.rank01 > span > a').text.strip()
    #         print(song_name)

    #         print('=' * 40)

    #         f.write(f'# 순위: {rank}\n')
    #         f.write(f'# 가수명: {artist_name}\n')
    #         f.write(f'# 앨범명: {album_name}\n')
    #         f.write(f'# 노래 제목: {song_name}\n')
    #         f.write('-' * 40 + '\n')

driver.close()