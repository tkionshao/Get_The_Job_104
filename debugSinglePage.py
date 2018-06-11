#!bin/python3

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import json
import datetime as dt
import re


# address_link = "http://www.104.com.tw/job/?jobno=5mnd9&jobsource=n104bank1"

# response = requests.get(address_link)
# single_company = BeautifulSoup(response.text)
# addresses = single_company.find("dl").find_all("dd")[3].strings
# address = list(addresses)[0].strip()
job_link = "https://www.104.com.tw/job/?jobno=5mnd9&jobsource=n104bank1"
resp = requests.get(job_link)
sjob_page = BeautifulSoup(resp.text)
# job_content = job_page.select_one("#job").find("div", {"class": 'content'}).p.text.strip().replace('\r', '')
job_update_date = re.findall('<time class="update">更新日期：(.+?)</time>', resp.text)
update_date = dt.datetime.strptime(str(job_update_date[0]), '%Y-%m-%d').date()


text ='''<dt>其他條件：<\/dt>
                               		                                		<dd>(.+?)</dl>'''
skill = re.findall(text, resp.text)

print(update_date)
print(resp.text)
print(skill)