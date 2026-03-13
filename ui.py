import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


schools ={
    'attaufiq' : {
         'school' : 'MIS ATTAUFIQ',
         'xpath' : '/html/body/div[3]/div[2]/div[2]/div/div[6]/button',
         'phoneNumber': '82119221427',
         'desa': '/html/body/div[3]/div[2]/div[4]/div/div[6]/button'
     },
    'balekambang' : {
         'school' : 'MIS BALEKAMBANG',
         'xpath' : '/html/body/div[3]/div[2]/div[2]/div/div[7]/button',
         'phoneNumber': '81214133967',
         'desa': '/html/body/div[3]/div[2]/div[4]/div/div[2]/button'
     },
     'duabojongasih': {
        'school' : 'SDN 2  BOJONGASIH',
        'xpath' : '/html/body/div[3]/div[2]/div[2]/div/div[17]/button',
        'phoneNumber': '85287424436',
        'desa': '/html/body/div[3]/div[2]/div[4]/div/div[4]/button'
     }
}

schoolData = schools['duabojongasih'] 

phoneNumber = schoolData['phoneNumber']
school = schoolData['school']
classSchool = '2'


kelas = {
    '1': '/html/body/div[3]/div[2]/div[2]/div/div[1]/button',
    '2': '/html/body/div[3]/div[2]/div[2]/div/div[2]/button',
    '3': '/html/body/div[3]/div[2]/div[2]/div/div[3]/button',
    '4': '/html/body/div[3]/div[2]/div[2]/div/div[4]/button',
    '5': '/html/body/div[3]/div[2]/div[2]/div/div[5]/button',
    '6': '/html/body/div[3]/div[2]/div[2]/div/div[6]/button',
}


month ={
    '01' : 1,
    '02' : 2,
    '03' : 3,
    '04' : 4,
    '05' :5,
    '06' : 6,
    '07' : 7,
    '08' : 8,
    '09' : 9,
    '10' : 10,
    '11' : 11,
    '12' : 12,
}

imt = {
    'buruk': '//*[@id="sq_102i_listPPV00000662"]',
    'kurang': '//*[@id="sq_102i_listPPV00000663"]',
    'baik': '//*[@id="sq_102i_listPPV00000664"]',
    'lebih': '//*[@id="sq_102i_listPPV00000665"]',
    'berlebih': '//*[@id="sq_102i_listPPV00000665"]',
    'obesitas': '//*[@id="sq_102i_listPPV00000666"]',
    'normal': '//*[@id="sq_102i_listPPV00000664"]',
}

gigi = {
    '0': '//*[@id="sq_100"]/div[2]/fieldset/div[1]/label',
    '1': '//*[@id="sq_100"]/div[2]/fieldset/div[2]/label',
    '2': '//*[@id="sq_100"]/div[2]/fieldset/div[3]/label',
    '3': '//*[@id="sq_100"]/div[2]/fieldset/div[4]/label',
    '4': '//*[@id="sq_100"]/div[2]/fieldset/div[5]/label',
}

def login(driver, email, password):
    # Isi username dan password
    username_field = driver.find_element("id", "email")
    password_field = driver.find_element("id", "password")


    time.sleep(3)

    username_field.send_keys(email)
    password_field.send_keys(password)
 
    
def modal(driver):
    # Klik modal
    modal_button = driver.find_element("xpath", '/html/body/div[1]/div[2]/div/div/div/div[2]/div[85]/div[1]/div/div/div[1]')
    modal_button.click()
    time.sleep(1)
    # Klik tombol "Lanjutkan"
    continue_button = driver.find_element("xpath", '/html/body/div[1]/div[2]/div/div/div/div[2]/div[86]/div/button')
    continue_button.click()

def goToCKGSchool(driver):
    button_menu = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[1]/div/div[2]/div/div/div[3]/div/button')
    button_menu.click()
    time.sleep(1)
    button_ckg = driver.find_element("xpath", '//*[@id="menu_cari/daftarkan_individu"]')
    button_ckg.click()

