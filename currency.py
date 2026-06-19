import requests
from datetime import datetime,timedelta

class Currency:
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"

    def get_rate(self,base_currency="USD",target_currency="CND"):
        """
        获取汇率
        base_currency: 基础货币（如 USD）
        target_currency: 目标货币（如 CNY）
        返回：1 base_currency = X target_currency
        """
        try:
            url = f'{self.base_url}{base_currency}'
            resp = requests.get(url,timeout=10)
            resp.raise_for_status()
            data = resp.json()

            rate = data["rates"].get(target_currency)
            if not rate:
                print(f"❌ 不支持的货币：{target_currency}")
                return None

            return rate

        except requests.exceptions.Timeout:
            print("⏰ 请求超时")
            return None
        except requests.exceptions.ConnectionError:
            print("🌐 网络连接失败")
            return None
        except Exception as e:
            print(f"❌ 获取汇率失败：{e}")
            return None

    def convert(self, amount, from_currency, to_currency):
        """
        货币转换
        amount: 金额
        from_currency: 源货币
        to_currency: 目标货币
        返回：转换后的金额
        """
        rate = self.get_rate(from_currency, to_currency)
        if rate is None:
            return None
        return amount * rate

# 测试
if __name__ == "__main__":
    converter = Currency()

    # 测试1：获取汇率
    rate = converter.get_rate("USD", "CNY")
    print(f"1 USD = {rate:.2f} CNY")

    # 测试2：货币转换
    result = converter.convert(100, "USD", "CNY")
    print(f"100 USD = {result:.2f} CNY")






















