import requests
import time
import pandas as pd
URL = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude" : 21.03,
    "longitude":105.85,
    "start_date":'2026-11-01',
    "end_date":'2026-11-10',
    "daily":"temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone":"Asia/Ho_Chi_Minh"
}
def goi_api(url,params,so_lan_thu=3):
    for lan in range(1,so_lan_thu+1):
        try:
            response = requests.get(url,params=params,timeout=10)
        except requests.exceptions.RequestException as loi:
            print(f"Lan {lan}:loi mang({loi}),doi roi thu lai ...")
            time.sleep(2**lan)
            continue

        if response.status_code == 200:
            return response.json()
        elif  response.status_code == 429 or response.status_code >= 500:
            print(f"Lần {lan}: server báo {response.status_code}, đợi rồi thử lại...")
            time.sleep(2 ** lan)
        else:
            raise Exception(f"Loi {response.status_code}: {response.text}")
    raise Exception(f"Đã thử {so_lan_thu} lần vẫn thất bại")

data=goi_api(URL,params)

df=pd.DataFrame(data["daily"])

df = df.rename(columns={
    "time":"ngay",
    "temperature_2m_max":"nhiet_max",
    "temperature_2m_min":"nhiet_min",
    "precipitation_sum":"luong_mua"
})

df["ngay"]=pd.to_datetime(df["ngay"]).dt.date

print (df.head(10))
print(df.dtypes)