def inputDate(driver, date):
        # Jika date bertipe timestamp, konversi ke string YYYY-MM-DD
    if isinstance(date, (int, float)):
        date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
    elif hasattr(date, 'strftime'):
        date = date.strftime('%Y-%m-%d')

    input_date = driver.find_element("xpath", '//*[@id="Tanggal Lahir"]/div[2]/div/div')
    input_date.click()
    time.sleep(1)
    click_detail = driver.find_element("xpath", '/html/body/div[3]/div/div/div[1]/span/button[1]')
    click_detail.click()
    time.sleep(0.5)
    button_back_year = driver.find_element("xpath", '/html/body/div[3]/div/div/div[1]/button[1]')
    # Ambil tahun dari parameter date (format diasumsikan YYYY-MM-DD)
    year = int(date.split('-')[0])
    clicks_needed = 2025 - year
    # Klik tombol mundur tahun sebanyak selisih tahun
    for _ in range(clicks_needed):
        button_back_year = driver.find_element("xpath", '/html/body/div[3]/div/div/div[1]/button[1]')
        button_back_year.click()
        time.sleep(0.3)

    # Klik bulan (data-month = bulan - 1)
    monthDate = date.split('-')[1]
    print(monthDate)
    month_xpath = f'//td[contains(@class,"cell") and @data-month="{month[monthDate] - 1}"]/div'
    month_cell = driver.find_element("xpath", month_xpath)
    month_cell.click()
    time.sleep(0.5)
    # Klik tanggal berdasarkan atribut title
    day = int(date.split('-')[2])
    date_title = f"{date}"
    day_xpath = f'//td[@class="cell" and @title="{date_title}"]/div[text()="{day}"]'
    day_cell = driver.find_element("xpath", day_xpath)
    day_cell.click()
    time.sleep(0.5)

def inputSchool(driver):
    input_school = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[10]/div/div/div[2]')
    input_school.click()
    time.sleep(0.5)
    # school_option = driver.find_element("xpath", f'//button[.//div[text()="{school}"]]')
    school_option = driver.find_element("xpath", schoolData['xpath'])
    school_option.click()
    time.sleep(0.5)


def address(driver):
    input_address = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[13]/div[1]/div[2]/div')
    input_address.click()
    time.sleep(0.5)
    province = driver.find_element("xpath", '/html/body/div[3]/div[2]/div[4]/div/div[6]/button[2]')
    province.click()
    time.sleep(2)
    city = driver.find_element("xpath", '/html/body/div[3]/div[2]/div[4]/div/div[19]/button')
    city.click()
    time.sleep(2)
    district = driver.find_element("xpath", '/html/body/div[3]/div[2]/div[4]/div/div[3]/button')
    district.click()
    time.sleep(2)
    subdistrict = driver.find_element("xpath", schoolData['desa'] )
    subdistrict.click()
    time.sleep(1)

     

def submitForm(driver, data):
    button_create = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/button')
    button_create.click()
 
    time.sleep(1)
    input_nik = driver.find_element("xpath", '//*[@id="nik"]')
    nik_value = str(data['nik'])
    if nik_value.startswith("'"):
        nik_value = nik_value[1:]
    input_nik.send_keys(nik_value)
    input_name = driver.find_element("xpath", '//*[@id="Nama Lengkap"]')
    input_name.send_keys(data['name'])
    time.sleep(0.5)
    inputDate(driver, data['date'])
    time.sleep(0.5)
    jenis_kelamin = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[5]/div/div[2]')
    jenis_kelamin.click()
    time.sleep(0.5)
    # Pilih jenis kelamin berdasarkan data['gender']
    if data['gender'] == "L":
        gender_option = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[5]/div/div[2]/div[3]/div/div[1]')
    else:
        gender_option = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[5]/div/div[2]/div[3]/div/div[2]')
    gender_option.click()
    time.sleep(0.5)
    marital_status = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[6]/div/div[2]')
    marital_status.click()
    time.sleep(0.5)
    marital_status_option = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[6]/div/div[2]/div[3]/div/div[3]')
    marital_status_option.click()
    time.sleep(0.5)
    disability = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[7]/div/div[2]')
    disability.click()
    time.sleep(0.5)
    disability_option = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[7]/div/div[2]/div[3]/div/div[1]')
    disability_option.click()
    time.sleep(0.5)
    input_phone = driver.find_element("xpath", '//*[@id="No Whatsapp"]')
    input_phone.send_keys(phoneNumber)
    time.sleep(0.5)
    inputSchool(driver)
    time.sleep(0.5)
    study = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[1]/div[1]/div[12]/div/div/div[2]')
    study.click()
    time.sleep(0.5)
    study_option = driver.find_element("xpath", kelas[str(int(data['class']))])
    study_option.click()
    time.sleep(0.5)
    address(driver)
    time.sleep(0.5)
    full_address = driver.find_element("xpath", '//*[@id="detail-domisili"]')
    full_address.send_keys(data['address'])
    time.sleep(0.5)
    button_submit = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div/div[3]/div/form/div[2]/div/button')
    button_submit.click()
    time.sleep(3)

    # Cek apakah muncul modal error
    try:
        error_modal = driver.find_element("xpath", '/html/body/div[1]/div[2]/div/div[2]/img')
        if error_modal and error_modal.get_attribute("src") == "https://sehatindonesiaku.kemkes.go.id/images/icons/warning.png":
            print("Gagal submit form", data['name'])
            with open("failed_names.txt", "a", encoding="utf-8") as f:
                f.write(data['name'] + "\n")
            driver.refresh()
            time.sleep(1)
        else:
            driver.refresh()
            time.sleep(1)
    except Exception:
        pass
        driver.refresh()
        time.sleep(1)
        


