from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys,os
from random import randint
import csv
from config import message
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options


loading_sleep = 30


def contactsData():
    
    filename=input("Enter the file name where all the contacts are stored: ")
    phone_numbers = []
    names = []
    # filename = sys.argv[1]
    with open(filename,"r",encoding='utf8') as f:
        rawData = csv.reader(f,delimiter=",",lineterminator="\n")
        
        for i in rawData:
            phone_numbers.append(i[1])
            names.append(i[0])
    return phone_numbers,names

def completed_till()->int:

    try:
        with open("count.txt","r",encoding="utf8") as f:
            done_till_counter = f.read()
            if(done_till_counter.strip()==""):
                raise IOError
            
            done_till_counter = int(done_till_counter)



    except (FileNotFoundError,IOError):
        with open("counter.txt","w",encoding="utf8") as f:
            done_till_counter = 0
            f.write("0")
        
    return done_till_counter

def sendMsg(phone_numbers,names):
        
    # auto install chromedriver/ make sure to delete the old chromedriver
    chromedriver_autoinstaller.install()
    
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={os.path.join(os.getcwd(),'Selenium')}") 

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('http://web.whatsapp.com')
    sleep(20)
    try:
        while(True):
            WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.CLASS_NAME,"_2UwZ_")))
            # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/div/div/div/div/div[1]/div")))

            print("Please scan the code")
            sleep(4)
    except:
        print("Scan Done")
        pass

    print(phone_numbers)
    print(names)

    for i in range(completed_till(),len(phone_numbers)):
        
        counter_file = open("counter.txt","w",encoding="utf8")
        phone_numbers[i]
        driver.get(f'https://web.whatsapp.com/send?phone=+{phone_numbers[i]}')

        try:
            for key in message:
                
                if(key.split(",")[0]=="message"):
                    
                    message_ = message[key].replace("<name>",names[i])

                    type_box = WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]")))
                    
                    message_lines = message_.split("\n")
                    for message__ in message_lines:
                        type_box.send_keys(message__+Keys.SHIFT+Keys.ENTER)
                        sleep(randint(1,5))
                    # send
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"))).send_keys(Keys.RETURN)


                elif(key.split(",")[0]=="media"):
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div"))).click()
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input"))).send_keys(os.path.join(os.path.abspath("assets"),message[key]))
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div"))).click()
                                                                                    
                
                elif(key.split(",")[0]=="document"):
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div"))).click()
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[4]/button/input"))).send_keys(os.path.join(os.path.abspath("assets"),message[key]))
                    WebDriverWait(driver,loading_sleep).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div"))).click()
                                                

                else:
                    print("wrong key passed")
                    continue
                
                sleep(randint(3,5))
            
            sleep(randint(10,20))
            print("done for",names[i])

        except Exception as e:
            print(f"Failed for Number {names[i]}")
        finally:
            counter_file.write(f"{i+1}")
    


[phone_numbers,names] = contactsData() 
sendMsg(phone_numbers,names)
