import scrapy
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json


class DicionarioSpider(scrapy.Spider):
    name = 'dicionario'
    allowed_domains = ['www.mediktor.com']
    start_urls = ['http://www.mediktor.com/']

    def parse(self, response):
        url = "https://www.mediktor.com/pt-br/doenca/abcesso-fistula-anal?conclusionId=128"
        option = Options()
        option.headless = True
        driver = webdriver.Chrome(options=option)
        driver.get(url)
        time.sleep(10)

        # nome_doenca = []

        nome_source = driver.find_element(By.XPATH,
                                          "//div[@class='mdk-conclusion-detail__main-title']"
                                          ).text
        SELETOR = driver.find_elements(
            By.XPATH, "//div[@class='mdk-conclusion-detail__main-description']")
        desc = []
        for p_tag in SELETOR:
            desc = {}
            desc['desc'] = (p_tag.find_element(By.XPATH,
                                               "//p").text)
        # nomes = nome_source.get_attribute('text')
        # nome_doenca.append(nomes)

        print(f'-------------{nome_source}---------')
        print(f'-------------{desc}---------')
        driver.quit()
