from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
from bs4 import BeautifulSoup

# 엑셀 처리 모듈 임포트
# pip install xlsxwriter
import xlsxwriter

# user-agent 정보를 변환해 주는 모듈 임포트
# 특정 브라우저로 크롤링을 진행할 때 차단되는 것을 방지
# pip install fake_useragent
from fake_useragent import UserAgent

# 이미지를 바이트 단위로 변환 처리 모듈
from io import BytesIO

# 요청 헤더 정보를 꺼내올 수 있는 모듈
import urllib.request as req


d = datetime.today()

file_path = f'C:/myWorkSpace/upload/알라딘 베스트셀러 1~400위_{d.year}_{d.month}_{d.day}.xlsx'

# User Agent 정보 변환 (필수는 아닙니다.)
opener = req.build_opener() # 헤더 정보를 초기화
opener.addheaders = [('User-agent', UserAgent().edge)]
req.install_opener(opener) # 새로운 헤더 정보를 삽입

# 엑셀 처리 선언
# Workbook 객체를 생성해서 액셀 파일을 하나 생성 (생성자의 매개값으로는 저장될 경로를 지정)
workbook = xlsxwriter.Workbook(file_path)

# 워크 시트  생성
worksheet = workbook.add_worksheet()

# 셀레늄 사용 중 브라우저 꺼짐 현상 방지 옵션
option = webdriver.ChromeOptions()
option.add_experimental_option('detach', True)

# 브라우저를 아예 안뜨게 하기
# option.add_argument('--headless')

# 크롬 드라이버를 별도로 설치하지 않고 버전에 맞는 드라이버를 사용하게 해 주는 코드
service = webdriver.ChromeService(ChromeDriverManager().install())

# 크롬 드라이버를 활용하여 웹 브라우저를 제어할 수 있는 객체를 리턴
driver = webdriver.Chrome(options=option, service=service)

# 페이지 이동 (베스트셀러 페이지)
driver.get('https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&start=we')

# 브라우저 내부 대기
# t.sleep(2) -> 브라우저 로딩에 상관 없이 무조건 10초 대기

# 웹 페이지 전체가 로딩될 때 까지 대기 후 렌더링이 완료 되었다면 남은 시간 무시
driver.implicitly_wait(10)

# 엑셀에 텍스트 저장 (헤더 만들기)
cell_format = workbook.add_format({'bold': True, 'font_color': 'red', 'bg_color':'yellow', 'font_size':'13'})
worksheet.write('A1', '썸네일', cell_format)
worksheet.write('B1', '제목', cell_format)
worksheet.write('C1', '작가', cell_format)
worksheet.write('D1', '출판사', cell_format)
worksheet.write('E1', '출판일', cell_format)
worksheet.write('F1', '가격', cell_format)
worksheet.write('G1', '링크', cell_format)

# selenium으로 현재 패이지의 html 소스 코드를 전부 불러오기
cur_page_num = 2 # 현재 페이지 번호
target_page_num = 9 # 목적지 페이지 번호
cnt = 2 # 엑셀 행 수를 카운트 해 줄 변수
while cur_page_num <= target_page_num:
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    div_list = soup.find_all('div', class_='ss_book_box')

    for div_ss_book_box in div_list:

        # 이미지
        img_url = div_ss_book_box.select_one('table div.cover_area div.flipcover_in > img.front_cover')
        # print(img_url)

        # 타이틀, 작가, 가격정보를 모두 포함하는 ul부터 지목
        ul = div_ss_book_box.select_one('div.ss_book_list > ul')

        # 타이틀
        title = ul.select_one('li > a.bo3')

        # 작가
        # 위에서 얻은 title의 부모요소 li의 다음 형제 li를 지목 -> 작가, 출판사, 출판일 존재
        author = title.find_parent().find_next_sibling()

        # 작가쪽 영역 데이터를 상세 분해
        author_data = author.text.split(' | ')
        author_name = author_data[0].strip()
        company = author_data[1].strip()
        pub_day = author_data[2].strip()

        # 가격
        price = author.find_next_sibling() # 작가 li 다음 형제 요소가 가격 li이다.
        price_data = price.text.split(', ')[0].strip()

        # 책 상세 정보 페이지 링크
        # title이라는 변수에 a태그를 취득 해놓은 상태.
        # title -> a태그의 요소 전부를 가지고 있는 상태.
        # href로 작성된 키를 전달하고, 해당 value를 받아 변수에 저장
        page_link = title['href']

        try:
            # 이미지 바이트 변환 처리
            # BytesIO 객체 생성. 생성자의 매개값으로 아까 준비 해놓은 img 태그의 src값을 urlopen 메서드에게 전달
            # 해당 url에 등록된 이미지를 읽어서 바이트 단위로 변환한 객체를 리턴
            img_data = BytesIO(req.urlopen(img_url['src']).read())

            # 액셀에 이미지 저장
            # worksheet.insert_image('배치할 셀 번호', 이미지 제목, {'image_data':img_data, 'x_scale':0.5, 'y_scale':0.5})
            worksheet.insert_image(f'A{cnt}', img_url['src'], {'image_data':img_data, 'x_scale':0.5, 'y_scale':0.5})

        except:
            # 파이썬에서는 블록 구조에 아무것도 작성하지 않으면 에러입니다.
            # 블록 구조 내부에 딱히 작성할 코드가 없어서 넘길 때
            # pass라는 키워드를 사용합니다.
            pass

        # 엑셀에 나머지 텍스트 저장
        worksheet.write(f'B{cnt}', title.text)
        worksheet.write(f'C{cnt}', author_name)
        worksheet.write(f'D{cnt}', company)
        worksheet.write(f'E{cnt}', pub_day)
        worksheet.write(f'F{cnt}', price_data)
        worksheet.write(f'G{cnt}', page_link)

        # 다음 행에 다음 데이터를 배치하기 위해 cnt값 증가
        cnt += 1

    cur_page_num += 1
    driver.find_element(By.XPATH, f'//*[@id="newbg_body"]/div[3]/ul/li[{cur_page_num}]/a').click()
    del soup
    driver.implicitly_wait(3)

driver.close()
workbook.close()