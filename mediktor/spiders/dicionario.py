import scrapy
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json


class DicionarioSpider(scrapy.Spider):
    name = 'dicionario'
    allowed_domains = ['www.mediktor.com']
    start_urls = ['http://www.mediktor.com/']

    def parse(self, response):
        url = "https://www.mediktor.com/pt-br/glossario"
        option = Options()
        option.headless = True
        driver = webdriver.Chrome(options=option)
        driver.get(url)
        time.sleep(10)

        # letra_click = driver.find_element(
        #     By.XPATH, "//button[normalize-space()='J']")
        # letra_click.click()

        el_links = driver.find_elements(
            By.XPATH, "//a[@class='mdk-dictionary-list__glossary-item']")
        urls = []
        nome_doenca = []
        #descricao, epidem, sintomas, fat_relac, espec = []

        # capturando as urls e guardando no dicionario urls
        for i in range(len(el_links)):
            urls.append(el_links[i].get_attribute('href'))

        # seguindo cada url dentro do dicionario e
        # crawleando as informações necessárias
        for link in urls:
            driver.get(link)

            myElem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//div[@class='mdk-conclusion-detail__main-title']"
                                                )))
            nome_source = driver.find_element(By.XPATH,
                                              "//div[@class='mdk-conclusion-detail__main-title']"
                                              ).text

            nome_doenca.append(nome_source)

            driver.back()
        print(nome_doenca)
        driver.quit()
