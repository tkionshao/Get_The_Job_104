from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import json
import datetime as dt
import re

def getTheJobBy104(url):
    # Prepare headers and filename
    date = dt.date.today()
    filename =  'data_engineer_'+str(date)+'.csv'

    headers = json.loads(r'''{
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "referer": "https://www.104.com.tw/jobs/search/?keyword=Python&jobsource=n104bank1&ro=0&order=1"
    }''')

    # Request
    response = requests.get(url)

    html = BeautifulSoup(response.text)
    jobs = html.find_all("article",{"class":"job-list-item"})

    i = 0
    df = pd.DataFrame(columns=['name', 'company', 'address', 'link','content','update'])
    for job in jobs:
        # Parsing
        name = job['data-job-name']
        company = job["data-cust-name"]
        job_page_link = "http:"+job.find("a",{"target":"_blank"})["href"]

        try:
            # Request
            # To get job page's link and parsing address,
            response = requests.get(job_page_link)
            single_company = BeautifulSoup(response.text)
            # Parsing
            addresses = single_company.find("dl").find_all("dd")[3].strings
            address = list(addresses)[0].strip()
            job_page_link = "http:" + job.find("a", {"class": "js-job-link"})["href"]

            # Parsing contents and update
            # Request
            resp = requests.get(job_page_link, headers=headers)
            time.sleep(1)
            # Parsing
            job_page = BeautifulSoup(resp.text)
            job_content = job_page.select_one("#job").find("div", {"class": 'content'}).p.text.strip().replace('\r','')
            job_update_date = re.findall('<time class="update">更新日期：(.+?)</time>', resp.text)
            update_date = dt.datetime.strptime(str(job_update_date[0]), '%Y-%m-%d').date()

            # Append row-data to pandas dataframe
            s = pd.Series([name, company, address, job_page_link, job_content, update_date], \
                          index=['name', 'company', 'address', 'link', 'content', 'update'])
            df = df.append(s, ignore_index=True)

            # Confirm the progression.
            i += 1
            print(job_page_link, 'is done.')
            time.sleep(3)

        # Trouble logs.
        except:
            with open("ErrorLog.txt",'a') as f:
                f.write("Somthing Wrong in single job page." + '\n' + "This is happened at link " + \
                    str(i) + '\n' + "Link as : " + job_page_link + "\n" + str(dt.datetime.now()) + "\n" * 2)
            print(job_page_link, '<--------- was fail.')

    # Output Datafram to csv
    df.to_csv(filename, mode='a', encoding='utf-8', index=False,header=False)

    # Confirm the progression.
    print("Total:",len(jobs),'confirm number: ',i)
    #return len(jobs)

# This is for counting the pages we have to finish
def totalPage(url):s
    response = requests.get(url)
    total_pages = int(re.findall('"totalPage":(\d+),"totalCount"', response.text)[0])
    return total_pages

if __name__ == '__main__':

    first_url = "https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007000000&keyword=%E8%B3%87%E6%96%99%E5%B7%A5%E7%A8%8B&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=n104bank1"
    endPage = totalPage(first_url)
    print('Total pages has to be parsed: ', endPage)

    url_for_change = "https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007000000&keyword=%E8%B3%87%E6%96%99%E5%B7%A5%E7%A8%8B&area=6001001000&order=1&asc=0&page={}&mode=s&jobsource=n104bank1"
    startPage = 1

    for page in range(startPage,endPage):
        print('page',page,'start parsing')
        url = url_for_change.format(page)
        getTheJobBy104(url)
        print('page',page,'done!!')