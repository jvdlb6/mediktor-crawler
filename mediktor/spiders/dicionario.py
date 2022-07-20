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
        url = "https://www.mediktor.com/pt-br/glossario"
        option = Options()
        option.headless = True
        driver = webdriver.Chrome(options=option)
        driver.get(url)
        time.sleep(10)

        doencas = driver.find_elements(
            By.XPATH, "//a[@class='mdk-dictionary-list__glossary-item']")
        urls = []
        for link_el in doencas:
            url = link_el.get_attribute('href')
            urls.append(url)
        print(urls)
        driver.quit()


# for link in element:
#        yield response.follow(link.get(), callback=self.parse_informacoes)

# def parse_informacoes(self, response):
#    descricao = response.XPATH(
#        "//div[@class= 'mdk-conclusion-detail__main-description']")
#    descricao.css("p::text").get()
