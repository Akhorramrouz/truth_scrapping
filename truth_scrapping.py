#!/usr/bin/env python
# coding: utf-8

# In[1]:


user = "observerAdel"
password = "@Del1654"



from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import time



class Truth:
    def __init__(self,author,id_,date,text):
        self.author = author
        self.id = id_
        self.text = text
        self.date = date
        
        

def sign_in(driver, username, password):
    driver.get("https://truthsocial.com/login")
    driver.implicitly_wait(2)
    driver.find_element(By.NAME,'username').send_keys(username)
    driver.find_element(By.NAME,'password').send_keys(password)

    for t in driver.find_elements(By.TAG_NAME,'button'):
        if t.text == 'Accept':
            t.click()
      
    for t in driver.find_elements(By.TAG_NAME,'button'):
        if t.text == "Sign in":
            print(t.text)
            t.click()
            
            
            

def truth_reply_parser(html):
    list_truths = []
    soup = BeautifulSoup(html,'html.parser')
    truths = soup.find_all(attrs={'data-id': True})
    for truth in truths:
        truth_id = truth['data-id']
        truth_author = truth.text.split("@")[1].split("·")[0]
        truth_text = truth.text
        truth_date = truth.text.split("@")[1].split("·")[1].split("Replying")[0]
        list_truths.append(Truth(truth_author, truth_id, truth_date, truth_text))
    
    return list_truths




def get_link(author, post_id):
    return f"https://truthsocial.com/@{author}/posts/{post_id}"


driver = webdriver.Chrome()
sign_in(driver,user,password )


# In[10]:


# df_truths['links'] = get_link(df_truths.author, df_truths.id)
# df_truths


# # Make Sure to Zoom out to 25%
# 

# In[17]:


df = pd.read_csv('trump.csv',index_col=0)
counter = 0
last_height = 0
list_truths = []

for j in range(len(df)):
    if f"{df.iloc[j].id}.csv" in os.listdir():
        print("I have already done this Truth")
        continue


    if j%40==39:
        print("I am going to sleep for 30 minutes")
        time.sleep(30*60)

    driver.get(df.iloc[j].links)
    for i in range(100):
        if i%51 == 50:
            print(i)
            print(len(list_truths))
            print("----------------")
            time.sleep(3)


        try:
            sub_list_truths = truth_reply_parser(driver.page_source)
            for truth in sub_list_truths:
                list_truths.append(truth)

        except:
            # print("Error")
            time.sleep(1)


        finally:     
            driver.execute_script(f"window.scrollTo(0, {counter*2160+1080})")
            counter += 1
            time.sleep(2)
            if driver.execute_script("return document.body.scrollHeight") == last_height:
                time.sleep(3.5)
                driver.execute_script(f"window.scrollTo(0, {counter*2160+1080+540})")
                if driver.execute_script("return document.body.scrollHeight") == last_height:
                    print("I have all i needed from this Truth")
                    break

            last_height = driver.execute_script("return document.body.scrollHeight")
            
            if i%5==4:
                l = []
                for t in list_truths:
                    l.append({
                        'date':t.date,
                        'author':t.author,
                        'text':t.text,
                        'id':t.id
                    })
                df_truths = pd.DataFrame(l).drop_duplicates().reset_index(drop=True)
                # print("------------------------>>>>>  ",len(df_truths))
                if len(df_truths) > 100:
                    print("I have more than 100 comments on this Truth")
                    print("*******************************************")
                    break
                        
        
    df_truths = pd.DataFrame(l).drop_duplicates().reset_index(drop=True)
            
    l = []
    for t in list_truths:
        l.append({
            'date':t.date,
            'author':t.author,
            'text':t.text,
            'id':t.id
        })
        
    df_truths = pd.DataFrame(l).drop_duplicates().reset_index(drop=True)
    df_truths.to_csv(f"{df.iloc[j].id}.csv")
    list_truths = []




