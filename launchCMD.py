import searchMarketUndervalued
import pandas as pd

if __name__ == '__main__':
    rerun = 'Y'
    while rerun == 'y' or rerun == 'Y':
        args = pd.DataFrame([{'gNumPercent':float(input('Percent difference between gNum and price (greater means more undervalued)(0-100): ')),
                              'fileLocation':str(input('Location and name of CSV file to save data EX:(D:\\\\FinTech\\\\UnderValuedStockSearcher\\\\Data12.csv): ')),
                              'dividend':float(input('Percent of share price given in dividend Annually EX:(1.50): ')),
                              'dataDate':str(input('Date where data is deemed inaccurate format EX:(YYYY-MM-DD): '))}])
        searchMarketUndervalued.run(args)
        print('Search Market Run Complete')
        rerun = input('Would you like to rerun? (Y/N)')
    print('**** End Program ****')
