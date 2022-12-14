import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    etalon = 'https://www.amayama.com'
    count = 0
    allowed_domains = ['amayama.com']
    file = open('Links.txt')
    start_urls = file.read().split()
    print(len(start_urls))


    def parse(self, response, **kwargs):

        c = response.css('.market a::attr(href)').extract()
        y = response.css('td[width="25%"] a::attr(href)').extract()
        c+=y
        for i in c:
            if 'http' in i:
                yield scrapy.Request(i, callback=self.parse3)
            else:
                yield scrapy.Request(self.etalon + i, callback=self.parse3)

    def parse3(self,response, **kwargs):
        c = response.css('.table a::attr(href)').extract()


        for i in c:
            if 'http' in i:
                yield scrapy.Request(i, callback=self.parse4)
            else:
                yield scrapy.Request(self.etalon + i, callback=self.parse4)
    def parse4(self,response, **kwargs):
        c = response.css('table[border="0"] a::attr(href)').extract()


        for i in c:
            if 'http' in i:
                yield scrapy.Request(i, callback=self.parse5)
            else:
                yield scrapy.Request(self.etalon + i, callback=self.parse5)
    def parse5(self,response, **kwargs):
        c = response.css('.colmask_wide a::attr(href)').extract()


        for i in c:
            if 'http' in i:
                yield scrapy.Request(i, callback=self.parse6)
            else:
                yield scrapy.Request(self.etalon + i, callback=self.parse6)
    def parse6(self,response, **kwargs):
        c = response.css('map[name="map1"] area::attr(href)').extract()



        for i in c:
            if 'http' in i:
                yield scrapy.Request(i, callback=self.parse7)
            else:
                yield scrapy.Request(self.etalon + i, callback=self.parse7)
    def parse7(self,response, **kwargs):
        c = response.css('.priceRangeContainer a::attr(href)').extract()
        for i in c:
            if 'http' in i:
                yield scrapy.Request(i, callback=self.final)
            else:
                yield scrapy.Request(self.etalon + i, callback=self.final)
                
    def final(self,response,**kwargs):
        self.count = 0
        for line in response.css('.part-table__body  tr'):
            if(line.css('.warehouse-name::text').extract_first('').strip()=='????????????' and self.count==0):
                self.count+=1
                items={
                    '????????????': response.url,
                    '????????????????': response.css('body > div.mainTable > div > div.part-page.part-page_redesign2018.part-page_ru > div.part-page__header > div.part-page__name > h1::text').extract_first('').strip(),
                    '??????????': response.css('body > div.mainTable > div > div.part-page.part-page_redesign2018.part-page_ru > div.part-page__header > div.part-page__compact-info > div.part-page__number::text').extract_first('').strip(),
                    '????????????': line.css('.warehouse-name::text').extract_first('').strip(),
                    '????????': line.css('.part-price::text').extract_first('').strip(),
                    '??????': line.css('td>span[data-type="weight"]::text').extract_first('').strip(),
                    '??????????????':line.css('.part-quantity::text').extract_first('').strip(),
                    '????????1':'',
                    '????????2':'',
                    '????????3': '',
                    '????????4': '',
                    '????????5': '',

                    #'????????????????1': response.css('.fitness__row>span::text').extract(),
                    #'????????????????': response.css('.item::text').extract(),

                 }
                lp= response.css('#fitness-table > div:nth-child(1) > div.fitness__row-content > div > span::text').extract()
                items.update({"????????????????1": lp})
                sp=response.css('.item::text').extract()
                for i in range(len(sp)):
                    sp[i]=''.join(sp[i].split())
                    if(sp[i]=='??????'):
                        sp[i]=''
                sp = list(filter(None,sp))
                items.update({"????????????????2":sp})
                photo =response.css('.part-page__gallery img::attr(src)').extract()
                for i in range(len(photo)):
                    items.update({"????????"+str(i+1):photo[i]})


                yield items






























