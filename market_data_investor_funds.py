import pandas as pd
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')

# market_data_driver = webdriver.Chrome(options=options)
market_data_driver = webdriver.Chrome(options=options)

market_data_driver.get("https://markets.ft.com/data/funds/uk/results")
time.sleep(10)  # Allow time for the page to load

try:
    iframes = market_data_driver.find_elements(By.TAG_NAME, "iframe")

    for iframe in iframes:
        market_data_driver.switch_to.frame(iframe)  # Switch to the iframe
        try:
            # Wait for the cookie accept button to be clickable and click it
            accept_cookies_button = WebDriverWait(market_data_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[3]/div/button[2]"))
            )
            accept_cookies_button.click()

            break

        except Exception as e:
            market_data_driver.switch_to.default_content()

            continue

        time.sleep(5)

    market_data_driver.switch_to.default_content()


except Exception as e:
    print("Error while accepting cookies:", str(e))

time.sleep(5)
list_data_btn = market_data_driver.find_elements(By.CSS_SELECTOR,
                                                 "body > div.o-grid-container.mod-container > div:nth-child(2) > section > div:nth-child(3) > div")

pagination_button = list_data_btn[0].find_elements(By.TAG_NAME, "button")
next_page = pagination_button[-1]


last_second_page = int(pagination_button[-2].text)

wait = WebDriverWait(market_data_driver, 10)  # 10 seconds timeout
invastor_link_dtls = []
for i in range(0, last_second_page):
    try:

        time.sleep(4)
        try:
            invastor_link = list_data_btn[0].find_elements(By.TAG_NAME,"a")

            for j in invastor_link:
                try:
                    temp = j.get_attribute("href")
                    invastor_link_dtls.append(temp)
                except:
                    temp = None
                    invastor_link_dtls.append(temp)
        except:
            invastor_link=None

        pagination_button = list_data_btn[0].find_elements(By.TAG_NAME, "button")
        next_page = pagination_button[-1]

        next_page.click()
        # print(f"Clicked page {i + 1}")

    except Exception as e:
        pass
        # print(f"Error clicking page {i + 1}: {e}")