def absence (driver):
    school_select = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div/div[2]')
    school_select.click()
    time.sleep(0.5)
    school_option = driver.find_element("xpath", f'//div[text()="{school}"]')
    school_option.click()
    time.sleep(0.5)
    class_select = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div/div[2]')
    class_select.click()
    time.sleep(0.5)
    class_option = driver.find_element("xpath", f'//div[text()="Kelas {classSchool}"]')
    class_option.click()
    time.sleep(0.5)
    while True:
        try:
            button_submit = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td[8]/div/div/div/button')
            button_submit.click()
            break
        except Exception:
            time.sleep(1)
    time.sleep(1)
    checkbox_absent = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div[4]/div[3]/div[1]/div/div[1]')
    checkbox_absent.click()
    time.sleep(0.5)
    button_submit = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div[5]/div[2]/button')
    button_submit.click()
    time.sleep(2)
    buttom_close = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[6]/div[2]/div/div[3]/div[2]/button')
    buttom_close.click()
    time.sleep(2)

def goToCGKServices(driver):
    button_menu = driver.find_element("xpath", '//*[@id="__nuxt"]/main/div/div[1]/section[1]/div/div[2]/div/div/div[3]/div/button')
    button_menu.click()
    time.sleep(1)
    button_ckg = driver.find_element("xpath", '//*[@id="menu_pelayanan"]')
    button_ckg.click()


def filterBySchoolAndClasses(driver):
    school_select = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div/div[2]')
    school_select.click()
    time.sleep(0.5)
    school_option = driver.find_element("xpath", f'//div[text()="{school}"]')
    school_option.click()
    time.sleep(0.5)
    class_select = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div/div[2]')
    class_select.click()
    time.sleep(0.5)
    class_option = driver.find_element("xpath", f'//div[text()="Kelas {classSchool}"]')
    class_option.click()
    time.sleep(0.5)

def scanForm(driver, data):
    target_name = data['nama'].strip().upper()
    # Tunggu tabel muncul sekali di luar loop
    wait = WebDriverWait(driver, 1)

    while True:
        # Cek apakah nama ada di halaman saat ini
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//tr[contains(@class,"p-2 border-b-solid")]')))
        except Exception:
            return False  # Tabel tidak muncul

        # Gunakan XPath langsung untuk nama target
        # Tangani kemungkinan tanda kutip tunggal di nama target
 
        # Build XPath that matches any text content (including special chars like .,-' and others) after upper-casing both sides
        # target_xpath = (
        #     '//tr[contains(@class,"p-2 border-b-solid") and '
        #     './td[2][normalize-space(translate(text(),'
        #     '"abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿžšœ.-,",'
        #     '"ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠŒ.-,"))='
        #     f'"{escaped_target}"]]'
        # )
        target_xpath = (
            '//tr[contains(@class,"p-2 border-b-solid") and '
            './td[2][normalize-space(translate(text(),'
            '"abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿžšœ.-,",'
            '"ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠŒ.-,"))='
            f'"{target_name}"]]'
        )
        targets = driver.find_elements(By.XPATH, target_xpath)
        if targets:
            # Klik tombol “Mulai” pada baris yang sesuai
            button = targets[0].find_element(By.XPATH, './/button[@type="button"]')
            button.click()
            time.sleep(1)
            fillScanningForm(driver, data)
            return True

        # Cek apakah masih ada halaman berikutnya
        try:
            next_link = driver.find_element(By.XPATH, '//li[contains(@class,"page-item") and not(contains(@class,"disabled"))]/a[@class="page-link" and text()=">"]')
            next_link.click()
            # Tunggu tabel baru muncul, maksimal 1 detik
            wait.until(EC.staleness_of(targets[0]) if targets else lambda d: True)
        except Exception:
            # Tidak ada halaman lagi
            with open("failed_names.txt", "a", encoding="utf-8") as f:
                f.write(data['nama'] + "\n")
            goToCGKServ(driver)
            return False

def fillScanningForm(driver, data):
    # Klik tombol “Mulai” di bagian atas halaman
    start_button = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div/button')
    start_button.click()
    time.sleep(1)
    inputGizi(driver, data)
    inputTensi(driver, data)
    inputGigi(driver, data)
    inputMT(driver, data)
    goToCGKServ(driver)

