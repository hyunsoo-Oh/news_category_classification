from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time

options = ChromeOptions()

options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = 'https://news.naver.com/section/100'
driver.get(url) # 5초 동안 Browser 띄우기
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'

for i in range(15):
    time.sleep(0.5)
    driver.find_element(By.XPATH, button_xpath).click()
time.sleep(5)

# container 1칸에 6개 titles
for i in range(1, 7): # container
    for j in range(1, 7): # title
        title_path = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
        try:
            title = driver.find_element(By.XPATH, title_path).text
            print(title)
        except:
            print('error', i, j)

# # 헤드 라인
# '//*[@id="_SECTION_HEADLINE_LIST_etbjt"]/li[1]/div/div/div[2]/a/strong'
# '//*[@id="_SECTION_HEADLINE_LIST_eyxl3"]/li[1]/div/div/div[2]/a/strong'

# # section / 1 / 페이지 / n 번째 뉴스
# # 정치 섹션
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[2]/div/div/div[2]/a/strong'
# # 경제 섹션
# '//*[@id="newsct"]/div[5]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[5]/div/div[1]/div[1]/ul/li[2]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[5]/div/div[1]/div[1]/ul/li[3]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[5]/div/div[1]/div[4]/ul/li[5]/div/div/div[2]/a/strong'
# # 사회 섹션
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'