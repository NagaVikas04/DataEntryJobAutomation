from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import lxml

google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd92U2ZLw1yXVZpiY1PDgerdUhQNi7kvUZhYPIWYjCJ-9Ue8A/viewform?usp=sf_link"
zillow_url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
edgedriver_path = r"C:\Users\nagav\EdgeDriver\edgedriver_win64\msedgedriver.exe"

headers = {
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

response = requests.get(url=zillow_url, headers=headers)
zillow_html = response.text




class DataEntryAutomation():
    def __init__(self):
        self.response = requests.get(url=zillow_url, headers=headers)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.driver = webdriver.Edge(service=Service(executable_path=edgedriver_path))

    def get_cost(self):
        cost_html_list = self.soup.find_all("div", class_="StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0 hRqIYX")
        cost_list = [int(c.text.strip().replace(",", "")[1:5]) for c in cost_html_list]
        return cost_list

    def get_address(self):
        address_html_list = self.soup.find_all("a", class_="property-card-link")
        address_list = [address.text for address in address_html_list if address.text != ""]
        return address_list

    def get_link(self):
        url_html_list = self.soup.find_all("a",
                                           class_="StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0 lhIXlm property-card-link")
        url_list = [l.get(key="href") for l in url_html_list]
        return url_list

    def update_googleforms(self, address, price, links):
        for i in range(len(price)):
            self.driver.get(url=google_form_url)
            address_update = self.driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
            address_update.send_keys(address[i])
            sleep(1)

            price_update = self.driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(2) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
            price_update.send_keys(price[i])
            sleep(1)

            link_update = self.driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(3) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
            link_update.send_keys(links[i])

            sleep(2)

            submit_form = self.driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb > div.lRwqcd > div > span > span")
            submit_form.click()

            sleep(2)

            print(f"form - {i} submitted successfully with data.\n address: {address[i]}\n price: {price[i]}\n link: {links[i]}")


dataentryautomation = DataEntryAutomation()
address = dataentryautomation.get_address()
price = dataentryautomation.get_cost()
links = dataentryautomation.get_link()
# print(f"{address}\n{link}\n{price}")
# print(len(address), len(link), len(price))
dataentryautomation.update_googleforms(address=address, price=price, links=links)




# service = Service(executable_path=edgedriver_path)
# driver = webdriver.Edge(service=service)
#
# driver.get(url=google_form_url)
# address = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
# address.send_keys("abc")
# sleep(3)
#
# link_t = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(2) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
# link_t.send_keys("def")
# sleep(3)
#
# price = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(3) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
# price.send_keys(123)
# sleep(3)
#
# submit_b = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb > div.lRwqcd > div > span > span")
# submit_b.click()
# sleep(3)



# soup = BeautifulSoup(zillow_html, "html.parser")
# address_and_link = soup.find("a", class_="property-card-link")
# print(address_and_link)
# print(address_and_link.get(key="href"))
# print(address_and_link.text)

# cost = soup.find_all("div", class_="StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0 hRqIYX")
# c = [c.text for c in cost]
# print(c[0].strip().replace(",", ""))
# c = [int(c.text.strip().replace(",", "")[1:5]) for c in cost]
# print(c)
# cost = cost.text()

# test = soup.find("div", class_="textContent")
# print(test)
