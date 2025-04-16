from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

from unicodedata import category

categories = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
df_titles = pd.DataFrame()

for i in range(6):
    url = 'https://news.naver.com/section/10{}'.format(i) # 정치

    resp = requests.get(url)
    # print(list(resp))
    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(soup.prettify())

    title_tags = soup.select('.sa_text_strong')

    # title = title_tags[0].text
    # print(title)

    titles = []
    for tag in title_tags:
        titles.append(tag.text)
    print(titles)

    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = categories[i]
    df_titles = pd.concat([df_titles, df_section_titles],
                          axis='rows', ignore_index=True)
    print(df_section_titles.head())

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False
)