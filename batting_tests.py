### Download ESPN test cricket batting stats webpage

import urllib2
import re
import itertools
import csv
from bs4 import BeautifulSoup

'''
Download function, as described in "Web Scraping with Python", by Richard Lawson

        url: Webpage to scrape
 user_agent: Identify who I am
num_retries: Retry failed download
'''
def download(url, user_agent='hvalle',num_retries=2):
    print 'Downloading:', url
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url, headers=headers)

    ### Check download occurs without errors
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        ### Retry failed download
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # Recursiely retry 5xx HTTP errors
                return download(url, user_agent, num_retries-1)
    return html

def scrape_data(h_elements,csv_writer):
    # Subset to table rows with with data
    data = [];
    for row in h_elements:
           if row.attrs and ('class' in row.attrs) and row['class'][0]=='data1':
               for string in row.stripped_strings:
                   data.append(string)
                #print data
                #data = []
               writer.writerow(data)
               data = []

def iterate_pages(h_url):
    html = download(h_url)
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the table rows
    rows = soup.find_all('tr')

    return rows

if __name__ == "__main__":

    ### Setup the csv file
    battingData = open('batting_test.csv','w')
    writer = csv.writer(battingData)

    try:
        fields = ['player','country','span','matches','innings','no','runs','hs','ave','100s','50s','ducks']
        writer.writerow(fields)

        for page in itertools.imap(lambda x: x+1, range(58)):
            url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;page=%d;template=results;type=batting' % page
            feature = iterate_pages(url)   
            scrape_data(feature, writer)

    finally:
        battingData.close()

    

    
