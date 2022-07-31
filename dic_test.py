import unicodedata
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json


url = "https://www.mediktor.com/pt-br/doenca/ataxia-cerebelar-aguda-pos-infecciosa-pediatria?conclusionId=958d85bf-e96a-4487-ab63-5772a6204661"
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
                               "//body[1]/div[1]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]"
                               ).text.splitlines()

fat_relac = driver.find_element(By.XPATH,
                                "(//div[@data-qa-ta='cardContentEl'])[3]"
                                ).text.splitlines()

espec = driver.find_element(By.XPATH,
                            "(//div[@class='mdk-ui-card__content'])[4]"
                            ).text.splitlines()
doencas['url'] = url
doencas['Nome'] = normalizeString(str(nome))
doencas['Descricao'] = normalizeString(str(desc))
doencas['Epidemiologia'] = normalizeString(str(epidem))
doencas['Sintomas'] = normalizeString(str(sintomas))
doencas['Fatores Relacionados'] = normalizeString(str(fat_relac))
doencas['Especialidades associadas'] = normalizeString(str(espec))

json_object = json.dumps(doencas, indent=5)
with open("doencas.json", "w") as outfile:
    outfile.write(json_object)
df = pd.DataFrame(doencas, index=[' '])
df.to_csv('doencas.csv', sep='\t', encoding='utf-8')
driver.quit()
