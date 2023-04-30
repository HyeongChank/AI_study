import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# 데이터 로드

df = pd.read_csv('samsung.csv')

# 날짜 인덱스 설정
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# 데이터 전처리
scaler = MinMaxScaler()
data = scaler.fit_transform(df[['Close']])
def create_dataset(dataset, look_back):
    X, Y = [], []
    print(dataset)
    print(dataset.size)
    print(dataset.shape)
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:(i + look_back), 0])
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

# 학습 데이터, 테스트 데이터 분리
start_date = '2022-05-01'
end_date = '2022-05-10'
look_back = 5

train_size = int(len(data) * 0.8)
train = data[:train_size, :]
test = data[train_size - look_back:, :]

# 데이터셋 생성
train_X, train_Y = create_dataset(train, look_back)
test_X, test_Y = create_dataset(test, look_back)

# LSTM 모델 구성
model = Sequential()
model.add(LSTM(128, input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# 모델 학습
model.fit(train_X, train_Y, epochs=20, batch_size=32, verbose=2)

# 예측 결과
test_input = np.array([test[-look_back:, 0]])
test_input = np.reshape(test_input, (test_input.shape[0], test_input.shape[1], 1))

preds = []
for i in range(10):
    pred = model.predict(test_input)[0][0]
    preds.append(pred)
    test_input = np.append(test_input[:, 1:, :], [[pred]], axis=1)

preds = scaler.inverse_transform(np.array(preds).reshape(-1, 1))
print(preds)