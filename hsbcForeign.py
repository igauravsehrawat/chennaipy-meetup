import urllib2
from lxml import html
from lxml import etree
import string
import requests
import csv

__all__ = ["hsbcForeign"]

def hsbcForeign():

    req_headers = {
        'User-agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safar/537.36'
        }
    laterToCSV = []
    one_row = {}

    laterToCSV = []
    period = ["2 Wk","3 Wk","1 Mth","2 Mth","3 Mth","6 Mth","9 Mth","12 Mth"]
    currency = ["AUD"]
    Product_name = ["HSBC "]
    for cur_code in currency:
        data = {
                "curcode":  cur_code}
        r = requests.post("http://www.datafeeds.hsbc.com.sg/sg/unitrust/foreign_currency_time_deposit_rates.jsp", data=data , headers= req_headers)
        table_gbp = html.fromstring(r.text)
        all_table = table_gbp.xpath("//table[@width='96%']")
        for tbl_itr in xrange(0,1):
            relevant_table = all_table[tbl_itr]
            all_tr = relevant_table.findall('tr')
            for tr_itr in xrange(2,len(all_tr)):
                all_td = all_tr[tr_itr].findall('td')
                min_max = all_td[0].text
                min_max = string.replace(string.replace(string.replace(string.replace(min_max,",",""),"Min",""),cur_code,""),u"\xa0","")
                if "above" in min_max:
                    #replaceing min,cur_code,","
                    min_amt = min_max.split("and")[0]
                    max_amt = 999999999
                else:
                    min_amt = min_max.split("to")[0]
                    max_amt = min_max.split("to")[1]

                for td_itr in xrange(1,8):
                    one_row["Product"] = Product_name[tbl_itr]+ cur_code + " Foreign Currency Time Deposit"
                    one_row["Currency"] = cur_code
                    one_row["Period"] = period[td_itr]
                    one_row["InterestRate"] = float(string.replace(all_td[td_itr].text,"%",""))
                    one_row["MinAmt"] = int(min_amt)
                    one_row["MaxAmt"] = int(max_amt)
                    print one_row
                    laterToCSV.append(one_row)
                    one_row = {}

    # keys = laterToCSV[0].keys()
    # print keys
    # with open('hsbcForeign.csv','wb') as output_file:
    #     dict_writer = csv.DictWriter(output_file, keys)
    #     dict_writer.writeheader()
    #     dict_writer.writerows(laterToCSV)
    return laterToCSV

if __name__ == "__main__":
    hsbcForeign()
