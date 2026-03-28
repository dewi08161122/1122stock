import requests

def get_json_by_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.twse.com.tw/"
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            print("請求失敗")
            return None
        data = response.json()
    except Exception as e:
        print(f"網路連線異常: {e}")
    return data