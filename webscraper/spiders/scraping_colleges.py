# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.selector import Selector
import time
import csv

base_url = 'https://nces.ed.gov/COLLEGENAVIGATOR/'
filename = "college_extraction_output.csv"

class CollegesDataSpider(scrapy.Spider):
    base_url = 'https://nces.ed.gov/COLLEGENAVIGATOR/'
    name = "collegedata"

    def start_requests(self):

        # field names
        fields = ['Name','Street','City','State','Zip','Phone','Website','Type','Awards','Campus_Setting','Campus_Housing','Student_Population','Student_to_Faculty_ratio']
                
        
                
        # name of csv file
        

        # data rows of csv file        
        # writing to csv file
        with open(filename, 'w') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                        
                # writing the fields
                csvwriter.writerow(fields)
    
        num_pages = 7
        urls = []
        index_url = 'https://nces.ed.gov/COLLEGENAVIGATOR/?s=all&sp=4&pg=' 
        for pg_id in range(1,num_pages):
            urls.append(index_url+str(pg_id))
        self.log(urls)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        sel = Selector(response)

        page_url_tables = "/html/body/div[1]/form/div[3]/div[2]/div[3]/div[3]/table/tbody"
        page_href_xpath = '/html/body/div[1]/form/div[3]/div[2]/div[3]/div[3]/table/tbody/tr[5]/td[2]/a'
        urls_table_xpath = '//*[@id="ctl00_cphCollegeNavBody_ucResultsMain_tblResults"]'
        self.log(response.xpath(urls_table_xpath).extract())
        table_data = response.xpath(urls_table_xpath).extract()
        links = Selector(text=str(table_data)).xpath('//td/a/@href').extract()

        for link in links:
            page_url = base_url + str(link).strip()
            yield response.follow(url=page_url,callback=self.parse_college_page)

    def parse_college_page(self, response):
        self.log("*******parse_college_page*******")
        self.log(response)                
        
        divs = response.xpath('//div')
        Name = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/span/span/text()').get()
        print(f"Name is {Name}")
        for span in divs.css('.collegedash'):
            Street = ""
            City = ""
            State = ""
            Zip = ""
            address = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/span/text()').extract()
            # self.log(address)
            if isinstance(address,list) and len(address)>0:
                address = address[0]
                

                Street = " ".join(str(address.split(',')[0]).split(' ')[1:])
                self.log(f"Street: {Street}")

                City = str(address.split(',')[1]).strip()
                self.log(f"City: {City}")

                State = str(address.split(',')[-1]).split(' ')[-2]
                self.log(f"State: {State}")
                
                Zip = str(address.split(',')[-1]).split(' ')[-1]
                self.log(f"Zip: {Zip}")

        data = response.xpath('//div').css('.collegedash').xpath('//table[1]').css('.layouttab')
            
        phone = data.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tr[1]/td[2]/text()').get()
        self.log(f"phone: {phone}")

            
        Website = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tr[2]/td[2]/a/@href/text()').get()
        self.log(f"Website : {Website}")
                    
        Type = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tr[3]/td[2]/text()').get()
        self.log(f"Type : {Type}")

        Awards = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tr[4]/td[2]/text()').get()
        self.log(f"Awards : {Awards}")

        Campus_Setting = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tr[5]/td[2]/text()').get()
        self.log(f"Campus_Setting : {Campus_Setting}")

        Campus_Housing = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tr[6]/td[2]/text()').get()
        self.log(f"Campus_Housing : {Campus_Housing}")

        Student_Population = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tr[7]/td[2]/text()').get()
        self.log(f"Student_Population : {Student_Population}")

        Student_to_Faculty_ratio = response.xpath('//*[@id="RightContent"]/div[4]/div/div[2]/table/tr[8]/td[2]/text()').get()
        self.log(f"Student_to_Faculty_ratio : {Student_to_Faculty_ratio}")

        row = [Name,Street,City,State,Zip,phone,Website,Type,Awards,Campus_Setting,Campus_Housing,Student_Population,Student_to_Faculty_ratio]
        print(row)
        
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(row)

            
        
        print("Completed the run")
        
        
