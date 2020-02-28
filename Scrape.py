#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

def get_content(url):
    
    """Get's HTML content for any provided url"""
    
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    content = bs(urlopen(req).read(), features='lxml')
    return content

def get_chapter_links(main_page):
    
    """Get's chapter links from the mainpage of a fiction"""
    
    content = get_content(main_page)
    table_of_contents = content.find_all('tr')
    links = []
    for row in range(1, len(table_of_contents)):
        abb_link = table_of_contents[row].find_all('a')[0].get('href')
        links.append(f'http://www.royalroad.com{abb_link}')
    return links

def get_chapter_content(chapter_url, formatting=True):
    
    """Get's only the story content from a chapter.
    
    Args:
        chapter_url (str): the full url for the chapter
        formatting (bool): determines if tabs and new lines are included im output
        
    Returns:
        Content formatted as a string.
    """
    
    ch_content = get_content(chapter_url)
    ch_content_cleaned = ch_content.find_all('p')
    ch_content_cleaned = ch_content_cleaned[1:len(ch_content_cleaned)-3]
    content_str = ''
    if formatting:
        for x in ch_content_cleaned:
            content_str += '\t' + x.get_text() + '\n'
    else:
        for x in ch_content_cleaned:
            content_str += x.get_text() + ' '
    return content_str

def get_top_stories(limit=20, category='best rated'):
    
    MAX_LIMIT = 100
    if limit > LIMIT: limit = LIMIT
    
    possible_categories = {'best rated': 'https://www.royalroad.com/fictions/best-rated',
                           'active only': 'https://www.royalroad.com/fictions/active-popular',
                           'complete': 'https://www.royalroad.com/fictions/complete',
                           'this week': 'https://www.royalroad.com/fictions/weekly-popular',
                           'latest update': 'https://www.royalroad.com/fictions/latest-updates',
                           'new releases': 'https://www.royalroad.com/fictions/new-releases',
                           'trending': 'https://www.royalroad.com/fictions/trending'}
    if category not in possible_categories:
        print('Valid categories include:')
        print(list(possible_categories.keys()))
    
    front_page = get_content(possible_categories[category])

fp = get_content('https://www.royalroad.com/fictions/best-rated')

print(fp.find_all('div', class_='fiction-list-item row')[1])

