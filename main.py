
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys 
import re
import time

from selenium.webdriver.chrome.webdriver import WebDriver

url = "https://www.latamairlines.com/cl/es/ofertas-vuelos?dataFlight=%7B%22tripTypeSelected%22%3A%7B%22label%22%3A%22Ida%20y%20Vuelta%22%2C%22value%22%3A%22RT%22%7D%2C%22cabinSelected%22%3A%7B%22label%22%3A%22Economy%22%2C%22value%22%3A%22Economy%22%7D%2C%22passengerSelected%22%3A%7B%22adultQuantity%22%3A1%2C%22childrenQuantity%22%3A0%2C%22infantQuantity%22%3A0%7D%2C%22originSelected%22%3A%7B%22id%22%3A%22SCL_CL_AIRPORT%22%2C%22name%22%3A%22A.%20Merino%20Benitez%20Intl.%22%2C%22city%22%3A%22Santiago%20de%20Chile%22%2C%22country%22%3A%22Chile%22%2C%22iata%22%3A%22SCL%22%2C%22latitude%22%3A-33.393001556396484%2C%22longitude%22%3A-70.78579711914062%2C%22timezone%22%3A-4%2C%22tz%22%3A%22America%2FSantiago%22%2C%22type%22%3A%22AIRPORT%22%2C%22countryAlpha2%22%3A%22CL%22%2C%22airportIataCode%22%3A%22SCL%22%7D%2C%22destinationSelected%22%3A%7B%22id%22%3A%22MAD_ES_AIRPORT%22%2C%22name%22%3A%22Barajas%20Intl.%22%2C%22city%22%3A%22Madrid%22%2C%22country%22%3A%22Espa%C3%B1a%22%2C%22iata%22%3A%22MAD%22%2C%22latitude%22%3A40.471926%2C%22longitude%22%3A-3.56264%2C%22timezone%22%3A1%2C%22tz%22%3A%22Europe%2FMadrid%22%2C%22type%22%3A%22AIRPORT%22%2C%22countryAlpha2%22%3A%22ES%22%2C%22airportIataCode%22%3A%22MAD%22%7D%2C%22dateGoSelected%22%3A%222021-04-30T16%3A00%3A00.000Z%22%2C%22dateReturnSelected%22%3A%222021-06-23T16%3A00%3A00.000Z%22%2C%22redemption%22%3Afalse%7D&sort=RECOMMENDED"

def get_driver_path():
    if sys.platform == "win32":
        return "./driver/chromedriver.exe"
    return "./driver/chromedriver"


def load_driver():
    path = get_driver_path()
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    #options.add_argument("--headless")
    
    return webdriver.Chrome(executable_path=path, options=options)


def parse_time_data(flight):
    departure_time = flight.find_element_by_xpath(".//div[contains(@class, 'flight-information')]/span[1]").text
    arrive_time_text = flight.find_element_by_xpath(".//div[contains(@class, 'flight-information')][2]/span[1]").get_property('textContent')
    arrive_time = re.sub(r"(\+[0-9]{1})", r" (\1 días)", arrive_time_text)

    return "Hora de salida {departure} - Hora de llegada: {arrive}".format(departure=departure_time, arrive=arrive_time) 


def get_flight_stopover(flight: WebElement, driver: WebDriver):
    btn = flight.find_element_by_xpath(".//div[@class='sc-jHZirH bSaNAq']/a")
    
    driver.execute_script("arguments[0].click();", btn)

    time.sleep(1)

    sections = flight.find_elements_by_xpath("//div[contains(@class, 'MuiPaper-root MuiDialog-paper')]/div[contains(@class, 'MuiDialogContent-root')]/article/div/section[@class='sc-bTiqRo dJJciX']")
    
    details = []
    
    for section in sections:
        departure = section.find_element_by_xpath(".//div[@class='iataCode'][1]/span[1]").text 
        departure_airport = section.find_element_by_xpath(".//div[@class='sc-gQNndl gWZIqE']/span[@class='ariport-name']").text 
        departure_time = section.find_element_by_xpath(".//div[@class='iataCode'][1]/span[2]").text 

        arrive = section.find_element_by_xpath(".//div[@class='sc-RmnOB kdryRf']/div[@class='iataCode']/span[1]").text
        arrive_airport = section.find_element_by_xpath(".//div[@class='sc-RmnOB kdryRf']/span[@class='ariport-name']").text
        arrive_time = section.find_element_by_xpath(".//div[@class='sc-RmnOB kdryRf']/div[@class='iataCode']/span[2]").text 

        duration = section.find_element_by_xpath(".//div[@class='sc-MYvYT cFHRkk']/span[@class='time']").text
        
        details.append({
            "departure": { "name": departure_airport + " - " + departure, "time": departure_time },
            "arrive": { "name": arrive_airport + " - " + arrive, "time": arrive_time },
            "duration": duration
        })

    section.find_element_by_xpath("//button[@class='MuiButtonBase-root MuiIconButton-root sc-kafWEX gtLWBX']").click()
        
    
    return details


def get_all_flights(driver: WebDriver):
    return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='sc-kkwfeq gOkuHo']")))


def get_time_date(driver: WebDriver) -> list[str]:
    flights = get_all_flights(driver)
    return [parse_time_data(flight) for flight in flights]


def get_prices(flight):
    prices = []
    flight.click()
    prices_container = flight.find_elements_by_xpath(".//ol[@class='sc-fjdPjP epCpTk']/li[@class='sc-kWHCRG aSpaq']")
    
    for container in prices_container:
        type = container.find_element_by_xpath(".//div[@class='sc-AUpyg gVCTLq']/div[@class='sc-jOBXIr hxoHWn']/div[@class='sc-kIWQTW jPzzYG']/div/span[1]").get_property('textContent').strip()
        prices_value = container.find_element_by_xpath(".//div[@class='sc-AUpyg gVCTLq']/div[@class='sc-jOBXIr hxoHWn']/div[@class='sc-kIWQTW jPzzYG']/div[2]/div[2]/div/div/span").text
        
        detail = {
            "type": type,
            "prices": prices_value
        }

        prices.append(detail)

    #WebDriverWait(flight, 10).until(EC.presence_of_element_located((By.XPATH, ".//div/div/div[@class='sc-aewfc lOllX']/div[2]/div/button"))).click()

    return prices

with load_driver() as driver:
    driver.get(url)

    flights = get_all_flights(driver)
    flight = flights[1]

    stopovers = get_flight_stopover(flight, driver)
    prices = get_prices(flight)

    details_times = get_time_date(driver)

    print(prices)

    time.sleep(3)