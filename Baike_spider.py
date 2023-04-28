"""
@Description :   BaiduBaike spider
@Author      :   zlJin_Jackson 
@Time        :   2023/04/26 18:50:39
"""

import requests
from bs4 import BeautifulSoup
import random
import time
import json
from tqdm import tqdm
import sys
import os

url_prefix = " https://baike.baidu.com/item/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# print(url_prefix)

not_found_word_file = 'result/Not_found_keyword_list.txt'
crawled_file = 'result/crawled_keyword.jsonl'
all_info_file = 'result/all_crawled_info.jsonl'

# get crawled keyword
def get_already_crwal_set(crawled_keyword_file):
    print('loading crawled baike keyword...')
    Crawled_keyword_set = set()
    Crawled_url_set = set()
    with open(crawled_keyword_file, 'r', encoding='utf-8') as reader:
        lines = reader.readlines()
        for line in tqdm(lines, desc='crawling'):
            a_data = json.loads(line)
            Crawled_keyword_set.add(a_data["keyword"])
            Crawled_url_set.add(a_data["url"])

    print("done, " + str(len(Crawled_keyword_set)) + " keyword has been crawled from Baidu Baike")
    return Crawled_keyword_set, Crawled_url_set


# get not found keyword
def get_not_found_set(not_found_word_file):

    print('loading not found keyword set...')

    with open(not_found_word_file, 'r', encoding='utf-8') as reader:
        lines = reader.readlines()

    Not_found_set = set(map(lambda x: x.strip(), lines)) 
    print('done, ' + str(len(Not_found_set)) + " keyword not found in Baidu Baike")
    return Not_found_set


# given keyword, get url
def get_crawl_url(keyword_list):

    new_url_list = []
    
    for keyword in keyword_list:
        new_url_list.append([keyword, url_prefix + keyword])
    
    return new_url_list


# given url, crawl content
def crawl_content(url_list):
    global count
    for keyword, url in tqdm(url_list):
        if keyword in Crawled_keyword_set or url in Crawled_url_set:
            continue
        print(url+"")
        print(headers)
        response = requests.get(url+"", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', class_='main-content')
        # if keyword doest exist
        if content == None :
            Not_found(keyword, Not_found_set)
        else:
            count += 1
            found_and_record(keyword, url, soup)

        rest_time = random.random() * 20
        print('rest for ' + str(rest_time) + "secs")
        time.sleep(rest_time)
    print('crawl done')

def Not_found(key_word, Not_found_set):
    global not_found_count
    not_found_count += 1
    if key_word in Not_found_set:
        return
    else:
        with open("result/Not_found_keyword_list.txt", 'a', encoding='utf-8') as writer:
            writer.write(key_word + '\n')
        Not_found_set.add(key_word)



def record_keyword_allinfo(all_info_file, a_data):

    with open(all_info_file, 'a', encoding='utf-8') as writer:
        json_str = json.dumps(a_data, ensure_ascii=False)
        writer.write(json_str + '\n')
    Crawled_keyword_set.add(a_data["keyword"])
    Crawled_url_set.add(a_data["url"])



def found_and_record(keyword, url, soup):
    title = soup.find('h1').get_text()
    if title in Crawled_keyword_set:
        return
    main_content = soup.find('div', class_='main-content').get_text().replace(' ', '').replace('\n', '').replace('\xa0', '')
    links = []
    filter_list = ['秒懂本尊答', '秒懂大师说', '秒懂看瓦特', '秒懂五千年', '秒懂全视界', '百科热词团队']
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'item' in href:
            for filter_word in filter_list:
                if filter_word in href:
                    break
            else:
                links.append("https://baike.baidu.com" + href)

    a_data = {"keyword": keyword, 
              "url": url,
              "title": title,
              "content": main_content,
              "linked_links:": links}
    
    record_keyword_allinfo(all_info_file, a_data)

    with open(crawled_file, 'a', encoding='utf-8') as writer:
        crawled_data = json.dumps({'keyword': keyword, 'url': url}, ensure_ascii=False)
        writer.write(crawled_data + '\n')
    
    return a_data


def crawl_main(keyword_list):
    new_url_list = get_crawl_url(keyword_list)

    crawl_content(new_url_list)

    
    
def read_keyword_file(keyword_file):
    with open(keyword_file, 'r', encoding='utf-8') as reader:
        lines = reader.readlines()
        keyword = list(map(lambda x: x.strip(), lines))
    return keyword

if __name__ == "__main__":
    count = 0
    not_found_count = 0
    # 加载已经爬过的keyword
    Crawled_keyword_set, Crawled_url_set = get_already_crwal_set(crawled_file)
    # 加载不存在的keyword
    Not_found_set = get_not_found_set(not_found_word_file)

    # 需要爬取的keyword_file
    # keyword_file = './keyword_file/4_27_12_01.txt'
    keyword_file = sys.argv[1]

    if not os.path.exists(keyword_file):
        print("file not exists, plz check again")    
        sys.exit(1)
    else:
        print('reading keyword file ....')
    keyword_list = read_keyword_file(keyword_file)

    crawl_main(keyword_list)
    res = str(count) + ' keyword has been collected. ' + \
            str(not_found_count) + " keyword not found. " + \
            str(len(keyword_list) - count - not_found_count) + "keyword repeated."
    print(res)
    
    # new_url_list = get_crawl_url(keyword_list)

    # print(new_url_list)