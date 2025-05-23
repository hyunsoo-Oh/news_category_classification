# 네이버 뉴스는 카테고리가 정확하지 않음
import pickle
import re
import pandas as pd
import numpy as np
from pygments.lexer import words
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt, Komoran
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 데이터 로드
# 네이버 뉴스 데이터 CSV 파일을 불러옴
# 컬럼: titles, category
df = pd.read_csv('./crawling_data/naver_sections_news_20250417.csv')

df.info()  # 데이터프레임 정보 출력
print(df.head(30))  # 상위 30개 데이터 출력
print(df.category.value_counts())  # 카테고리별 데이터 개수 출력

# 입력(X), 라벨(Y) 분리
df.titles  # 뉴스 제목 리스트
X = df.titles
Y = df.category

okt = Okt()
# # 형태소 분석 예시 (첫 번째 뉴스 제목)
# print(X[0])
# okt = Okt()
# okt_x = okt.morphs(X[0])  # OKT 형태소 분석
# print(okt_x)
# okt_x = okt.morphs(X[0], stem=True)  # OKT 형태소 분석(어간 추출)
# print(okt_x)
#
# komoran = Komoran()
# komoran_x = komoran.morphs(X[0])  # KOMORAN 형태소 분석
# print(komoran_x)

# 라벨 인코딩: 카테고리 문자열을 숫자 라벨로 변환
encoder = LabelEncoder()  # ['Culture', 'Economic', 'Politics', 'Social', 'World', 'IT']
labeled_y = encoder.fit_transform(Y)  # 카테고리 문자열을 숫자로 변환
print(labeled_y[:5])  # 인코딩된 라벨 샘플 출력

label = encoder.classes_  # 카테고리 클래스명 출력
print(label)
with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)  # 인코더 저장

# 원-핫 인코딩: 다중 클래스 분류를 위한 라벨 변환
onehot_y = to_categorical(labeled_y)
print(onehot_y)

# 전체 데이터 전처리: 한글만 남기고, 형태소 분석, 1글자 제외
for i in range(len(X)):  # 실제로는 len(X) 사용 가능
    X[i] = re.sub('[^가-힣]', ' ', X[i])  # 한글만 남기고 공백 처리
    X[i] = okt.morphs(X[i], stem=True)  # 형태소 분석
    if i % 1000 == 0:
        print(i)  # 진행상황 출력
print(X)  # 형태소 분석된 결과 출력

# 형태소 분석된 결과에서 1글자 단어 제외, 다시 문장으로 합침
for idx, sentence in enumerate(X):
    print(sentence)
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    print(words)
    X[idx] = ' '.join(words)  # 띄어쓰기 기준으로 다시 합침
print(X)

# 토크나이저 생성 및 전체 데이터에 대해 학습
# 각 단어에 고유 인덱스 부여
token = Tokenizer()
token.fit_on_texts(X)
tokened_x = token.texts_to_sequences(X)

print(tokened_x)

# 단어 집합 크기 계산 (패딩 인덱스 포함)
wordsize = len(token.word_index) + 1

# 가장 긴 문장 길이(max) 계산
max = 0
for sentence in tokened_x:
    if len(sentence) > max:
        max = len(sentence)
print(max)

# 토크나이저 객체 저장 (max값을 파일명에 포함)
with open('./models/token_max_{}.pickle'.format(max), 'wb') as f:
    pickle.dump(token, f)

# 패딩: 모든 시퀀스를 max 길이에 맞춰 0으로 채움
x_pad = pad_sequences(tokened_x, max)
print(x_pad)

# 학습/테스트 데이터 분리
x_train, x_test, y_train, y_test = train_test_split(x_pad, onehot_y, test_size=0.2)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

# 전처리된 데이터를 npy 파일로 저장
np.save('./crawling_data/title_x_train_wordsize{}.npy'.format(wordsize), x_train)
np.save('./crawling_data/title_x_test_wordsize{}.npy'.format(wordsize), x_test)
np.save('./crawling_data/title_y_train_wordsize{}.npy'.format(wordsize), y_train)
np.save('./crawling_data/title_y_test_wordsize{}.npy'.format(wordsize), y_test)