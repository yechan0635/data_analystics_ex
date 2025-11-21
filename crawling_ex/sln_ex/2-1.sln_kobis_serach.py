# 1. 필요한 라이브러리 로딩
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup as BS
import urllib.request as req
import os
import csv
from datetime import datetime
import time

# 파일저장 함수를 정의한 모듈 로딩
from my_lib import save_lib

# 2. 크롬브라우저 옵션 정의
options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("--no-sandbox")            # 샌드박스 사용 안함
options.add_argument("--disable-dev-shm-usage") # 메모리 부족 방지
options.add_argument("headless")                # 크롬 창을 안뜨게함

# 3. 크롬 웹드라이브를 통한 크롬브라우저 객체 생성
service = Service("chromedriver_142/chromedriver.exe")
chrome = webdriver.Chrome(service=service, options=options)

# 4. 데이터 수집할 웹 주소
url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"
chrome.get(url)
time.sleep(1)

# 지정한 요소가 브라우저에 로딩될때까지 기다림, 최대 10초
wait = WebDriverWait(chrome, 10)
def find(wait, css_selector):
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

# 5. 데이터 수집할 부분에 대한 검색 액션 수행
try:
    # 한국 영화만 체크
    ele = find(wait, "label[for='repNationNoKor']")
    ele.click()

    # 조회버튼 클릭
    btn = find(wait, ".wrap_btn button.btn_blue")
    btn.click()

except Exception as e:
    print("오류 발생:", e)

# -----------------------------------------
# try 블록은 여기서 끝!
# -----------------------------------------

# 조회된 데이터에서 필요한 데이터 수집
time.sleep(0.5)

items = chrome.find_elements(By.CSS_SELECTOR, "table.tbl_comm tbody tr")

print("영화제목 | 개봉일 | 예매매출액 | 예매관람수")
movie_lists = []

for item in items:
    title = item.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
    open_date = item.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
    reserve_price = item.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.rstrip("%")
    reserve_count = item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.replace(",", "")

    if not open_date:
        open_date = "-"

    # print(f"{title} | {open_date} | {reserve_price} | {reserve_count}")
    movie_lists.append([title, open_date, reserve_price, reserve_count])

print("총 수집 건수:", len(movie_lists))

time.sleep(1)

# 파일로 저장하기(csv)
# 6. 리스트 -> 파일에 저장
# 현재 날짜/시간 가져오기


# 호출부
data_keyword = "movie"
head = ["영화제목", "개봉일", "예매매출액", "예매관람수"]
save_lib.save_datas(data_keyword, head, movie_lists)

chrome.close()
chrome.quit()



