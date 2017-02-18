### Download ESPN test cricket batting stats webpage

'''
TODO

Update the programs so that the link iterates over a list of categories:
e.g. types = ['batting', 'bowling', 'fielding']

TODO

Update the programs so that they capture the player link
e.g. test = row.find_all("a",limit=1)

TODO

Update the programs so that the code is inserted and updated
straight into MongoDB. That is, skip the intermediate step
of importing the constructed CSV file.

TODO

Add an exception to the TRY block in case there is an error.

'''

import urllib2
import re
import itertools
import csv
from bs4 import BeautifulSoup

'''
Download function, as described in "Web Scraping with Python",
by Richard Lawson

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
    bowlingData = open('bowling_test.csv','w')
    writer = csv.writer(bowlingData)
    
    try:
        fields = ['player','country','span','matches','innings','balls','runs','wkts','bbi','bbm','ave','econ','sr','_5s','_10s']
        writer.writerow(fields)

#url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;page=1;template=results;type=bowling'

        for page in itertools.imap(lambda x: x+1, range(58)):
            url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;page=%d;template=results;type=bowling' % page
            feature = iterate_pages(url)   
            scrape_data(feature, writer)

    finally:
        bowlingData.close()

    

    
