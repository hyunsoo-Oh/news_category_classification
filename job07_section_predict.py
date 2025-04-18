import pickle
import pandas as pd
import numpy as np
from keras.utils import to_categorical
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import re

from job01_crawling_headline import df_titles

df = pd.read_csv('./crawling_data/naver_sections_news_20250418.csv')
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(df.head())
df.info()
print(df.category.value_counts())

X = df.titles
Y = df.category

with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)

label = encoder.classes_
print(label)

labeled_y = encoder.transform(Y)
onehot_y = to_categorical(labeled_y)
print(onehot_y)

okt = Okt()
for i in range(len(X)):
    X[i] = re.sub('[^가-힣]', ' ', X[i])
    X[i] = okt.morphs(X[i], stem=True)
print(X)

for idx, sentence in enumerate(X):
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    X[idx] = ' '.join(words)
print(X[:10])

with open('./models/token_max_25.pickle', 'rb') as f:
    token = pickle.load(f)
tokened_x = token.texts_to_sequences(X)
print(tokened_x[:10])

for i in range(len(tokened_x)):
    if len(tokened_x[i]) > 25:
        tokened_x[i] = tokened_x[i][:25]

x_pad = pad_sequences(tokened_x, 25)
print(x_pad[:10])

model = load_model('./models/news_section_classification_model_0.7318723201751709.h5')
preds = model.predict(x_pad)
print(preds[:10])

predict_section = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predict_section.append([most, second])
print(predict_section[:10])

df['predict'] = predict_section
print(df[['category', 'predict']].head(30))  # 상위 30개 데이터 출력

score = model.evaluate(x_pad, onehot_y)
print(score[1])

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] == df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 1
print(df.OX.mean())