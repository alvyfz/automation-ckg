import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import ui
import pandas as pd

email='romdoni0682@gmail.com'
password='Bojongasih#24'
 




def main():
    url = "https://sehatindonesiaku.kemkes.go.id/auth/login"
    # Baca Excel dengan engine 'openpyxl' dan error handling yang jelas
    excel_path = r'C:\Users\alvyf\My Project\input-sehat\DATA KLS 6.xlsx'
    df = pd.read_excel(excel_path, engine='openpyxl')


    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    driver.maximize_window()    
 
 

    print("Browser dibuka ke halaman login. Silakan isi username, password, dan captcha secara manual.")
     
    ui.login(driver, email, password)
    time.sleep(15)
    ui.modal(driver)
    time.sleep(2)
    ui.goToCKGSchool(driver)
    time.sleep(1)
    # Loop through setiap baris di dataframe
    for index, row in df.iterrows():
        print("start input data", row)
        ui.submitForm(driver, row)
    # ui.absence(driver)

    time.sleep(5)
    print("Waktu tunggu selesai. Jika butuh lebih lama, ubah nilai time.sleep di file ini.")

    # Tutup browser setelah waktu tunggu selesai
    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()