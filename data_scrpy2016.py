import urllib2
from bs4 import BeautifulSoup
import csv
import time

#see page number from http://www.century21-hk.com/tran_prop.php
from_page = 481
to_page = 1741
year = 2016
folder_name = "2016_data"
lock = False
domain = 'http://www.century21-hk.com/'

def get_page(num_page):
    quote_page = domain + 'tran_prop.php?page='+str(num_page)+'&year='+str(year)
    while True:
        try:
            page = urllib2.urlopen(quote_page)
            lock = True
            break
        except:
            print("Error, try to reconnect ...")
            time.sleep(.3)
            continue
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def get_table_row(soup):
    info_table = soup.find_all('table')[7]
    info_table_row = info_table.find_all('tr')
    return info_table_row

def insert_csv(info_table_row):
    with open(folder_name + '.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for n_row in range(1, len(info_table_row) - 3):
            info_export = []
            for n_col in range(1, 8):
                info_export.append(info_table_row[n_row].find_all('td')[n_col].text.encode('utf8'))
            property_link = domain+info_table_row[n_row].find_all('td')[8].a['href']
            property_detail = generate_property_detail(property_link)
            info_export = info_export + property_detail
            writer.writerow(info_export)

def generate_property_detail(property_page):
    while True:
        try:
            page = urllib2.urlopen(property_page)
            lock = True
            break
        except:
            print("Error, try to reconnect to detail page ...")
            time.sleep(.3)
            continue
    soup = BeautifulSoup(page, 'html.parser')
    info_table = soup.find_all('table')[6];
    #get all rows
    info_table_row = info_table.find_all("tr")
    #get right column
    info_export = []
    for n_row in range(0, len(info_table_row) ):
        info_td = info_table_row[n_row].find_all('td')
        for n_col in range(1,len(info_td),2):
            # print(info_td[n_col].text)
            info_export.append(info_td[n_col].text.encode('utf8').strip(' \t\n\r'))
            # info_export.append(info_table_row[n_row].find_all('td')[n_col].text.encode('utf8'))
    return info_export

def generate_result(page):
    soup = get_page(page)
    info_table_row = get_table_row(soup)
    insert_csv(info_table_row)
    print("Page "+str(page)+" done!")


page = from_page
while (bool(lock) == False and page < to_page + 1):
    generate_result(page)
    page = page + 1
