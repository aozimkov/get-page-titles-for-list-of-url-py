# this script parsing urls from csv file and collect titles from each url
import pandas as pd
import os
from lxml.html import parse
from urllib2 import urlopen, Request, HTTPError, URLError

SCRIPT_URL = os.path.dirname(os.path.abspath(__file__))
FILE_WITH_URLS_FILENAME = "report.csv"

def get_list_of_url(filename):
    columns = 'url'
    data = pd.read_csv('{}/{}'.format(SCRIPT_URL, filename), header=None, names=[columns])
    data.drop_duplicates(subset=columns, keep=False, inplace=True)
    urls = []
    for i in range(0, len(data)):
        urls.append(data.iloc[i][columns])
    return urls

def get_page_title(url):

    req = Request(url)
    try:
        response = urlopen(req)
    except HTTPError as e:
        return e
    except URLError as e:
        return e.reason

    page = urlopen(url)
    p = parse(page)
    return p.find(".//title").text

def main():
    print("Loading urls from file...")
    urls = get_list_of_url(REPORT_FILENAME)
    print("{} urls loaded".format(len(urls)))
    
    titles = []
    for url in urls:
        print(get_page_title(url))
        titles.append(get_page_title(url))
    
    ready_dict = {'urls': urls, 'titles': titles}
    result_dataframe = pd.DataFrame.from_dict(ready_dict)

    export_filename  = '{}/ready-{}'.format(SCRIPT_URL, FILE_WITH_URLS_FILENAME)
    result_dataframe.to_csv(export_filename, sep=';', columns=['urls', 'titles'], index = False, encoding='utf-8', quotechar='"')

if __name__ == "__main__":
    main()
