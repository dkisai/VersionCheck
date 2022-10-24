import os
# import msvcrt
import csv
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
    image = "./Screenshot/" + planta[8:] + ".png"
    driver.save_screenshot(image)
    print(version[22:] + "," + planta[8:] + "," + ip)
    return [version[22:], planta[8:], ip]


def save_to_csv(version):
    # Open file in append mode
    with open('new-version.csv', 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer2 = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer2.writerow(version)


if __name__ == "__main__":
    header = ['version', 'planta', 'ip']
    with open('new-version.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
    print("version,planta,ip")
    driver_options = Options()
    driver_options.add_argument('--headless')
    driver_options.add_argument('--no-sandbox')
    driver_options.add_argument('log-level=3')
    driver = webdriver.Chrome(executable_path='chromedriver', options=driver_options)
    driver.set_window_size(800, 800)
    if not os.path.isdir('./Screenshot'):
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
                save_to_csv(planta_info(line[:-1]))
            except NoSuchElementException:
                print(line[:-1] + " NoSuchElement ERROR")
                continue
            driver.get(url_logout)
        driver.quit()
    file.close()
    # print("Presione una tecla para terminar...")
    # msvcrt.getch()
