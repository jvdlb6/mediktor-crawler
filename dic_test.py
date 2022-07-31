from re import T
import unicodedata
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json


url = "https://www.mediktor.com/pt-br/doenca/assaduras-fralda-pediatria?conclusionId=2ba50c2f-73e9-415b-99be-55da9ffd21c7"
option = Options()
option.headless = True
driver = webdriver.Chrome(options=option)
driver.get(url)
time.sleep(10)


def normalizeString(string: str) -> str:
    normalized = unicodedata.normalize('NFD', string)
    return normalized.encode('ascii', 'ignore').decode('utf-8')


doencas = []
doencas = {}

nome = driver.find_element(By.XPATH,
                           "//div[@class='mdk-conclusion-detail__main-title']"
                           ).text
desc = driver.find_element(By.XPATH,
                           "//div[@class='mdk-conclusion-detail__main-description']"
                           ).text.splitlines()

epidem = driver.find_element(By.XPATH,
                             "//div[@class='mdk-ui-card__content']"
                             ).text.splitlines()

sintomas = driver.find_element(By.XPATH,
                               "//div[@class='mdk-ui-card mdk-ui-card--overflow']"
                               ).text.splitlines()

fat_relac = driver.find_element(By.XPATH,
                                "(//div[@data-qa-ta='cardContentEl'])[3]"
                                ).text.splitlines()

espec = driver.find_element(By.XPATH,
                            "(//div[@class='mdk-ui-card__content'])[4]"
                            ).text


doencas['url'] = url
doencas['Nome'] = nome
doencas['Descricao'] = normalizeString(str(desc))
doencas['Epidemiologia'] = normalizeString(str(epidem))
doencas['Sintomas'] = normalizeString(str(sintomas))
doencas['Fatores Relacionados'] = normalizeString(str(fat_relac))
doencas['Especialidades associadas'] = normalizeString(str(espec))

json_object = json.dumps(doencas, indent=5)
with open("doencas.json", "w") as outfile:
    outfile.write(json_object)

driver.quit()
