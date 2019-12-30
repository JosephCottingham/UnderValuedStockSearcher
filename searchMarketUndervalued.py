import traceback
import time
import pandas as pd
import requests
from datetime import datetime
import math

url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/AAPL'
x = requests.get(url)
y = str(x.content)
print()



def dataScrap(ticker):
    urlEPS = 'https://financialmodelingprep.com/api/v3/financials/income-statement/' + ticker
    urlShareholdersEquity = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/' + ticker
    urlShares = 'https://financialmodelingprep.com/api/v3/company/profile/' + ticker

    byteDataIncome = requests.get(urlEPS)
    byteDataShareholdersEquity = requests.get(urlShareholdersEquity)
    byteDataShares = requests.get(urlShares)

    dataIncome = str(byteDataIncome.content)
    dataBalance = str(byteDataShareholdersEquity.content)
    DataShares = str(byteDataShares.content)

    if len(dataIncome) > 10 and len(dataBalance) > 10 and len(DataShares) > 10:
        startLocationEPS = dataIncome.find("EPS Diluted") + 16
        endLocationEPS = dataIncome.find('",', startLocationEPS)
        EPS = dataIncome[startLocationEPS:endLocationEPS]

        startLocationIncomeDate = dataIncome.find("date") + 9
        endLocationIncomeDate = dataIncome.find('",', startLocationIncomeDate)
        if endLocationIncomeDate - startLocationIncomeDate < 8:
            incomeDate = datetime.strptime(dataIncome[startLocationIncomeDate:endLocationIncomeDate], "%Y-%m")
        else:
            incomeDate = datetime.strptime(dataIncome[startLocationIncomeDate:endLocationIncomeDate], "%Y-%m-%d")

        startLocationBalanceDate = dataBalance.find("date") + 9
        endLocationBalanceDate = dataBalance.find('",', startLocationBalanceDate)
        if endLocationBalanceDate - startLocationBalanceDate < 8:
            balanceDate = datetime.strptime(dataBalance[startLocationBalanceDate:endLocationBalanceDate], "%Y-%m")
        else:
            balanceDate = datetime.strptime(dataBalance[startLocationBalanceDate:endLocationBalanceDate], "%Y-%m-%d")

        startLocationShareholdersEquity = dataBalance.find("Total shareholders equity") + 30
        endLocationShareholdersEquity = dataBalance.find('",', startLocationShareholdersEquity)
        ShareholdersEquity = dataBalance[startLocationShareholdersEquity:endLocationShareholdersEquity]

        startLocationPrice = DataShares.find("price") + 9
        endLocationPrice = DataShares.find(',', startLocationPrice)
        price = str(DataShares[startLocationPrice:endLocationPrice])

        startLocationCompany = DataShares.find("companyName") + 16
        endLocationCompany = DataShares.find('",', startLocationCompany)
        company = DataShares[startLocationCompany:endLocationCompany]

        startLocationDividend = dataIncome.find("Dividend per Share") + 23
        endLocationDividend = dataIncome.find('",', startLocationDividend)
        if dataIncome[startLocationDividend:endLocationDividend] != "":
            dividend = 100 * (float(dataIncome[startLocationDividend:endLocationDividend]) / float(price))
        else:
            dividend = 0

        startLocationMarketcap = DataShares.find("mktCap") + 11
        endLocationMarketcap = DataShares.find('",', startLocationMarketcap)
        Marketcap = DataShares[startLocationMarketcap:endLocationMarketcap]

        return EPS, ShareholdersEquity, price, Marketcap, dividend, incomeDate, balanceDate, company
    else:
        return '', '', '', '', '', datetime.strptime('1941-07-09', "%Y-%m-%d"), datetime.strptime('1941-07-09', "%Y-%m-%d"), ''

def run(args):
    abcSpace = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    EPS = {}
    ShareholdersEquity = {}
    cutOffDate = datetime.strptime(args['dataDate'][0], "%Y-%m-%d")
    header = True
    tickersChecked = 0
    tickersAdded = 0
    for i in abc:
        for j in abcSpace:
            for x in abcSpace:
                for y in abcSpace:
                    ticker = i + j + x + y
                    now = datetime.now()
                    tickersChecked += 1
                    print('\n***********************************\n*******\tTesting Ticker ' + ticker + '\t*******\n*******\t' + now.strftime("%d/%m/%Y %H:%M:%S") + '\t*******\n*******\tCheck #' + str(tickersChecked) + '\t\t*******\n***********************************\n')
                    try:
                        tempEPS, tempShareholdersEquity, tempPrice, tempMarketcap, dividend, incomeDate, balanceDate, company = dataScrap(ticker)
                        if (incomeDate > cutOffDate and balanceDate > cutOffDate) and tempEPS != '' and tempShareholdersEquity != '' and tempPrice != '' and tempMarketcap != '' and dividend != '' and float(tempEPS) >= 0 and dividend >= args['dividend'][0]:
                            EPS[ticker] = tempEPS
                            ShareholdersEquity[ticker] = tempShareholdersEquity
                            print('\tCollected: ' + ticker)
                            print('\tEPS: ' + tempEPS)
                            print('\tShareholdersEquity: ' + tempShareholdersEquity)
                            print('\tprice: ' + tempPrice)
                            print('\tMarketcap: ' + tempMarketcap)
                            gNum = math.sqrt(15 * 1.5 * (float(tempEPS)) * (float(tempShareholdersEquity) / (float(tempMarketcap)/float(tempPrice))))
                            print('\tgnum: ' + str(gNum))
                            gNumPercent = 100 - (100*(float(tempPrice)/gNum))
                            print('\tgNumPercent: ' + str(gNumPercent))
                            print('\tDividend: ' + str(dividend))
                            print()
                            if gNum > float(tempPrice) and args['gNumPercent'][0] < gNumPercent:
                                tickersAdded += 1
                                print("\t****Added To File****")
                                print('\tTicker Added #' + str(tickersAdded))
                                tempRowDF = pd.DataFrame([{'gNum':gNum,
                                                           'Ticker':ticker,
                                                           'EPS':tempEPS,
                                                           'ShareholdersEquity':tempShareholdersEquity,
                                                           'Price':tempPrice,
                                                           'Marketcap':tempMarketcap,
                                                           'gNumPercent':gNumPercent,
                                                           'Dividend':dividend,
                                                           'Comapany':company,
                                                           'IncomeDate':incomeDate.strftime("%m/%d/%Y"),
                                                           'BalanceDate':balanceDate.strftime("%m/%d/%Y")}])
                                tempRowDF.to_csv(args['fileLocation'][0], mode='a', header=header)
                                header=False
                            print('***********************************')
                            time.sleep(0.001)
                    except Exception as e:
                        print('Error: ' + ticker)
                        print(str(e))
                        print(traceback.format_exc())