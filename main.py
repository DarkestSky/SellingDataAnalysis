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
    print(df)
    sumByMonth(df)
    userNumByMonth(df)
    consumptionByUser(df)
    countByUser(df)
    firstConsumeMonth(df)
    lastConsumeMonth(df)


# 每月消费额
def sumByMonth(df: pandas.DataFrame):
    sum_by_month = df.groupby(by='Month')['Total'].sum()
    print(sum_by_month)
    sum_by_month.to_csv('./data/SumByMonth.csv')
    return sum_by_month


# 每月消费人数
def userNumByMonth(df: pandas.DataFrame):
    usernums = df.groupby(by='Month')['CustomerID'].nunique()
    print(usernums)
    usernums.to_csv('./data/UserNumByMonth.csv')
    return usernums


# 各用户消费总额
def consumptionByUser(df: pandas.DataFrame):
    consumption = df.groupby(by='CustomerID')['Total'].sum()
    print(consumption)
    consumption.to_csv('./data/ConsumptionByUser.csv')
    return consumption


# 各用户消费次数
def countByUser(df: pandas.DataFrame):
    count = df.groupby(by='CustomerID').count()['Quantity']
    print(count)
    count.to_csv('./data/CountByUser.csv')
    return count


def firstConsumeMonth(df: pandas.DataFrame):
    first = df.groupby(by='CustomerID')['Month'].min().value_counts()
    print(first)
    first.to_csv('./data/FirstConsumeMonth.csv')
    return first


def lastConsumeMonth(df: pandas.DataFrame):
    last = df.groupby(by='CustomerID')['Month'].max().value_counts()
    print(last)
    last.to_csv('./data/LastConsumeMonth.csv')
    return last


if __name__ == '__main__':
    analysis()
