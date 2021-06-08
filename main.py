import pandas
import pandas as pd
import numpy as np
from datetime import datetime


def analysis():
    custom_date_parser = lambda x: datetime.strptime(x, "%d-%m-%Y %H:%M")
    path = r'./data/OnlineRetail.csv'
    f = open(path, 'r', encoding='utf-8')
    df = pd.read_csv(f, parse_dates=['InvoiceDate'], date_parser=custom_date_parser)
    df['Total'] = df['Quantity'] * df['UnitPrice']
    df['Month'] = df['InvoiceDate'].astype('datetime64[M]')
    print(df.info())
    sumByMonth(df)
    userNumByMonth(df)
    consumptionByUser(df)
    countByUser(df)
    firstConsumeMonth(df)
    lastConsumeMonth(df)
    applyRfm(df)


# 每月消费额
def sumByMonth(df: pandas.DataFrame):
    sum_by_month = df.groupby(by='Month')['Total'].sum()
    sum_by_month.to_csv('./data/SumByMonth.csv')
    return sum_by_month


# 每月消费人数
def userNumByMonth(df: pandas.DataFrame):
    usernums = df.groupby(by='Month')['CustomerID'].nunique()
    usernums.to_csv('./data/UserNumByMonth.csv')
    return usernums


# 各用户消费总额
def consumptionByUser(df: pandas.DataFrame):
    consumption = df.groupby(by='CustomerID')['Total'].sum()
    consumption.to_csv('./data/ConsumptionByUser.csv')
    return consumption


# 各用户消费次数
def countByUser(df: pandas.DataFrame):
    count = df.groupby(by='CustomerID').count()['Quantity']
    count.to_csv('./data/CountByUser.csv')
    return count


# 首次消费的月份
def firstConsumeMonth(df: pandas.DataFrame):
    first = df.groupby(by='CustomerID')['Month'].min().value_counts()
    first.to_csv('./data/FirstConsumeMonth.csv')
    return first


# 最后一次消费的月份
def lastConsumeMonth(df: pandas.DataFrame):
    last = df.groupby(by='CustomerID')['Month'].max().value_counts()
    last.to_csv('./data/LastConsumeMonth.csv')
    return last


# 进行用户分层
def applyRfm(df: pandas.DataFrame):
    rfm = df.pivot_table(index='CustomerID', aggfunc={'InvoiceDate': 'max', 'Quantity': 'sum', 'Total': 'sum'})
    max_date = df['InvoiceDate'].max()
    rfm['R'] = -(df.groupby(by='CustomerID')['InvoiceDate'].max() - max_date) / np.timedelta64(1, 'D')
    rfm.drop(columns=['InvoiceDate'], inplace=True)
    rfm.rename(columns={'Quantity': 'F', 'Total': 'M'}, inplace=True)
    # 生成分层标签
    rfm['Lable'] = rfm.apply(lambda x: x - x.mean()).apply(getRfmLable, axis=1)
    rfm.to_csv('./data/RFM.csv')
    return rfm


# 对用户添加分层标签
def getRfmLable(x):
    level = x.map(lambda _x: '1' if _x >= 0 else '0')
    label = level.R + level.F + level.M
    d = {
        '111': u'重要价值客户',
        '011': u'重要保持客户',
        '101': u'重要挽留客户',
        '001': u'重要发展客户',
        '110': u'一般价值客户',
        '010': u'一般保持客户',
        '100': u'一般挽留客户',
        '000': u'一般发展客户'
    }
    result = d[label]
    return result


if __name__ == '__main__':
    analysis()
