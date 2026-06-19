from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from currency import Currency
from cache import Cache
import uvicorn
import requests

app = FastAPI(tilte = "汇率查询 API")

# 初始化
converter = Currency()
cache = Cache(expiry=3600)

# 请求体模型
class ConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

class RateRequest(BaseModel):
    base_currency: str
    target_currency: str

@app.get("/")
def root():
    return {
        "message": "汇率查询 API",
        "endpoints": {
            "/rate?base=USD&target=CNY": "获取汇率",
            "/convert": "货币转换（POST）",
            "/supported": "查看支持的货币"
        }
    }

@app.get("/rate")
def get_rate(base_currency: str = "USD", target_currency: str = "CNY"):
    """
    获取实时汇率
    """
    # 检查缓存
    cache_key = f"{base_currency}_{target_currency}"
    cached = cache.get(cache_key)
    if cached:
        return {
            "base": base_currency,
            "target": target_currency,
            "rate": cached,
            "source": "cache"
        }

    # 请求实时汇率
    rate = converter.get_rate(base_currency, target_currency)
    if rate is None:
        raise HTTPException(status_code=404, detail="不支持的货币")

    # 存入缓存
    cache.set(cache_key, rate)

    return {
        "base": base_currency,
        "target": target_currency,
        "rate": rate,
        "source": "api"
    }


@app.post("/convert")
def convert(request: ConvertRequest):
    """
    货币转换
    """
    result = converter.convert(
        request.amount,
        request.from_currency,
        request.to_currency
    )

    if result is None:
        raise HTTPException(status_code=404, detail="不支持的货币")

    return {
        "from": request.from_currency,
        "to": request.to_currency,
        "amount": request.amount,
        "result": round(result, 2)
    }

@app.get("/supported")
def supported_currencies():
    """
    获取支持的货币列表
    """
    # 常见货币列表
    currencies = [
        "USD", "CNY", "EUR", "GBP", "JPY", "KRW",
        "AUD", "CAD", "CHF", "HKD", "SGD", "NZD"
    ]
    return {"supported_currencies": currencies}

@app.get("/rate/all")
def get_all_rates(base_currency: str = "USD"):
    """
    获取某一货币对所有其他货币的汇率
    """
    cache_key = f"all_{base_currency}"
    cached = cache.get(cache_key)
    if cached:
        return {
            "base": base_currency,
            "rates": cached,
            "source": "cache"
        }

    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        rates = data.get("rates", {})

        # 只保留常见货币
        common = ["CNY", "EUR", "GBP", "JPY", "KRW", "AUD", "CAD", "CHF", "HKD", "SGD"]
        filtered = {k: rates[k] for k in common if k in rates}

        cache.set(cache_key, filtered)

        return {
            "base": base_currency,
            "rates": filtered,
            "source": "api"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