for k in invastor_link_dtls:
    if k:
        market_data_driver.get(k)

        try:
            share_name = WebDriverWait(market_data_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[1]/div[1]/h1"))
            )

            symbol_data = WebDriverWait(market_data_driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[1]/div[2]"))
            )
            symbol = symbol_data.text.split(":")
            ISIN =symbol[0]
            currency = symbol[1]


            one_year_change = WebDriverWait(market_data_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[2]/ul/li[3]/span[2]")))



            price_data = WebDriverWait(market_data_driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[2]/ul/li[1]"))
            )
            price = price_data.find_elements(By.XPATH,"/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[2]/ul/li[1]/span[2]")[0].text
        except:
            share_name = None
            symbol_data = None
            one_year_change = None
            price_data = None
            price = None
            symbol = None
            ISIN = None
            Currency = None



        ############################################ top 5 holder name, year change and weight ######################################
        try:

            top_5_holding_table = accept_cookies_button = WebDriverWait(market_data_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[3]/section/div[4]/div/div/table"))
            )
            table_top5_holders = top_5_holding_table.find_elements(By.TAG_NAME, "tbody")
            table_top5_holders_dtls = table_top5_holders[0].find_elements(By.TAG_NAME, "tr")

            for p in table_top5_holders_dtls:
                ###### first company holding ######

                first_holding_name = p.find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(4) > div > div > table > tbody > tr:nth-child(1) > td.mod-ui-table__cell--text")


                first_holding_1y_change = p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[1]/td[2]")
                first_holding_weight = p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[1]/td[3]")

                ###### Second company holding ######


                second_holding_name = p.find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(4) > div > div > table > tbody > tr:nth-child(2) > td.mod-ui-table__cell--text")

                second_holding_1y_change = p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[2]/td[2]")

                second_holding_weight = p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[2]/td[3]")


                second_holding_name = None
                second_holding_1y_change = None
                second_holding_weight = None

                ###### Third company holding ######

                third_holding_name= p.find_elements(By.CSS_SELECTOR,
                                  "body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(4) > div > div > table > tbody > tr:nth-child(3) > td.mod-ui-table__cell--text")

                third_holding_1y_change=p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[3]/td[2]")

                third_holding_weight = p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[3]/td[3]")

                third_holding_name = None
                third_holding_1y_change = None
                third_holding_weight = None


                ###### Forth company holding ######

                fourth_holding_name  =p.find_elements(By.CSS_SELECTOR,
                                  "body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(4) > div > div > table > tbody > tr:nth-child(4) > td.mod-ui-table__cell--text")
                fourth_holding_1y_change = p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[4]/td[2]")
                fourth_holding_weight = p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[4]/td[3]")

                fourth_holding_name = None
                fourth_holding_1y_change = None
                fourth_holding_weight = None


                ###### Fifth company holding ######
                fifth_holding_name = p.find_elements(By.CSS_SELECTOR,
                                "body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(4) > div > div > table > tbody > tr:nth-child(5) > td.mod-ui-table__cell--text")

                fifth_holding_1y_change = p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[5]/td[2]")

                fifth_holding_weight = p.find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[4]/div/div/table/tbody/tr[5]/td[3]")



                fifth_holding_name = None
                fifth_holding_1y_change = None
                fifth_holding_weight = None


            ########################################################################################################################################################

        except:
            top_5_holding_table = None
            table_top5_holders = None
            table_top5_holders_dtls = None
            first_holding_name = None
            first_holding_1y_change = None
            first_holding_weight = None



        # Sector names and weights
        try:
            diversification = WebDriverWait(market_data_driver, 10).until(EC.element_to_be_clickable((By.XPATH,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5)")))


            div_top5_section = diversification.find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(2)")
            table_sector = div_top5_section[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[2]/div[2]/table")


            first_sector_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(2) > div.mod-diversification__column__table > table > tbody > tr:nth-child(1) > td.mod-ui-table__cell--colored")


            first_sector_weight =table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[2]")


            second_sector_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(2) > div.mod-diversification__column__table > table > tbody > tr:nth-child(2) > td.mod-ui-table__cell--colored")
            second_sector_weight = table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[2]/div[2]/table/tbody/tr[2]")

            third_sector_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(2) > div.mod-diversification__column__table > table > tbody > tr:nth-child(3) > td.mod-ui-table__cell--colored")
            third_sector_weight = table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[2]")

            fourth_sector_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(2) > div.mod-diversification__column__table > table > tbody > tr:nth-child(4) > td.mod-ui-table__cell--colored")
            fourth_sector_weight = table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[2]/div[2]/table/tbody/tr[4]/td[2]")

            fifth_sector_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(2) > div.mod-diversification__column__table > table > tbody > tr:nth-child(5) > td.mod-ui-table__cell--colored")
            fifth_sector_weight = table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[2]/div[2]/table/tbody/tr[5]/td[2]")



            # Region names and weights

            reagons_section  = diversification.find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(3)")
            table_region = reagons_section[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[3]/div[2]/table")

            first_region_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(3) > div.mod-diversification__column__table > table > tbody > tr:nth-child(1) > td.mod-ui-table__cell--colored")
            first_region_weight = table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[3]/div[2]/table/tbody/tr[1]/td[2]")

            second_region_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(3) > div.mod-diversification__column__table > table > tbody > tr:nth-child(2) > td.mod-ui-table__cell--colored")
            second_region_weight = table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[3]/div[2]/table/tbody/tr[2]/td[2]")

            third_region_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(3) > div.mod-diversification__column__table > table > tbody > tr:nth-child(3) > td.mod-ui-table__cell--colored")
            third_region_weight = table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[3]/div[2]/table/tbody/tr[3]/td[2]")

            fourth_region_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(3) > div.mod-diversification__column__table > table > tbody > tr:nth-child(4) > td.mod-ui-table__cell--colored")
            fourth_region_weight = table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[3]/div[2]/table/tbody/tr[4]/td[2]")

            fifth_region_name = table_sector[0].find_elements(By.CSS_SELECTOR,"body > div.o-grid-container.mod-container > div:nth-child(3) > section > div:nth-child(5) > div > div.mod-module__content > div:nth-child(3) > div.mod-diversification__column__table > table > tbody > tr:nth-child(5) > td.mod-ui-table__cell--colored")
            fifth_region_weight = table_sector[0].find_elements(By.XPATH,"/html/body/div[3]/div[3]/section/div[5]/div/div[2]/div[3]/div[2]/table/tbody/tr[5]/td[2]")
        except:
            diversification = None
            div_top5_section = None
            div_top5_section = None
            table_sector = None
            first_sector_name = None
            first_sector_weight = None
            second_sector_name = None
            second_sector_weight = None
            third_sector_name = None
            third_sector_weight = None
            fourth_sector_name = None
            fourth_sector_weight = None
            fifth_sector_name = None
            fifth_sector_weight = None
            reagons_section = None
            table_region = None
            first_region_name = None
            first_region_weight = None
            second_region_name = None
            second_region_weight = None
            third_region_name = None
            third_region_weight = None
            fourth_region_name = None
            fourth_region_weight = None
            fifth_region_name = None
            fifth_region_weight = None


        # Dictionary mapping keys to the corresponding variables
        data = {

            "Name": share_name,
            "ISIN":ISIN,
            "Price": price,
            "Currency":currency ,

            "1-Year Change": one_year_change,

            # Holdings
            "1st Holding Name": first_holding_name,
            "1st Holding 1Y Change": first_holding_1y_change,
            "1st Holding Weight": first_holding_weight,

            "2nd Holding Name": second_holding_name,
            "2nd Holding 1Y Change": second_holding_1y_change,
            "2nd Holding Weight": second_holding_weight,

            "3rd Holding Name": third_holding_name,
            "3rd Holding 1Y Change": third_holding_1y_change,
            "3rd Holding Weight": third_holding_weight,

            "4th Holding Name": fourth_holding_name,
            "4th Holding 1Y Change": fourth_holding_1y_change,
            "4th Holding Weight": fourth_holding_weight,

            "5th Holding Name": fifth_holding_name,
            "5th Holding 1Y Change": fifth_holding_1y_change,
            "5th Holding Weight": fifth_holding_weight,

            # Sectors
            "1st Sector Name": first_sector_name,
            "1st Sector Weight": first_sector_weight,

            "2nd Sector Name": second_sector_name,
            "2nd Sector Weight": second_sector_weight,

            "3rd Sector Name": third_sector_name,
            "3rd Sector Weight": third_sector_weight,

            "4th Sector Name": fourth_sector_name,
            "4th Sector Weight": fourth_sector_weight,

            "5th Sector Name": fifth_sector_name,
            "5th Sector Weight": fifth_sector_weight,

            # Regions
            "1st Region Name": first_region_name,
            "1st Region Weight": first_region_weight,

            "2nd Region Name": second_region_name,
            "2nd Region Weight": second_region_weight,

            "3rd Region Name": third_region_name,
            "3rd Region Weight": third_region_weight,

            "4th Region Name": fourth_region_name,
            "4th Region Weight": fourth_region_weight,

            "5th Region Name": fifth_region_name,
            "5th Region Weight": fifth_region_weight
        }

    else:
        continue


header =[
    "1-Year Change",
    "1st Holding Name",
    "1st Holding 1Y Change",
    "1st Holding Weight",
    "2nd Holding Name",
    "2nd Holding 1Y Change",
    "2nd Holding Weight",
    "3rd Holding Name",
    "3rd Holding 1Y Change",
    "3rd Holding Weight",
    "4th Holding Name",
    "4th Holding 1Y Change",
    "4th Holding Weight",
    "5th Holding Name",
    "5th Holding 1Y Change",
    "5th Holding Weight",
    "1st Sector Name",
    "1st Sector Weight",
    "2nd Sector Name",
    "2nd Sector Weight",
    "3rd Sector Name",
    "3rd Sector Weight",
    "4th Sector Name",
    "4th Sector Weight",
    "5th Sector Name",
    "5th Sector Weight",
    "1st Region Name",
    "1st Region Weight",
    "2nd Region Name",
    "2nd Region Weight",
    "3rd Region Name",
    "3rd Region Weight",
    "4th Region Name",
    "4th Region Weight",
    "5th Region Name",
    "5th Region Weight"
]
data_frame = pd.DataFrame(data,columns=header)
data_frame.to_csv("market_data_investor_funds.csv",index=False)
print("csv created successfully")

