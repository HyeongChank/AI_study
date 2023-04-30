import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt


# 삼성전자 주가 데이터 가져오기
def load_data_scale(code, s_date, e_date):
    stock = yf.download(code, start=s_date, end=e_date)
    print(stock)
    print(stock.shape)
    stock = stock[['Close']]
    stock = stock.dropna()
    # 데이터 정규화 (0 ~ 1 사이의 값으로 스케일링)
    scaler = MinMaxScaler()
    stock = scaler.fit_transform(stock)
    # 학습용 데이터와 검증용 데이터 분리 (train:test = 7:3)
    train_size = int(len(stock) * 0.7)
    test_size = len(stock) - train_size
    train, test = stock[0:train_size,:], stock[train_size:len(stock),:]
    return scaler, train, test

# LSTM 입력 데이터 생성 함수
def create_dataset(dataset, look_back):
    X, Y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:(i + look_back), 0])
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

def make_model(train, test, ref_back, epoch):
    
    # 입력 데이터 생성 (look_back = 50)
    look_back = ref_back
    train_X, train_Y = create_dataset(train, look_back)
    test_X, test_Y = create_dataset(test, look_back)

    # 입력 데이터의 shape 변환 (samples, time steps, features)
    train_X = np.reshape(train_X, (train_X.shape[0], train_X.shape[1], 1))
    test_X = np.reshape(test_X, (test_X.shape[0], test_X.shape[1], 1))

    # LSTM 모델 구성
    model = Sequential()
    model.add(LSTM(128, input_shape=(look_back, 1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    # 모델 학습
    model.fit(train_X, train_Y, epochs=epoch, batch_size=32, verbose=2)

    # 예측 결과
    train_predict = model.predict(train_X)
    test_predict = model.predict(test_X)
    return train_predict, test_predict, train_Y, test_Y, train_X

def make_unscale(train_predict, test_predict, train_Y, test_Y):
    # 정규화 된 값을 다시 원래의 값으로 변환
    train_predict = scaler.inverse_transform(train_predict)
    train_Y = scaler.inverse_transform([train_Y])
    test_predict = scaler.inverse_transform(test_predict)
    test_Y = scaler.inverse_transform([test_Y])
    # 예측값
    print(train_Y)
    # 실제값
    print(test_Y)
    return train_predict, train_Y, test_predict, test_Y

def predict_to_df(train_predict, train_Y, test_predict, test_Y):
    # 예측 결과를 데이터프레임에 저장
    train_predict_df = pd.DataFrame(train_predict, columns=['train_predict'])
    train_Y_df = pd.DataFrame(train_Y[0], columns=['train_actual'])
    test_predict_df = pd.DataFrame(test_predict, columns=['test_predict'])
    test_Y_df = pd.DataFrame(test_Y[0], columns=['test_actual'])
    return train_predict_df, train_Y_df

def make_graph(train_predict_df, train_Y_df, code, s_date, e_date):
    stock_rd = yf.download(code, start=s_date, end=e_date)
    fig, (ax1, ax2) = plt.subplots(2,1)
    # Plot 1
    ax1.plot(stock_rd.index, stock_rd['Adj Close'], label='stock')
    ax1.set_title('Stock Prices')
    ax1.set_ylabel('Price')
    ax1.legend()
    # Plot 2
    ax2.plot(train_predict_df, label='train predict')
    ax2.plot(train_Y_df, label='train actual')
    ax2.legend()
    plt.show()
    
# import datetime

# def make_model2(train, test, ref_back):
    
#     # 입력 데이터 생성 (look_back = 50)
#     look_back = ref_back
#     train_X, train_Y = create_dataset(train, look_back)
#     test_X, test_Y = create_dataset(test, look_back)

#     # 입력 데이터의 shape 변환 (samples, time steps, features)
#     train_X = np.reshape(train_X, (train_X.shape[0], train_X.shape[1], 1))
#     test_X = np.reshape(test_X, (test_X.shape[0], test_X.shape[1], 1))
#     return train_X
    
# def predict_price(code, s_date, e_date, ref_back, predict_date, train_X):
#     # 데이터 가져오기
#     stock = yf.download(code, start=s_date, end=e_date)
#     stock = stock[['Close']]
#     stock = stock.dropna()

#     # 정규화 (0 ~ 1 사이의 값으로 스케일링)
#     scaler = MinMaxScaler()
#     stock_scaled = scaler.fit_transform(stock)

#     # 예측 기간 설정 (predict_date부터 look_back 일 전까지의 데이터를 사용)
#     predict_date = datetime.datetime.strptime(predict_date, '%Y-%m-%d')
#     end_date = predict_date - datetime.timedelta(days=1)
#     start_date = end_date - datetime.timedelta(days=ref_back)

#     # 예측에 사용할 데이터 추출
#     predict_data = stock_scaled[(stock.index >= start_date) & (stock.index <= end_date)]
#     predict_data = np.reshape(predict_data, (1, predict_data.shape[0], 1))

#     # 모델 생성 및 학습
#     model = Sequential()
#     model.add(LSTM(128, input_shape=(ref_back, 1)))
#     model.add(Dense(1))
#     model.compile(loss='mean_squared_error', optimizer='adam')
#     model.fit(train_X, train_Y, epochs=epoch, batch_size=32, verbose=2)

#     # 예측 결과
#     predict_scaled = model.predict(predict_data)
#     predict_price = scaler.inverse_transform(predict_scaled)[0][0]
#     return predict_price
    

if __name__=='__main__':
    s_date = '2023-03-01'
    e_date = '2023-04-30'
    # 코스닥 종목은 .KQ / 코스피 종목은 .KS
    code = '005930.KS'
    epoch = 30
    # ref_back(start 4월 1일 end 4월 30일 ref_bake 10 이면 3월 20일~ 4월 20일 까지 데이터 이용)
    ref_back = 5
    scaler, train, test = load_data_scale(code, s_date, e_date)
    train_predict, test_predict, train_Y, test_Y, train_X = make_model(train, test, ref_back, epoch)
    train_predict, train_Y, test_predict, test_Y = make_unscale(train_predict, test_predict, train_Y, test_Y)
    train_predict_df, train_Y_df = predict_to_df(train_predict, train_Y, test_predict, test_Y)
    make_graph(train_predict_df, train_Y_df, code, s_date, e_date)
    # train_X = make_model2(train, test, ref_back)
    # predict_price(code, s_date, e_date, ref_back, '2023-05-01', train_X)
  