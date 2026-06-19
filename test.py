import requests

BASE_URL = "http://localhost:8000"

def test_hello():
    resp = requests.get(f"{BASE_URL}/")
    print("根路径：", resp.json())

def test_rate():
    resp = requests.get(f"{BASE_URL}/rate", params={
        "base_currency": "USD",
        "target_currency": "CNY"
    })
    print("汇率：", resp.json())

def test_convert():
    resp = requests.post(f"{BASE_URL}/convert", json={
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "CNY"
    })
    print("转换结果：", resp.json())

def test_all_rates():
    resp = requests.get(f"{BASE_URL}/rate/all", params={
        "base_currency": "USD"
    })
    print("全部汇率：", resp.json())

if __name__ == "__main__":
    test_hello()
    test_rate()
    test_convert()
    test_all_rates()