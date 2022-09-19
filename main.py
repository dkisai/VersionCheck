import os
import msvcrt
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException


def login_gbc():
    usr = driver.find_element(By.XPATH, '//*[@id="user"]')
    usr.send_keys(config['TEST']['GBC_USER'])
    psw = driver.find_element(By.XPATH, '//*[@id="password"]')
    psw.send_keys(config['TEST']['GBC_PASSWORD'] + Keys.RETURN)


def planta_info(ip):
    menu = driver.find_element(By.XPATH, '/html/body/nav/div/div[1]/a/i/img')
    menu.click()
    version = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(By.XPATH, '/html/body/div[2]/ul/li[1]/div/a[4]/h6/b').text)
    planta = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(By.XPATH, '//*[@id="slide-out"]/li[1]/div/a[3]/h6/b').text)
    imagen = "./Screenshot/" + planta[8:] + ".png"
    driver.save_screenshot(imagen)
    print(ip + " " + planta[8:] + " " + version[22:])


if __name__ == "__main__":
    driver_options = Options()
    driver_options.add_argument('--headless')
    driver_options.add_argument('--no-sandbox')
    driver_options.add_argument('log-level=3')
    driver = webdriver.Chrome(executable_path='chromedriver', options=driver_options)
    driver.set_window_size(800, 800)
    if os.path.isdir('./Screenshot') == False:
        os.mkdir('./Screenshot')
    config = configparser.ConfigParser()
    config.read('config.ini')
    with open("plantas.txt") as file:
        for line in file:
            url = "http://" + line[:-1] + config['TEST']['GBC_LOGIN']
            url_logout = "http://" + line[:-1] + config['TEST']['GBC_LOGOUT']
            try:
                driver.get(url)
            except WebDriverException:
                print(line[:-1] + " WebDriver ERROR ")
                continue
            try:
                login_gbc()
                planta_info(line[:-1])
            except NoSuchElementException:
                print(line[:-1] + " NoSuchElement ERROR")
                continue
            driver.get(url_logout)
        driver.quit()
    file.close()
    print("Presione una tecla para terminar...")
    msvcrt.getch()