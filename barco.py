from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import numpy as np
from selenium.common.exceptions import NoSuchElementException

def main():
    s = Service(r"/Users/chenyufan/PycharmProjects/chromedriver")
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    url ='https://www.barco.com/en/clickshare/support/warranty-info'
    driver.get(url)
    cookie(driver)
    textbox(driver)
    driver.close()

def cookie(driver):
    #check accept all cookie
    cookie_btn = driver.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']")
    cookie_btn.click()

def textbox(driver):
    #element
    serial_textbox = driver.find_element(By.XPATH,"//*[@id='SerialNumber']")
    Getinfo_btn = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/section/div/div[1]/div/div[2]/div[1]/div[2]/button")

    for i in range(1,10):
        print('===test case '+str(i)+'===')
        # input_content
        text = np.random.choice(['1863552437', '123', '186355243a', '!@#4', '186355243!','1863552417'])

        # step1: input content
        print('step1: insert the serial number with ' + text)
        serial_textbox.clear()
        serial_textbox.send_keys(text)
        # step2: click Get info button
        print('step2: click button')
        driver.implicitly_wait(8)
        Getinfo_btn.click()
        # wait
        driver.implicitly_wait(8)
        # step4: check corresponding result
        print('step3: verification')
        result_verification(driver, text)


def result_verification(driver,text):
    #case1: length<6
    if len(text) < 6:
        print('(verification: check length<6)')
        expectedMessage = 'Minimum 6 characters required'
        error_hint = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/section/div/div[1]/div/div[2]/div[1]/div[1]/span[2]")
        error_msg = error_hint.text
        driver.implicitly_wait(8)
        if error_msg == expectedMessage:
            print('Correct! the error msg is '+ error_msg)

    #case2: invalid text
    elif len(text) > 6 and text != '1863552437':
        wrong_srl = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/section/div/div[2]/div/div/div/div/p")
        cannot_find_product_msg = 'We couldn\'t find a product with this serial number. Please double-check the serial number and try again.'
        driver.implicitly_wait(8)
        if len(text) == 10 :
            print('(verification: check correct length with empty information content)')
            print('sorry! you get correct length of serial number, but i only have 1863552437 device info to do valification.')
        elif wrong_srl.text == cannot_find_product_msg:
            print('(verification result: check error input)')
            print('Correct! ' + wrong_srl.text + 'is equal to ' + cannot_find_product_msg)

    #case3: correct device
    elif len(text) == 10 and text == '1863552437':
        print('(verification: check 1863552437 device information content)')
        devic_info = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/section/div/div[2]/div/div/article/div/div/div[2]")
        devic_1863552437_info = ['Description','CLICKSHARE CX-50 SET NA','Part number', 'R9861522NA', 'Delivery date','05/07/2020 00:00:00','Installation date','09/28/2020 00:00:00', 'Warranty end date', '09/27/2021 00:00:00','Service contract end date', '01/01/0001 00:00:00']
        devic_info = devic_info.text.split('\n')
        for i in range(len(devic_info)):
            driver.implicitly_wait(8)
            if devic_info[i] == devic_1863552437_info[i]:
                print('Correct! '+devic_info[i]+' is equal to '+devic_1863552437_info[i])



if __name__ == '__main__':
    main()





