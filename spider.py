from scrapy import Spider
import urllib.request
from bs4 import BeautifulSoup
import re
import scrapy


class Foo(Spider):
    categories = dict()
    iterator = 1
    categories_iterator=1
    openCsv = open('produkty.csv', 'w', encoding="utf-8")
    kategorieCsv = open('kategorie.csv', 'w', encoding="utf-8")
    start_urls = ["https://www.bookbook.pl/sport-forma-fizyczna-2","https://www.bookbook.pl/literatura-piekna-proza-polska","https://www.bookbook.pl/komiksy","https://www.bookbook.pl/informatyka-internet-2","https://www.bookbook.pl/dramat","https://www.bookbook.pl/ksiazki-dla-dzieci"
                  ,"https://www.bookbook.pl/lektury-szkolne","https://www.bookbook.pl/romans","https://www.bookbook.pl/literatura-dla-dzieci",
                  "https://www.bookbook.pl/dom-2","https://www.bookbook.pl/dramat-2","https://www.bookbook.pl/literatura-obcojezyczna-2","https://www.bookbook.pl/humor-satyra-2",
                  "https://www.bookbook.pl/filmy","https://www.bookbook.pl/gry-komputerowe","https://www.bookbook.pl/nauka-jezykow-2","https://www.bookbook.pl/atlasy-i-przewodniki",
                  "https://www.bookbook.pl/figurki","https://www.bookbook.pl/puzzle","https://www.bookbook.pl/pojazdy","https://www.bookbook.pl/zabawki-do-kapieli",
                  "https://www.bookbook.pl/notatniki","https://www.bookbook.pl/torby-plecaki","https://www.bookbook.pl/naklejki",
                  "https://www.bookbook.pl/szkola-podstawowa-2","https://www.bookbook.pl/szkola-srednia","https://www.bookbook.pl/przedszkole-2"]

    name = "basic_spider"

    def __del__(self):
        self.kategorieCsv.close()
        self.openCsv.close()

    def getPrices(self,url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        script = soup.find_all('script')
        pattern = re.compile("'price'   : '(.*?)'")
        fields = []
        for scripts in script:
            # print(scripts.text)
            result = re.findall(pattern, scripts.text)
            if result != []:
                fields=result
        return(fields)

    def parse(self, response):
        Ksiazki_kategoria = response.xpath('//ul[contains(@class,"breadcrumb")]/li[2]/a/text()').get()
        Ksiazki_kategoria = Ksiazki_kategoria.replace('\t', '')
        Ksiazki_kategoria = Ksiazki_kategoria.replace('\n', '')
        Ksiazki_podkategoria = response.xpath('//div[contains(@class,"category-header page-header")]/h1[1]/text()').get()
        Ksiazki_podkategoria=Ksiazki_podkategoria.replace('\t','')
        Ksiazki_podkategoria=Ksiazki_podkategoria.replace('\n','')

        if self.categories.get(Ksiazki_kategoria) == None :
            self.categories[Ksiazki_kategoria]=self.categories_iterator
            self.kategorieCsv.write(str(self.categories_iterator) + ';' + Ksiazki_kategoria + '\n')
            self.categories_iterator =self.categories_iterator+1
        if self.categories.get(Ksiazki_podkategoria) == None:
            self.categories[Ksiazki_podkategoria] = self.categories_iterator
            self.kategorieCsv.write(str(self.categories_iterator) + ';' + Ksiazki_podkategoria + '\n')
            self.categories_iterator = self.categories_iterator + 1

        Ksiązki_liter_piekna_nazwy = response.xpath('//div[contains(@class,"product-box gallery gallery_100")]/a[contains(@class,"product-name")]/@title').getall()
            #'//body/div[@class="back"]/div[@class="wrap-content"]/div[1]/div[@class="row"]/section[1]/div[1]/div[@class="page-content"]/div[4]/ul[1]/li/div[1]/div[2]/a/@title').getall()
        Ksiazki_liter_piekna_autor = response.xpath('//div[contains(@class,"product-producer")]/a[1]/@title').getall()
         #   '//body/div[@class="back"]/div[@class="wrap-content"]/div[1]/div[@class="row"]/section[1]/div[1]/div[@class="page-content"]/div[4]/ul[1]/li/div[1]/div[3]/a[1]/@title').getall()
        Ksiazki_liter_piekna_zdjecie = response.xpath('//div[contains(@class,"product-box gallery gallery_100")]/div[contains(@class,"product-image")]/div[contains(@class,"preload-image")]/img[1]/@src').getall()
            #'//body/div[@class="back"]/div[@class="wrap-content"]/div[1]/div[@class="row"]/section[1]/div[1]/div[@class="page-content"]/div[4]/ul[1]/li/div[1]/div[2]/div[1]/img/@src').getall()

        Ksiazki_liter_piekna_cena = self.getPrices((response.request.url))
        #response.xpath('//body/script[contains(.,"dataLayerProducts.push")]/text()').getall()
            #'//body/div[@class="back"]/div[@class="wrap-content"]/div[1]/div[@class="row"]/section[1]/div[1]/div[@class="page-content"]/div[4]/ul[1]/li/div[1]/div[4]/span[2]/span[1]/text()').getall()

        for i in range(0,len(Ksiązki_liter_piekna_nazwy)):
            self.openCsv.write(str(self.iterator)+';'+Ksiązki_liter_piekna_nazwy[i]+';'+Ksiazki_liter_piekna_autor[i]+';'+Ksiazki_liter_piekna_zdjecie[i]+
                        ';'+Ksiazki_liter_piekna_cena[i]+';'+str(self.categories[Ksiazki_kategoria])+','+str(self.categories[Ksiazki_podkategoria])+',0\n')
            self.iterator = self.iterator+1
