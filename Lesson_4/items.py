# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AutoyoulaParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HHVacancyItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    company_url = scrapy.Field()


class EmployerItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    emp_name = scrapy.Field()
    area_of_activity = scrapy.Field()
    emp_description = scrapy.Field()
    emp_vacancy_offer = scrapy.Field()