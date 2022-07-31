import time
import unicodedata
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

url = "https://www.mediktor.com/pt-br/glossario"
option = Options()
option.headless = True
driver = webdriver.Chrome(options=option)
driver.get(url)
time.sleep(10)

# Caminho para os links
el_links = driver.find_elements(
    By.XPATH, "//a[@class='mdk-dictionary-list__glossary-item']")

# declarando dicionarios
urls = []
nome_doenca = []
desc = []
epidem = []
sintomas = []
fat = []
espec = []
doenca_info = []
doenca_info = {}


# func para remover ç e acentos

def normalizeString(string: str):
    normalized = unicodedata.normalize('NFD', string)
    return normalized.encode('ascii', 'ignore').decode('utf-8')


# capturando as urls e guardando no dicionario urls #
for i in range(len(el_links)):
    urls.append(el_links[i].get_attribute('href'))

    # seguindo cada url dentro do dicionario e
    # crawleando as informações necessárias
for link in urls:

    driver.get(link)
    print(link)
    waitReturn = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH,
                                        "//div[@class='mdk-conclusion-detail__main-title']"
                                        )))
    nome_source = driver.find_element(By.XPATH,
                                      "//div[@class='mdk-conclusion-detail__main-title']"
                                      ).text
    try:
        epidem_source = driver.find_element(By.XPATH,
                                            "//div[@class='mdk-ui-card__content']"
                                            ).text.splitlines()
    except NoSuchElementException:
        epidem.append('Nao possui Epidemiologia.')
        pass
    try:
        sintomas_source = driver.find_element(By.XPATH,
                                              "//body[1]/div[1]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]"
                                              ).text.splitlines()
    except NoSuchElementException:
        sintomas.append('Nao possui Sintomas.')
        pass

    try:
        fat_source = driver.find_element(By.XPATH,
                                         "(//div[@data-qa-ta='cardContentEl'])[3]"
                                         ).text.splitlines()
    except NoSuchElementException:
        fat.append('Nao possui Fatores Relacionados.')
        pass

    try:
        espec_source = driver.find_element(By.XPATH,
                                           "(//div[@class='mdk-ui-card__content'])[4]"
                                           ).text.splitlines()
    except NoSuchElementException:
        espec.append('Nao possui Especialidades.')
        pass

    try:
        desc_source = driver.find_element(By.XPATH,
                                          "//div[@class='mdk-conclusion-detail__main-description']"
                                          ).text.splitlines()
    except NoSuchElementException:
        desc.append(normalizeString(str('Nao possui Descricao.')))
        pass

    # povoando os arrays com a função para remover ascii

    desc.append(normalizeString(str(desc_source)))
    epidem.append(normalizeString(str(epidem_source)))
    sintomas.append(normalizeString(str(sintomas_source)))
    nome_doenca.append(normalizeString(str(nome_source)))
    fat.append(normalizeString(str(fat_source)))
    espec.append(normalizeString(str(espec_source)))
    # povoando o dicionario

    doenca_info['url'] = url
    doenca_info['Nome'] = nome_doenca
    doenca_info['Descricao'] = desc
    doenca_info['Epidemiologia'] = epidem
    doenca_info['Sintomas'] = sintomas
    doenca_info['Fatores relacionados'] = fat
    doenca_info['Especialidades'] = espec

    driver.back()
# criando arquivo json

json_object = json.dumps(doenca_info, indent=5)
with open("doencas.json", "w") as outfile:
    outfile.write(json_object)
df = pd.DataFrame(doenca_info, index=[' '])
df.to_csv('doencas.csv', sep='\t', encoding='utf-8')
driver.quit()
