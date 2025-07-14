import scrapy
import json
from ..items import McItem
from scrapy.http import HtmlResponse

class McSpiderSpider(scrapy.Spider):
    name = "mc_spider"
    allowed_domains = ["mcdonalds.com"]
    start_urls = ["https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"]

    def parse(self, response:HtmlResponse):
        product_ids = response.css('li.cmp-category__item::attr(data-product-id)').getall()
        for pid in product_ids:
            url = f"https://www.mcdonalds.com/dnaapp/itemDetails?country=UA&language=uk&showLiveData=true&item={pid}"
            yield scrapy.Request(url, callback=self.product_pars)

    def product_pars(self, response:HtmlResponse):
        data = response.json()
        data_item = data["item"]
        data_nutrient_facts = data_item["nutrient_facts"]
        data_nutrient = data_nutrient_facts["nutrient"]
        item = McItem()
        item["name"] = data_item["item_name"]
        item["description"] = data_item["description"]
        item["calories"] = data_nutrient[2]["value"]
        item["fats"] = data_nutrient[3]["value"]
        item["carbs"] = data_nutrient[5]["value"]
        item["proteins"] = data_nutrient[7]["value"]
        item["unsaturated_fats"] = data_nutrient[4]["value"]
        item["sugar"]=data_nutrient[6]["value"]
        item["salt"] = data_nutrient[8]["value"]
        item["portion"] = data_nutrient[0]["value"]
        yield item