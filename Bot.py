from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from selenium.common.exceptions import NoSuchElementException
import time
import pickle
from playsound import playsound
from selenium.webdriver.firefox.options import Options



def get_user(driver):
    user = driver.find_element_by_xpath('//span[@title = "XII A"]')
    user.click()
    return  user, driver

def read_last_in_message(user, driver):
    """
    Reading the last message that you got in from the chatter
    """
    for messages in driver.find_elements_by_xpath("//div[contains(@class,'message-in')]"):
        try:
            message = ""
            emojis = []

            message_container = messages.find_element_by_xpath(".//div[@class='copyable-text']")

            message = message_container.find_element_by_xpath(".//span[contains(@class,'selectable-text invisible-space copyable-text')]").text
        
            for emoji in message_container.find_elements_by_xpath(".//img[contains(@class,'selectable-text invisible-space copyable-text')]"):
                emojis.append(emoji.get_attribute("data-plain-text"))

        except NoSuchElementException:  # In case there are only emojis in the message
            try:
                message = ""
                emojis = []
                message_container = messages.find_element_by_xpath(".//div[@class='copyable-text']")

                for emoji in message_container.find_elements_by_xpath(".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
                ):
                    emojis.append(emoji.get_attribute("data-plain-text"))
            except NoSuchElementException:
                pass

    return message, emojis


def main():
    url = "https://web.whatsapp.com"
    driver = webdriver.Firefox()
    
    driver.get(url)
    input("Scan QR code and Press Enter to Start the BOT")
    previous_in_message = None
    user, driver = get_user(driver)
    while True:
        last_in_message, emojis = read_last_in_message(user, driver)
        if previous_in_message != last_in_message:
            print(last_in_message, emojis)
            keyword_list = ['zoom', 'attendance', 'meeting time', 'link', 'join', 'call', 'https:']
            check = False
            previous_in_message = last_in_message
            for item in keyword_list:
                if item in last_in_message.lower():
                    check = True
                    break
            if check:
                playsound('alert.mp4')

        time.sleep(1)


if __name__ == '__main__':
    main()
