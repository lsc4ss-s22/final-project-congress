'''
Name: scrape_cr_pt.py
Author: Lynette Dang

Crawl congressional record pages and scrape all congressional record in given
date range for the given legislature (house or senate) using pool thread
executor, , save the results in a dictionary, with key being speaker, value
being all speeches given by the speaker

References:
1. https://towardsdatascience.com/political-python-1e8eb46c1bc1
2. https://superfastpython.com/threadpoolexecutor-get-results/
2. http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
3. https://stackoverflow.com/questions/9278858/python-exception-logging-correct-syntax
4. https://github.com/jchaskell/scraper-cr
5. https://github.com/jchaskell/scraper-cr/blob/master/clean/filterCR_fix.py
'''


# import scraping libraries
import re
import requests
from datetime import date, timedelta as td
from bs4 import BeautifulSoup
import json
import logging
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, as_completed, wait


URL = "https://www.congress.gov/congressional-record/"
URL_ROOT = "https://www.congress.gov"
MATCH = ['Mr. McCONNELL.', 'Mr. McCONNELL', 'The PRESIDING OFFICER', 'The PRESIDING OFFICER.',
         'The PRESIDENT pro tempore', 'The PRESIDENT pro tempore.', 'The PRESIDING OFFICER',
         'The PRESIDING OFFICER.', 'The PRESIDENT', 'The PRESIDENT.', 'The VICE PRESIDENT',
         'The VICE PRESIDENT.', 'The PRESIDING OFFICER', 'The PRESIDING OFFICER.', 'Mr. PRESIDENT.',
         'Mr. PRESIDENT', 'The SPEAKER pro tempore', 'The SPEAKER pro tempore.', 'The SPEAKER.',
         'The SPEAKER']
SPEAKER_MATCH = r"^\s*(((Mr\.|Ms\.|Mrs\.) [A-Z][ec]?[A-Z-]+\.)|((Mr\.|Ms\.|Mrs\.) [A-Z][ec]?[A-Z-]+ of \w+( \w+)?\.)|(The PRESIDENT pro tempore\.?)|(The PRESIDING OFFICER\.?)|(The PRESIDENT\.)|(The VICE PRESIDENT\.?)|(The PRESIDING OFFICER \(.*\)\.?))( .*)"
PROCEEDING = r'There\s+being\s+no\s+objection,\s+the\s+\w+\s+was\s+ordered\s+to\s+be\s+printed\s+in\s+the\s+Record,\s+as\s+follows:'


