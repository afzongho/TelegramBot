from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import time
import re
import schedule

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException

from requests.auth import HTTPBasicAuth

from bs4 import BeautifulSoup

def telegram_bot_sendtext(bot_message):

    #scorpio id
    #bot_chatID = '1140152048'
    #afzongho id
    #bot_chatID = '687764190'
    #OddMathBOTtom id
    bot_chatID = '@oddMathBottom'

    bot_token= '886538007:AAFi_q7N5MGPHP8H7OeV5YJtHHJEKrwerTs'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def main():
    url = "https://www.oddsmath.com/"

    idSelect = ["1"]#,"12","14","40"]

    for id in idSelect:

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
#ChromeDriverManager().install())
        driver.get(url + "login")
        myElem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'loginform-username')))
        myElem2 = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'loginform-password')))
        driver.find_element_by_id("loginform-username").send_keys("blereau95")
        driver.find_element_by_id("loginform-password").send_keys("Curry958827!")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div[2]/div/div/div/div/form/div[5]/button").click()
        time.sleep(10)
        a = driver.find_element_by_xpath('//*[@id="provider_id"]')
        # a = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[3]/div[2]/div/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[1]/select')
        select = Select(a)
        select.select_by_value(id)
        selectValue = select.first_selected_option.text
        time.sleep(5)
        b = driver.find_element_by_xpath('// *[ @ id = "interval"]')
        # a = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[3]/div[2]/div/div/div[2]/div[1]/div/table[1]/tbody/tr[1]/td[1]/select')
        select = Select(b)
        select.select_by_value("10")
        selectValuePeriod = select.first_selected_option.text
        time.sleep(5)

        en_tete = driver.find_element_by_id("table-dropping-odds")
        b = en_tete.get_attribute("outerHTML")
        soup = BeautifulSoup(b,"html.parser")
        tbody = soup.find("tbody")
        #txt = "Voici les drop sur " + selectValue + " sur les " + selectValuePeriod + " minutes:\n"
        txt = ""
        for i in tbody:
            #print(i)
            if (str(type(i)) != "<class 'bs4.element.NavigableString'>"):
                dropCell = i.findAll("td",{"class":"drop primary"})
                dropValue = dropCell[0].findAll("span","drop-percent")[0].contents[0]
                if (float(dropValue) >= 10):
                    #print(dropValue)
                    if (float(dropValue) <= 8):
                        signDrop = "-"
                    elif (float(dropValue) <= 15 and float(dropValue) > 8):
                        signDrop = "--"
                    else:
                        signDrop = "---"

                    ligue = i.findAll("td")[0].findAll("a")[0]["title"]
                    homeTeam = i.findAll("td",{"class":"homeTeam"})[0].findAll("a")[0].contents[0]
                    print(i.findAll("td",{"class":"awayTeam"})[0].findAll("a"))
                    awayTeam = i.findAll("td",{"class":"awayTeam"})[0].findAll("a")[0].contents[0]
                    regHome = re.compile(".*odds odds-1 odds-dropping.*")
                    regX = re.compile(".*odds odds-X odds-dropping.*")
                    regAway = re.compile(".*odds odds-2 odds-dropping.*")

                    homeOdd = i.findAll("td",{"class":regHome})[0].findAll("span",{"class":"drop-value-current"})[0].contents[0]
                    print(i.findAll("td",{"class":regX}))
                    print(i.findAll("td", {"class": regX})[0])
                    print(i.findAll("td",{"class":regHome})[0].findAll("span",{"class":"drop-value-current"}))
                    print(i.findAll("td",{"class":regHome})[0].findAll("span",{"class":"drop-value-current"})[0])
                    print(i.findAll("td",{"class":regHome})[0].findAll("span",{"class":"drop-value-current"})[0].contents)
                    print(i.findAll("td",{"class":regHome})[0].findAll("span",{"class":"drop-value-current"})[0].contents[0])
                    xOdd = i.findAll("td",{"class":regX})[0].findAll("span",{"class":"drop-value-current"})[0].contents[0]
                    awayOdd = i.findAll("td", {"class": regAway})[0].findAll("span", {"class": "drop-value-current"})[0].contents[0]
                    print(i.findAll("td",{"class":regHome})[0]["class"])

                    if (any("drop-" in s for s in i.findAll("td",{"class":regHome})[0]["class"])):
                        msg = "ligue : " + ligue + "\n" + \
                              "Home : " + homeTeam + "\n" + \
                              "Away : " + awayTeam + "\n" + \
                              "1 : " + homeOdd + " " + signDrop +  "\n" + \
                              "X : " + xOdd + "\n" + \
                              "2 : " + awayOdd + "\n" + \
                              "Drop : " + dropValue
                        txt += "\n" + msg
                    elif (any("drop-" in s for s in i.findAll("td",{"class":regX})[0]["class"])):
                        msg = "ligue : " + ligue + "\n" + \
                              "Home : " + homeTeam + "\n" + \
                              "Away : " + awayTeam + "\n" + \
                              "1 : " + homeOdd + "\n" + \
                              "X : " + xOdd + " " + signDrop +  "\n" + \
                              "2 : " + awayOdd + "\n" + \
                              "Drop : " + dropValue
                        txt += "\n" + msg
                    elif (any("drop-" in s for s in i.findAll("td",{"class":regAway})[0]["class"])):
                        msg = "ligue : " + ligue + "\n" + \
                              "Home : " + homeTeam + "\n" + \
                              "Away : " + awayTeam + "\n" + \
                              "1 : " + homeOdd + "\n" + \
                              "X : " + xOdd + "\n" + \
                              "2 : " + awayOdd + " " + signDrop +  "\n" + \
                              "Drop : " + dropValue
                        txt += "\n" + msg
                    print("------")
                    print("ligue : " + ligue)
                    print("Home : " + homeTeam)
                    print("Away : " + awayTeam)
                    print("1 : " + homeOdd)
                    print("X : " + xOdd)
                    print("2 : " + awayOdd)
                    print("Drop : " + dropValue)
            #'886538007:AAFi_q7N5MGPHP8H7OeV5YJtHHJEKrwerTs'


        driver.close()
        driver.quit()
        if (len(txt) > 1):
            #test = telegram_bot_sendtext("Voici les drop sur " + selectValue + " on " + selectValuePeriod + " :\n" + txt)
            print("Voici les drop sur " + selectValue + " on " + selectValuePeriod + " :\n" + txt)


try:
	print("debut traitement")
	schedule.every(8).minutes.do(main)
	print("fin traitement")

except:
    print("error")


while True:
    schedule.run_pending()
    time.sleep(1)
