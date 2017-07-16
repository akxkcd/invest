import requests
from lxml import etree, html
from collections import defaultdict
import numpy as np

count = 1
cur_url = "http://www.dataroma.com/m/m_activity.php?m={}&typ=a&L={}".format("brk",count)

result = requests.get(cur_url)
print result.url
print result.text
result_file_path = "crawl_result/{}_{}.html".format("brk", count)
result_file = open(result_file_path, "w")

result_file.write(result.text)

tree = html.fromstring(result.content)
table = tree.find("body/div")
print(etree.tostring(tree, pretty_print=True))
#print tree, table
#table = etree.HTML(result.content).find("body/table")
rows = iter(table)
headers = [col.text for col in next(rows)]
for row in rows:
    values = [col.text for col in row]
    print dict(zip(headers, values))
#divs = tree.findall(".//div")
divs = tree.findall(".//table")
transactions = defaultdict(list)
cur_quarter = ""
for cur_div in divs:
    #print cur_div.tag, cur_div.text_content()
    for row in iter(cur_div):
        print "row", row.tag
        if row.tag == "tbody":
            cur_trans = []
            count = 0
            for tab_rows in iter(row):
                if tab_rows.get("class") == "q_chg":
                    print "processing a quarter:", tab_rows[0].text, tab_rows.text_content()
                    cur_quarter = tab_rows.text_content()
                    transactions[cur_quarter] = []


                if tab_rows.get("class") == "stock":
                    print "processing a transaction"
                    cur_trans = []
                    cur_trans.append(tab_rows[0].text)
                if (tab_rows.get("class") == "buy" or tab_rows.get("class") == "sell") and count == 1:
                    cur_trans.append(tab_rows.text_content())
                    transactions[cur_quarter].append(cur_trans)
                    #print "adding", count
                    cur_trans = []
                    count = 0
                elif tab_rows.get("class") == "buy" or\
                        tab_rows.get("class") == "sell":
                    cur_trans.append(tab_rows.get("class"))
                    count = 1

                    
                values = [col.text for col in tab_rows]
                #print tab_rows.get("class"), values, tab_rows.text_content()
        #print row.text_content()

print transactions