class CRScraper:

    def __init__(self, dir_, section):
        self.headers = {"User-Agent": "web scraper for classroom purposes"}
        self.section = section
        self.tail_url = "/" + section + "-section"
        self.logger = logging.getLogger('cr_logger')
        self.dir_ = dir_ + "/" + section

    def get_links(self, url):
        '''
        Retrieves link to one day of congressional record

        Inputs:
            url: the link to congressional record

        Outputs:
            links: all truncated links to congressional record for a day
        '''
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.text, "html")
        # only even numbered indexes
        issues = [issue for issue in soup.find_all('td')]
        links = [issues[i].a.get('href')
                 for i in range(len(issues)) if not i % 2]
        print(links)
        return(links)

    def scrape_page(self, url):
        '''
        Scrapes one issue of congressional record, store the content and return

        Inputs:
            url: the link to congressional record

        Outputs:
            text: content of one issue of congressional record
        '''
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.text, "html")
        while True:
            try:
                text = soup.find('pre', class_='styled').text
                if text:
                    text_all = ''.join(str(text))
                    return text_all
                break
            except AttributeError as e:
                self.logger.exception(
                    'There was an Attribute Error; details are %s' % e)

    def clean_and_split(self, data):
        '''
        Clean the scraped daily congressional record
        Credit to Jen Haskell's "Scraping the Congressional Record"

        Inputs:
            data: raw text of daily congressional record

        Outputs:
            lines: a list of the lines in the cleaned-up daily congressional
            record
        '''
        data = re.sub(
            r'From the Congressional Record Online through the Government Publishing Office \[www\.gpo\.gov\]', '', data)
        data = re.sub(
            r"[\[]{1,2}\', \<a href\=[\"\''][^\s]+[\"\'']\>Page S[0-9]+\</a\>, u[\"\''][\]]{1,2}", "", data)
        data = re.sub(
            r"[\[]{1,2}\', \<a href\=[\"\''][^\s]+[\"\'']\>Pages S[0-9]+\-S[0-9]+\</a\>, u[\"\''][\]]{1,2}", "", data)
        data = re.sub(
            r"\<a href\=[\"\''][^\s]+[\"\'']\>([^\<\>]+)\</a\>", r"\1", data)
        data = re.sub(r'\[?\[[\"\'], Page S[0-9]+, u[\'\"]?\]\]?', '', data)
        data = re.sub(r'([\'\"]\]|\[u\\?[\'\"])', '', data)
        data = re.sub(r'\s{2,}', ' ', data)
        data = re.sub(
            r'\(?[\'\"], ([SH]\. Res\. [0-9]+|[SH]\.J\. Res\. [0-9]+|[HS]\. Con\. Res\. [0-9]+|S\. [0-9]+|H\.R\. [0-9]+), u[\'\"]\)?', r'\1', data)
        matches = r"(((Mr\.|Ms\.|Mrs\.) [A-Z][ec]?[A-Z-]+\.)|((Mr\.|Ms\.|Mrs\.) [A-Z][ec]?[A-Z-]+ of \w+( \w+)?\.)|(The PRESIDENT pro tempore\.?)|(The PRESIDING OFFICER\.?)|(The PRESIDENT\.)|(The VICE PRESIDENT\.?)|(The PRESIDING OFFICER \(.*\)\.?))"
        data = re.sub(matches, "\\n\\n\\1", data)
        data = re.sub(r'(______)', "\\n\\n\\1\\n\\n", data)
        data = re.sub(r'(There\s+being\s+no\s+objection,\s+the\s+\w+\s+was\s+ordered\s+to\s+be\s+printed\s+in\s+the\s+Record,\s+as\s+follows:)',
                      '\\1\\n\\n', data)  # need to fix splitting mechanism here - doesn't seem to be working

        data = re.sub(r'(\\n){2,}', '\n', data)
        data = re.sub(r'\\n', ' ', data)
        lines = data.splitlines()
        return lines

    def parse_speech(self, lines):
        '''
        Parse the speech from the lines of daily congressional record passed in
        Credit to Jen Haskell's "Scraping the Congressional Record"

        Inputs:
            lines: a list of the lines in the cleaned-up daily congressional
            record

        Outputs:
            all_speeches: a list of speech with identified speaker and speech
        '''
        all_speeches = []
        speaker = ""
        speech = ""
        for _, l in enumerate(lines):
            if re.search(r'__', l):
                if speaker:
                    all_speeches.append(speaker + "\t " + speech)
                speaker = ""
                speech = ""
                continue
            else:
                match = re.findall(SPEAKER_MATCH, l)
                if match:
                    if speaker:
                        all_speeches.append(
                            speaker + "\t " + speech)
                    speaker = ""
                    speech = ""
                    if match[0][0] != speaker:
                        if speaker:
                            all_speeches.append(
                                speaker + "\t " + speech)
                        speaker = match[0][0]
                        speech = match[0][0] + match[0][11]
                        if re.search(PROCEEDING, l):
                            all_speeches.append(
                                speaker + "\t " + speech)
                            speaker = ""
                            speech = ""
                else:
                    if not speaker:
                        continue
                    else:
                        speech += " " + l
        if speaker:
            all_speeches.append(speaker + '\t ' + speech)
        return(all_speeches)

    def scrape_record(self, date):
        '''
        Scrape the congressional record for a range of dates, and store the
        record in a dictionary with speaker as the key, and the speech given
        by the speaker as value

        Inputs:
            /

        Outputs:
            speech: a dictionary with speaker as the key, and the speech given
            by the speaker as value of all congressional record in given date
            range and section
        '''
        day_url = URL + date + self.tail_url
        print(day_url)
        links = self.get_links(day_url)
        daily_cr = ""
        for link in links:
            link = URL_ROOT + link
            print(link)
            while True:
                try:
                    daily_cr = daily_cr + " " + self.scrape_page(link)
                    break
                except AttributeError as e:
                    self.logger.exception(
                        'There was an Attribute Error; details are %s and the url is %s' % e % link)
        return daily_cr


def main():
    dir_ = '.'

    # get the range of date
    start_date = date(2019, 1, 1)
    end_date = date(2021, 12, 31)
    section1 = "house"
    section2 = "senate"
    dates = []
    for n in range(int((end_date - start_date).days)+1):
        d = start_date + td(n)
        d = d.strftime("%Y/%m/%d")
        dates.append(d)

    # scrape house speeches
    scrape_house = CRScraper(dir_, section1)
    with ThreadPoolExecutor(max_workers=8) as executor:
        # download each url and save as a local file
        futures = [executor.submit(
            scrape_house.scrape_record, date) for date in dates]
    wait(futures, timeout=1000, return_when=ALL_COMPLETED)
    merged_list = [v for f in futures for v in f.result()]
    speech_house = {}
    cr_house = ''.join(merged_list)
    lines = scrape_house.clean_and_split(cr_house)
    raw_text = scrape_house.parse_speech(lines)
    for line in raw_text:
        text = line.split("\t")
        if text[0] not in MATCH:
            speaker = text[0]
            if text[0][-1] == ".":
                speaker = text[0][:-1]
                speech_house[speaker] = speech_house.get(
                    text[0], "") + text[1] + " "
    with open(f"speech_{section1}_{start_date}_{end_date}.json", "w") as f:
        json.dump(speech_house, f)

    # scrape senate speeches
    scrape_senate = CRScraper(dir_, section2)
    with ThreadPoolExecutor(max_workers=8) as executor:
        # download each url and save as a local file
        futures = [executor.submit(
            scrape_senate.scrape_record, date) for date in dates]
    wait(futures, timeout=1000, return_when=ALL_COMPLETED)
    merged_list = [v for f in futures for v in f.result()]
    speech_senate = {}
    cr_senate = ''.join(merged_list)
    lines = scrape_house.clean_and_split(cr_senate)
    raw_text = scrape_house.parse_speech(lines)
    for line in raw_text:
        text = line.split("\t")
        if text[0] not in MATCH:
            speaker = text[0]
            if text[0][-1] == ".":
                speaker = text[0][:-1]
                speech_senate[speaker] = speech_senate.get(
                    text[0], "") + text[1] + " "
    with open(f"speech_{section2}_{start_date}_{end_date}.json", "w") as f:
        json.dump(speech_senate, f)
    print("successfully wrote house and senate speeches")


if __name__ == '__main__':
    main()
