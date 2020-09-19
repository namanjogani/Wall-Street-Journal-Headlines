# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which

class HeadlinesSpider(scrapy.Spider):
    name = 'headlines'
    allowed_domains = ['https://www.wsj.com/']
    start_urls = ['http://www.wsj.com/market-data/quotes/MSFT?mod=searchresults_companyquotes/']
    
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        chrome_path = which("chromedriver")

        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get('http://www.wsj.com/market-data/quotes/MSFT?mod=searchresults_companyquotes/')
        rur_tab = driver.find_element_by_id("latestNewsLoad")
        rur_tab.click()
        self.html = driver.page_source
        driver.close()
    def parse(self, response):
        resp = Selector(text=self.html)
        Headlines = resp.xpath("//ul[@class='WSJTheme--cr_newsSummary--2RNDoLB9 ']/li")
        for headline in Headlines:
            yield{
            'name':headline.xpath(".//a/text()").get(),
            'link':headline.xpath(".//span[@class='WSJTheme--headline--33gllX4Y ']/a/@href").get()
            }