def goToCGKServ(driver):
    driver.get("https://sehatindonesiaku.kemkes.go.id/ckg-pelayanan-sekolah?back=true")
    driver.refresh()
    time.sleep(1)


def inputGizi(driver, data):
     input_button = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[5]/div[2]/div[2]/div[2]/div/div/div/div/div[4]/div/button')
     input_button.click()
     time.sleep(1)
     input_weight = driver.find_element("xpath", '//*[@id="sq_100i"]')
     input_weight.send_keys(data['bb'])
     time.sleep(0.5)
     input_height = driver.find_element("xpath", '//*[@id="sq_101i"]')
     input_height.send_keys(data['tb'])
     time.sleep(0.5)
     select_click = driver.find_element("xpath", '//*[@id="sq_102"]/div[2]/div')
     select_click.click()
     time.sleep(1)
     select_option = driver.find_element("xpath", imt[data['imt']])
     select_option.click()
     time.sleep(1)
     button_submit = driver.find_element("xpath", '//*[@id="sv-nav-complete"]/div/input')
     button_submit.click()
     time.sleep(2)

def inputTensi(driver,data):
     input_button = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[5]/div[2]/div[2]/div[3]/div/div/div/div/div[4]/div/button')
     input_button.click()
     time.sleep(1)
     input_systolic = driver.find_element("xpath", '//*[@id="sq_100i"]')
     input_systolic.send_keys(data['sistol'])
     time.sleep(0.5)
     input_diastolic = driver.find_element("xpath", '//*[@id="sq_101i"]')
     input_diastolic.send_keys(data['diastol'])
     time.sleep(0.5)
     button_submit = driver.find_element("xpath", '//*[@id="sv-nav-complete"]/div/input')
     button_submit.click()
     time.sleep(2)

def inputGigi(driver, data):
     value = data['gigi']
     if int(value) >= 4:
        value = '4'
     else:
        value = str(int(float(value)))

     input_button = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[5]/div[2]/div[2]/div[4]/div/div/div/div/div[4]/div/button')
     input_button.click()
     time.sleep(1)
     input_gigi = driver.find_element("xpath", gigi[value])
     input_gigi.click()
     time.sleep(0.5)
     button_submit = driver.find_element("xpath", '//*[@id="sv-nav-complete"]/div/input')
     button_submit.click()
     time.sleep(2)


def inputMT(driver, data):
    mt={
        '1': {
            '1': '//*[@id="sq_100"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_100"]/div[2]/fieldset/div[2]/label',
            
        },
        '2': {
            '1': '//*[@id="sq_101"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_101"]/div[2]/fieldset/div[2]/label',
        },
        '3': {
            '1': '//*[@id="sq_102"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_102"]/div[2]/fieldset/div[2]/label',
        },
        '4': {
            '1': '//*[@id="sq_103"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_103"]/div[2]/fieldset/div[2]/label',
        },
        '5': {
            '1': '//*[@id="sq_104"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_104"]/div[2]/fieldset/div[2]/label',
        },
        '6': {
            '1': '//*[@id="sq_105"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_105"]/div[2]/fieldset/div[2]/label',
        },
        '7': {
            '1': '//*[@id="sq_106"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_106"]/div[2]/fieldset/div[2]/label',
        },
        '8': {
            '1': '//*[@id="sq_107"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_107"]/div[2]/fieldset/div[2]/label',  
        },
        '9': {
            '1': '//*[@id="sq_108"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_108"]/div[2]/fieldset/div[2]/label',
        },
        '10': {
            '1': '//*[@id="sq_109"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_109"]/div[2]/fieldset/div[2]/label',
        },
        '11': {
            '1': '//*[@id="sq_110"]/div[2]/fieldset/div[1]/label',
            '2': '//*[@id="sq_110"]/div[2]/fieldset/div[2]/label',
        },
    }
    input_button = driver.find_element("xpath", '/html/body/div[1]/main/div/div[1]/section[2]/div/div/div/div[2]/div/div[5]/div[2]/div[2]/div[5]/div/div/div/div/div[4]/div/button')
    input_button.click()
    time.sleep(1)
    for i in range(1,12):
        value = data['tm '+str(i)]
        # Jika value 1 maka pilih '1', jika value 2 maka pilih '2'
        option_key = str(int(float(value)))
        input_mt = driver.find_element("xpath", mt[str(i)][option_key])
        input_mt.click()
        time.sleep(0.5)
    submit_btn = driver.find_element("xpath", '//*[@id="sv-nav-complete"]/div/input')
    submit_btn.click()
    time.sleep(2)
     
