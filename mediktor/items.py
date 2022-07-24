# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediktorItem(scrapy.Item):
    nome = scrapy.Field()
    descricao = scrapy.Field()
    epidem = scrapy.Field()
    sintomas = scrapy.Field()
    fatores_rel = scrapy.Field()
    especialidades = scrapy.Field()
    url = scrapy.Field()
