# Data Frame : titles, category
# crawling_data : naver_sections_news_20250416.csv
# 모든 Section 3번 컨테이너 없음

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import datetime

options = ChromeOptions()

options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

categories = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
df_titles = pd.DataFrame()

# 각 섹션별로 수집
for section_id in range(6):
    url = 'https://news.naver.com/section/10{}'.format(section_id)
    driver.get(url)  # 5초 동안 Browser 띄우기
    button_xpath = '//*[@id="newsct"]/div[{}]/div/div[2]'.format(5 if section_id == 1 else 4)

    # 더보기 버튼 클릭
    click_counts = [0] * 6  # 각 섹션별 클릭 횟수 저장
    for _ in range(15):  # 최대 200번 시도
        try:
            time.sleep(0.5)
            driver.find_element(By.XPATH, button_xpath).click()
            click_counts[section_id] += 1
        except:
            break
    time.sleep(2)
    # 기사 수집 : container 1칸에 6개 titles
    titles = []
    total_articles = click_counts[section_id] * 6  # 한 번 클릭당 6개 기사 추가됨

    # 각 기사 수집
    for i in range(1, total_articles):
        for j in range(1, 7):  # 컨테이너 내 위치 (1~6)
            s = 4 if section_id != 1 else 5
            title_xpath = '//*[@id="newsct"]/div[{}]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(s, i, j)
            try:
                title = driver.find_element(By.XPATH, title_xpath).text
                titles.append(title)
                print(f"[{categories[section_id]}] {title}")
            except:
                print('error', i, j)
                if i != 3:
                    break
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = categories[section_id]
    df_titles = pd.concat([df_titles, df_section_titles],
                      axis='rows', ignore_index=True)
print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_sections_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False
)