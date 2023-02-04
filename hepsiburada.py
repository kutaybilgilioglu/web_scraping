import csv
import time
from typing import Optional, Match

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import re
import locale
locale.setlocale(locale.LC_NUMERIC,'tr_TR')

computers = ['ASUS','Acer','MSI','Lenovo','HP','Apple','Monster','Dell']
screen_keywords = ['inç','"',"''",'15.6','17.3','14','16','16.0']
marka = ''
model = ''

class hepsiburada:
    def is_computer(self,item):
        global computers, marka
        for computer in computers:
            if computer in item:
                marka = computer
                return True
        return False

    def model_extract(self,item):
        global marka, model
        if marka == 'Lenovo':
            model = re.search(
                r'20x3..........|82.....gtx|20t........|30e.......|20......ea|20......ea\d\d|11......tx\d\d|11......tx|20tn......\d\d|90m.........|11q..........|81........\d\d|21........\d\d|82........\d\d|20tes.....|20yg.........|20vd........|20tdf........|20ta0...tx|20tk.......|20ta0........|20yg......|20v.......|20tbs........|20td......|20y...........|82........|81........|20ta......|21........',
                item, re.IGNORECASE)
            if model:
                model = model.group()
        elif marka == 'MSI':
            model = re.search(
                r'a5........|11s........|11u.....xtr|11u.......|11u........|b5.........|12u........|12u.....tr|a11.........|a11........|b12..........|a12........',
                item, re.IGNORECASE)
            if model:
                model = model.group()
        elif marka == 'HP':
            model = re.search(
                r'54...ea|6q...e.|5....ea\d\d|5....ea|6....ea\d\d|6....ea|2v...e.\d\d|5f...ea|69q..ea|62...ea|6b8..ea\d\d|6b8....|6q...e.\d\d|3....e.|2....ea|1....ea|54t2.ea|6z.......|06........|39...ea|6s.....|22.......|6q...ea|6q...ea\d\d|4h...ea|6g...ea|68...ea|6y...ea|4g...ea|9H...ea|4p...e.',
                item, re.IGNORECASE)
            if model:
                model = model.group()
        elif marka == 'Acer':
            model = re.search(
                r'an.....\d|a315...|an...........|sf.......\w|sf.......|a7......|tmp.......|nh..........|nx..........',
                item,
                re.IGNORECASE)
            if model:
                model = model.group()
        elif marka == 'Dell':
            model = re.search(
                r'fb.........n..|fb1.......n|g5........u|n..........emea.......|fb..f..\w|f35.........\d|35........\w|f35.......|g5....\d\d\d\du|n0..............u|\d\d\d\d.i\d.\d\d\d\d\d.\d|n0..........\w|t78...silver..........|xct..............\d|xct............|.\d\d\d\d-w-\d\d\d\d|\d\d\d\d-w-\d\d\d\d-\d|xps..............|t58.......\d\d|g5.........\d\d|i56.......|n\d\d\d\d.......u|f11......|n02........em....|i77..........|sif15....................|xct.................|n4.................|n01..............5|n01.................|n01..............|n21..............|4b........|n20............|n80...............u|n60.................|n80...............|n65..................|fb......|i35.........|i35.......|cyborg...............|n\d\d\d\d...............\d|in..........\d|i........\w\w',
                item, re.IGNORECASE)
            if model:
                model = model.group()
        elif marka == 'Monster':
            model = re.search(r'V\d...\d|V\d....\d|V\d..\d', item)
            if model:
                model = model.group()
        elif marka == 'ASUS':
            model = re.search(
                r'x5...........|d51.........|g51.........|fa5..........|b15...............|h56..........|gv3..........|m15.............|fx............|k51...........',
                item, re.IGNORECASE)
            if model:
                model = model.group()
        else:
            model = ''

    def components(self,item):
        global screen_keywords
        gpu_pattern = re.compile(r'rx.....|gtx.....\D|.rtx.....\D|rtx.....|mx...|integrated...........|iris....',
                                 re.IGNORECASE)
        ram_pattern = re.compile(r'...gb\sram', re.IGNORECASE)
        islemci_pattern = re.compile(r'i\d.......|ryzen.......|celeron....|m2|m1', re.IGNORECASE)
        # number_converter = re.compile(r'[0-9]+')
        ram = ram_pattern.search(item)
        gpu = gpu_pattern.search(item)
        islemci = islemci_pattern.search(item)
        if islemci:
            islemci = islemci.group().strip(' ,-')
        #print(islemci)
        if gpu:
            gpu = gpu.group()

        else:
            gpu = ''

        if not ram:
            ram_pattern1 = re.compile(r'.\dgb', re.IGNORECASE)
            ram = ram_pattern1.search(item)

        # print(ram)

        if ram:
            ram = re.findall(r'[0-9]+', ram.group())
            ram = int(ram[0])
            # print(type(ram[0]))
        screen = ''
        for index, screen_s in enumerate(screen_keywords):
            if screen_s in item:
                if index > 2:
                    screen = screen_keywords[index]
                else:
                    index_b = item.find(screen_s)
                    # index_e = item.find(',',index_b)
                    screen = item[index_b - 5:index_b + 4]
                    screen = screen.strip(" (HDG,-FH:Gtxr,BQHinç")
        if screen == '':
            print(item)
        component_ls = (screen, ram, gpu, islemci)
        return component_ls

    def extract_record(self,item):
        global marka
        datum = {}
        atag = item.a

        description = item.h3.text.strip()
        #description = description.strip()
        #print(description)
        component_ls = self.components(description)
        item_url = 'https://www.hepsiburada.com' + atag.get('href')
        #print(item_url)
        try:
            price = item.find('div', attrs={'data-test-id':'price-current-price'}).text
            price = price.strip(' TL')
            price = locale.atof(price)

        except AttributeError:
            return
        image_url = item.img
        image_url = image_url.get('src')
        rating = ''
        review_count = ''



        result = (description, marka, component_ls[0], component_ls[1], component_ls[2], component_ls[3], price, rating,
                  review_count, item_url, image_url)
        return result

    def __init__(self):
        global model
        driver = webdriver.Chrome(ChromeDriverManager().install())

        client = MongoClient("mongodb://localhost:27017/")
        db = client["yazlab"]
        collection = db["hepsiburada"]
        collection.drop()
        db = client["yazlab"]
        collection = db["hepsiburada"]


        records = []
        data = []
        for page in range(1, 25):
            url = 'https://www.hepsiburada.com/asus-lenovo-dell-hp-msi-monster-acer/laptop-notebook-dizustu-bilgisayarlar-c-98'
            page_str = str(page)
            url += '?sayfa=' + page_str
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            results = soup.find_all('li', {'type': 'comfort'})
            for item in results:
                datum = {}
                tag = item.a
                tag = tag.get('title')
                description_c = tag.strip()
                if self.is_computer(description_c) == False:
                    continue
                self.model_extract(description_c)
                record = self.extract_record(item)

                if record:
                    datum['description'] = record[0]
                    datum['marka'] = record[1]
                    datum['model'] = model
                    datum['ekran'] = record[2]
                    datum['ram'] = record[3]
                    datum['ekran_karti'] = record[4]
                    datum['islemci'] = record[5]
                    datum['fiyat'] = record[6]
                    datum['puan'] = record[7]
                    datum['yorum_sayisi'] = record[8]
                    datum['url'] = record[9]
                    datum['img_url'] = record[10]
                    datum['site'] = 'amazon'
                    data.append(datum)
                    records.append(record)

        driver.close()
        for computer in data:
            x = collection.insert_one(computer)
        with open('results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['Description', 'marka', 'ekran', 'islemci', 'ram', 'ekran_karti', 'depolama', 'isletim_sistemi',
                 'model', 'Price', 'Rating', 'ReviewCount', 'Url', 'ImageUrl'])
            writer.writerows(records)



#hepsiburada()


