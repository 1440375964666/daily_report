# from vnstock_data import Finance, Quote
# from datetime import date, timedelta
from datetime import date
# today = date.today()
# yesterday = date.today() - timedelta(days=1)
# quote = Quote(source='vnd', symbol="VNINDEX")
# vnindex = quote.history(start=f"{yesterday}", end=f"{today}", interval="1D")
# print(vnindex)
    
# # print(yesterday)

today = date.today()
print(today.strftime("%Y_%m_%d"))  # -> "2025_10_16"
print(today)