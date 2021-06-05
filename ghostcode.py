from os import link
import aiohttp
import asyncio
import os
from numpy.core.arrayprint import set_printoptions
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor
import time
from bs4 import BeautifulSoup
import requests
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed
webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/849821595358330910/-1i9ULF_Uj4gedVVepkO8md_6Ah7ccMf54Csog0vBSrnlqAJesZHSkAnUx0Hh6B8nMgi', username="ghostcodes artist")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Safari/537.36'
}
startTime = time.time()

nam = 'dance'
df = pd.read_excel(f'ghostcoders_{nam}.xlsx')
linka = df['links'].tolist()
links = []
for li in linka:
  if 'ghostcodes' in li:
    links.append(li)
print(len(links))
data = {}
lists = []
res = []


def fetch(session, url):
    with session.get(url, headers=headers) as response:
        res.append(response)


def main():
    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            num = 1
            for link in links:
                executor.map(fetch, [session], [link])
                print(num)
                num = num + 1
            executor.shutdown(wait=True)


main()
counter = 1
for r in res:
    print(counter)
    counter = counter + 1
    soup = BeautifulSoup(r.content, 'lxml')
    try:
      title1 = soup.find('title').text.split('.')[0].replace('GhostCodes profile of ','')
      name = soup.find('h1',attrs = {'class':'text-center'}).text.replace(title1,'').strip()
      title = title1.lower()
    except:
      name = '-'
      title = '-'
    try:
      likes = soup.find('span',attrs = {'class':'user-likes'}).text
    except:
      likes = '-'
    try:
      img_link = soup.find('div',attrs = {'class':'user-profile'}).findAll('img')[2]['data-original']
    except:
      img_link = '-'
    try:
      category = soup.find('div',attrs = {'class':'user-profile'}).find('a')['href'].split('/')[-1]
    except:
      category = '-'
    try:
        bio = soup.find('div',attrs = {'class':'user-profile'}).find('p').text
    except:
        bio = '-'
    print(name)
    try:
      social_links = soup.findAll('div',attrs={'class':'text-center'})[1].findAll('a')

      for social in social_links:
          if 'facebook' in social['href']:
              facebook = social['href']
          elif 'snapchat' in social['href']:
              snapchat = social['href']
          elif 'twitter' in social['href']:
              twitter = social['href']
          elif 'instagram' in social['href']:
              instagram = social['href']
          elif 'youtube' in social['href']:
              youtube = social['href']
          elif 'periscope' in social['href']:
              periscope = social['href']
          elif 'linkedin' in social['href']:
              linkedin = social['href']
          elif 'pinterest' in social['href']:
              pinterest = social['href']
          else:
              others = social['href']
      try:
          facebook = facebook
      except:
          facebook = '-'
      try:
          snapchat = snapchat
      except:
          snapchat = '-'
      try:
          twitter = twitter
      except:
          twitter = '-'
      try:
          instagram = instagram
      except:
          instagram = '-'
      try:
          youtube = youtube
      except:
          youtube = '-'
      try:
          linkedin = linkedin
      except:
          linkedin = '-'
      try:
          periscope = periscope
      except:
          periscope = '-'
      try:
          pinterest = pinterest
      except:
          pinterest = '-'
      try:
          others = others
      except:
          others = '-'
    except:
      facebook = '-'
      snapchat = '-'
      twitter = '-'
      instagram = '-'
      youtube = '-'
      linkedin = '-'
      periscope = '-'
      pinterest = '-'
      others = '-'
    data = {
        'name': name,
        'title': title,
        'likes':likes,
        'image link': img_link,
        'category':category,
        'bio':bio,
        'facebook': facebook,
        'instagram':instagram,
        'snapchat':snapchat,
        'twitter':twitter,
        'linkedin':linkedin,
        'youtube':youtube,
        'periscope':periscope,
        'pinterest': pinterest,
        'others':others
    }
    lists.append(data)
    facebook = '-'
    snapchat = '-'
    twitter = '-'
    instagram = '-'
    youtube = '-'
    linkedin = '-'
    periscope = '-'
    pinterest = '-'
    others = '-'
df = pd.DataFrame(lists).drop_duplicates()
df.to_csv(f'ghostcode_thread_{nam}.csv',encoding='utf-8', index=False)

time.sleep(2)
print('2nd portion...')

df = pd.read_csv(f'ghostcode_thread_{nam}.csv')
name = df['name'].tolist()
title = df['title'].tolist()
image_link = df['image link'].tolist()
category = df['category'].tolist()
bio = df['bio'].tolist()
facebook = df['facebook'].tolist()
snapchat = df['snapchat'].tolist()
twitter = df['twitter'].tolist()
instagram = df['instagram'].tolist()
youtube = df['youtube'].tolist()
periscope = df['periscope'].tolist()
linkedin = df['linkedin'].tolist()
pinterest = df['pinterest'].tolist()
others = df['others'].tolist()

datan = {}
listan = []
for link in links:
    lins = link.split('/')[-1]
    for na,tit,ima,cat,bi,face,snap,twit,inst,you,peri,lin,pin,oth in zip(name,title,image_link,category,bio,facebook,snapchat,twitter,instagram,youtube,periscope,linkedin,pinterest,others):
        if lins == tit:
            datan = {
                'Link':link,
                'Name': na,
                'Title':tit,
                'Image Link': ima,
                'Category': cat,
                'Bio': bi,
                'Facebook':face,
                'Snapchat': snap,
                'Twitter': twit,
                'Instagram': inst,
                'Youtube': you,
                'Periscope': peri,
                'Linkedin': lin,
                'Pinterest': pin,
                'Other Links': oth
            }
            listan.append(datan)
df = pd.DataFrame(listan).drop_duplicates()
df.to_csv(f'ghostcode_{nam}_final.csv',encoding='utf-8', index=False)
time.sleep(2)

with open(f'ghostcode_{nam}_final.csv', "rb") as f:
    webhook.add_file(file=f.read(), filename=f'ghostcode_{nam}_final.csv')

response = webhook.execute()
webhook.remove_files()

print('Bot Sent files')