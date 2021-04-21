import json

import scrapy

from scrapy.loader import ItemLoader

from ..items import AlhilalbankaeItem
from itemloaders.processors import TakeFirst


class AlhilalbankaeSpider(scrapy.Spider):
	name = 'alhilalbankae'
	start_urls = ['https://www.alhilalbank.ae/en/news/newsjson.json']

	def parse(self, response):
		data = json.loads(response.text)
		for nii in data:
			for year in nii:
				for post in nii[year]:
					if post:
						url = post['link']
						title = post['title']
						date = post['date']
						yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, date, title):
		description = response.xpath('//div[@class="c-cms-content -article-content"]//text()[normalize-space() and not(ancestor::a[text()="Read Full Story"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=AlhilalbankaeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
