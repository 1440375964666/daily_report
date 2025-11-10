from vnstock_data import Finance
fin = Finance(symbol='TCX', period='year', source='MAS')
print(fin.income_statement()["Doanh thu thuần"])