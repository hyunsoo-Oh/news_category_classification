import pandas as pd
import glob

# df1 = pd.read_csv('./crawling_data/naver_sections_news_politics.csv')
# df2 = pd.read_csv('./crawling_data/naver_sections_news_economic.csv')
# df3 = pd.read_csv('./crawling_data/naver_sections_news_social.csv')
# df4 = pd.read_csv('./crawling_data/naver_sections_news_culture.csv')
# df5 = pd.read_csv('./crawling_data/naver_sections_news_world.csv')
# df6 = pd.read_csv('./crawling_data/naver_sections_news_it.csv')
#
# df = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index=True)
# df.to_csv('./crawling_data/naver_sections_news_total.csv', index=False)

###############
data_dir = './crawling_data/'
data_path = glob.glob(data_dir + 'naver_sections_news_*.csv') # *.*
df = pd.DataFrame()
for path in data_path:
    df_section = pd.read_csv(path)
    df = pd.concat([df, pd.read_csv(path)], ignore_index=True)
df.info()
print(df.head())
df.to_csv('./crawling_data/naver_sections_news_total.csv', index=False)