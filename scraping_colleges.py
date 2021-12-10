# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.selector import Selector
import time

base_url = 'https://nces.ed.gov/COLLEGENAVIGATOR/'


class CollegesDataSpider(scrapy.Spider):
    base_url = 'https://nces.ed.gov/COLLEGENAVIGATOR/'
    name = "collegedata"

    def start_requests(self):

        num_pages = 7
        urls = []
        index_url = 'https://nces.ed.gov/COLLEGENAVIGATOR/?s=all&sp=4&pg=' 
        for pg_id in range(1,num_pages):
            urls.append(index_url+str(pg_id))
        self.log(urls)
        """
        urls = [
            'https://nces.ed.gov/COLLEGENAVIGATOR/?s=all&sp=4&pg=1',
            'https://nces.ed.gov/COLLEGENAVIGATOR/?s=all&sp=4&pg=2',
        ]
        """
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("=")[-1]
        sel = Selector(response)
        filename = f'quotes-{page}.html'
        #print(f"response: {response}")
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        page_url_tables = "/html/body/div[1]/form/div[3]/div[2]/div[3]/div[3]/table/tbody"
        page_href_xpath = '/html/body/div[1]/form/div[3]/div[2]/div[3]/div[3]/table/tbody/tr[5]/td[2]/a'
        urls_table_xpath = '//*[@id="ctl00_cphCollegeNavBody_ucResultsMain_tblResults"]'
        self.log(response.xpath(urls_table_xpath).extract())
        table_data = response.xpath(urls_table_xpath).extract()
        #self.log(f"table_data : {table_data}")
        #trs = table_data.xpath('//tr').extract()
        #self.log(f"trs : {trs}")
        #Selector(text=body).xpath('//td/text()').get()
        links = Selector(text=str(table_data)).xpath('//td/a/@href').extract()
        #self.log(links)
        #Selector(text=body).xpath('//span/text()').get()
        #self.log(links)
        for link in links[:1]:
            page_url = base_url + str(link).strip()
            yield response.follow(url=page_url,callback=self.parse_college_page)

    def parse_college_page(self, response):
        self.log("*******parse_college_page*******")
        self.log(response)
        #data = Selector(response).css('.collegedash').extract()
        divs = response.xpath('//div')
        for span in divs.css('.collegedash'):
            # self.log(span.extract())
            #data = span.xpath('/div[2]').extract()
            #data = span.extract()
            #self.log(f"***{data}")
            """
            """
            address = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/span/text()').extract()
            # self.log(address)
            if isinstance(address,list) and len(address)>0:
                address = address[0]
                
                Name = ""

                Street = " ".join(str(address.split(',')[0]).split(' ')[1:])
                self.log(f"Street: {Street}")

                City = str(address.split(',')[1]).strip()
                self.log(f"City: {City}")

                State = str(address.split(',')[-1]).split(' ')[-2]
                self.log(f"State: {State}")
                
                Zip = str(address.split(',')[-1]).split(' ')[-1]
                self.log(f"Zip: {Zip}")

            data = response.xpath('//div').css('.collegedash').xpath('//table[1]').css('.layouttab')
            self.log(data.extract())
            phone = data.xpath('//tr[2]/td[2]').extract()
            #Phone = span.xpath('//table/tbody/tr[1]/td[2]')
            self.log(f"phone: {phone}")
            #self.log(data)

            #for table in tables.css('.layouttab'):
            #    data = table.xpath('//td/text()')
                #self.log(data)
                
            #    Phone = table.xpath('//tbody/tr[1]/td[2]').extract()
            #    self.log(f"Phone : {Phone}")
            """
            Website = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tbody/tr[2]/td[2]').extract()
            self.log(f"Website : {Website}")
                    
            Type = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tbody/tr[3]/td[2]').extract()
            self.log(f"Type : {Type}")

            Awards = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tbody/tr[4]/td[2]').extract()
            self.log(f"Awards : {Awards}")

            Campus_Setting = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tbody/tr[5]/td[2]').extract()
            self.log(f"Campus_Setting : {Campus_Setting}")

            Campus_Housing = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tbody/tr[6]/td[2]').extract()
            self.log(f"Campus_Housing : {Campus_Housing}")

            Student_Population = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tbody/tr[7]/td[2]').extract()
            self.log(f"Student_Population : {Student_Population}")

            Student_to_Faculty_ratio = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tbody/tr[8]/td[2]').extract()
            self.log(f"Student_to_Faculty_ratio : {Student_to_Faculty_ratio}")
            """
        #with open(filename, 'wb') as f:
        #    f = ""            
        
        """
        page = response.url.split("=")[-1]
        sel = Selector(response)
        filename = f'file.csv'
        #print(f"response: {response}")
        with open(filename, 'wb') as f:
            f.write(response.body)
        """
        print("Completed the run")
        
        
