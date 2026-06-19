import json
import os
import time


class Cache:
    """简单缓存管理"""

    def __init__(self, cache_file="currency_cache.json", expiry=3600):
        self.cache_file = cache_file
        self.expiry = expiry  # 缓存过期时间（秒），默认1小时
        self._load_cache()

    def _load_cache(self):
        """加载缓存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
                print(f"✅ 加载缓存成功，共 {len(self.cache)} 条")
            except:
                self.cache = {}
        else:
            self.cache = {}

    def _save_cache(self):
        """保存缓存"""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def get(self, key):
        """获取缓存"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["timestamp"] < self.expiry:
                print(f"📦 缓存命中：{key}")
                return entry["data"]
            else:
                print(f"⏰ 缓存过期：{key}")
                del self.cache[key]
                self._save_cache()
        return None
    def set(self, key, data):
        """设置缓存"""
        self.cache[key] = {
            "data": data,
            "timestamp": time.time()
        }
        self._save_cache()
        print(f"💾 已缓存：{key}")


# 测试
if __name__ == "__main__":
    cache = Cache()
    cache.set("USD_CNY", 7.25)
    print(cache.get("USD_CNY"))  # 7.25

