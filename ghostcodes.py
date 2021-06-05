from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup as bs
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/849821595358330910/-1i9ULF_Uj4gedVVepkO8md_6Ah7ccMf54Csog0vBSrnlqAJesZHSkAnUx0Hh6B8nMgi', username="ghostcodes artist")

chrome_options  = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)
url = 'https://www.ghostcodes.com/category/non-profit'
driver.get(url)
file_name = url.split('/')[-1]
sleep(1)
count = 1
# for i in range(5):
try:
    while driver.find_element_by_xpath("//*[@id='load_more_button']"):
        try:
            try:
                try:
                    element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='load_more_button']"))
                        )
                    element.click()
                except:
                    sleep(5)
                    element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='load_more_button']"))
                        )
                    element.click()
            except:
                sleep(10)
                element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@id='load_more_button']"))
                    )
                element.click()
        except:
            sleep(30)
            element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='load_more_button']"))
                )
            element.click()
        sleep(1.5)
        print(count)
        count = count + 1
except:
    pass
links = []
lin = {}
soup = bs(driver.page_source,'html.parser')
list_of_users = soup.find('div',attrs={'id':'category_users_list_results'}).findAll('ul')
for list in list_of_users:
    lis= list.findAll('li')
    for li in lis:
        try:
            link = li.find('a')['href']
       
            if 'http' in link:
                print(link)
                lin = {
                    'links':link
                }
                links.append(lin)
            else:
                link = "https://www.ghostcodes.com" + link
                print(link)
                lin = {
                    'links':link
                }
                links.append(lin)
        except:
            link = '-'
print(len(links))
# driver.quit()

df = pd.DataFrame(links)
df.to_csv(f'ghostcoders_non_prof.csv',encoding='utf-8', index=False)

sleep(5)

with open(f'ghostcodes_non_prof.csv', "rb") as f:
    webhook.add_file(file=f.read(), filename=f'ghostcodes_non_prof.csv')

response = webhook.execute()
webhook.remove_files()

print('Bot Sent files')