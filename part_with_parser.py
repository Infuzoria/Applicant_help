from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def parser(url):
    ops = webdriver.ChromeOptions()
    ops.add_argument('headless')
    driver_service = Service(executable_path="C:/chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service, options=ops)

    driver.get(url)
    html = driver.page_source

    parse = BeautifulSoup(html, features="html.parser")
    table1 = parse.find("tr", class_="titlesRow")
    table2 = parse.find("table")
    headers = []
    for i in table1.find_all("th"):
        title = i.text
        headers.append(title)

    main_table = []
    for j in table2.find_all("tr")[1:]:
        temp = {}
        row_data = j.find_all("td")
        for index, i in enumerate(row_data):
            temp[headers[index]] = i.text
        main_table.append(temp)

    return main_table
