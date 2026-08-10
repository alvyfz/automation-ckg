import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from selenium import webdriver

import ui

email = "romdoni0682@gmail.com"
password = "Bojongasih#24"
 




def _write_failed_download(
    *,
    mode: str,
    excel_path: str,
    failed_rows: list[pd.Series],
    name_column: str,
) -> None:
    if not failed_rows:
        return

    downloads_dir = Path.home() / "Downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    failed_df = pd.DataFrame([r.to_dict() for r in failed_rows])
    out_xlsx = downloads_dir / f"failed_{mode}_{ts}.xlsx"
    failed_df.to_excel(out_xlsx, index=False)

    out_txt = downloads_dir / f"failed_{mode}_{ts}.txt"
    names = [str(r.get(name_column, "")).strip() for r in failed_rows]
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"source_excel={excel_path}\n")
        for n in names:
            if n:
                f.write(n + "\n")


def run(excel_path: str, *, school_key: str | None = None) -> None:
    url = "https://sehatindonesiaku.kemkes.go.id/auth/login"
    if school_key is not None:
        ui.set_school(school_key)
    df = pd.read_excel(excel_path, engine='openpyxl')

    failed_rows: list[pd.Series] = []

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
    with open("failed_names.txt", "a", encoding="utf-8") as f:
                f.write("START " + excel_path + "\n")
    # Loop through setiap baris di dataframe
    for index, row in df.iterrows():
        print("start input data", row)
        ok = ui.submitForm(driver, row)
        if not ok:
            failed_rows.append(row)
    # ui.absence(driver)

    time.sleep(5)
    with open("failed_names.txt", "a", encoding="utf-8") as f:
                f.write("END " + excel_path + "\n")
    print("Waktu tunggu selesai. Jika butuh lebih lama, ubah nilai time.sleep di file ini.")

    # Tutup browser setelah waktu tunggu selesai
    try:
        driver.quit()
    except Exception:
        pass

    _write_failed_download(mode="daftar", excel_path=excel_path, failed_rows=failed_rows, name_column="name")


def main() -> None:
    run("./data/DATA KLS 1.xlsx")


if __name__ == "__main__":
    main()
