# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 23:01:01 2022

@author: GEFORCE I7
"""
from itemloaders import ItemLoader
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Articulo(Item):
    titulo = Field()
    precio = Field()


 
 
class Mercadolibre(CrawlSpider):
    name = "Scrap-MercadoLibre"
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 2
    
    }
 
    download_delay = 2
 
    allowed_domains = ["listado.mercadolibre.com.co","articulo.mercadolibre.com.co","mercadolibre.com.co"]
 
    start_urls = ["https://listado.mercadolibre.com.co/construccion-materiales-obra#D[A:construccion-materiales-obra]"]
 
    rules = (
        # Paginacion
        Rule(
            LinkExtractor(
                allow=r'_Desde_'
            ),follow=True
        ),
        #Detalles de los productos
        Rule(
            LinkExtractor(
                allow=r'/MCO-'
            ), follow=True, callback='parse_items'
        ),
    )
 
    def Limpiartext(self, texto):
        nuevotext = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return nuevotext
 
    def parse_items(self, response):
        sel = Selector(response)
        item = ItemLoader(Articulo(), sel)
        item.add_xpath('titulo', '//h1/text()',MapCompose(self.Limpiartext))
        item.add_xpath('precio', '//span[@class="price-tag-fraction"]/text()') 
        yield item.load_item()