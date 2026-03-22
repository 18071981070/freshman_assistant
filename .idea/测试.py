import requests

# 替换为你刚创建的高德API Key
AMAP_KEY = "5725f36203fb09b3f30cbb59c1743a9d"
city = "天津"  # 可修改为任意城市

# 1. 获取城市adcode
geo_url = f"https://restapi.amap.com/v3/geocode/geo?address={city}&key={AMAP_KEY}"
geo_resp = requests.get(geo_url).json()

if geo_resp["status"] == "1":
    adcode = geo_resp["geocodes"][0]["adcode"]
    # 2. 查询实时天气
    weather_url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={adcode}&key={AMAP_KEY}"
    weather_resp = requests.get(weather_url).json()
    
    if weather_resp["status"] == "1":
        live = weather_resp["lives"][0]
        print(f"✅ {live['city']} 当前天气：{live['weather']}")
        print(f"🌡️  温度：{live['temperature']}℃ | 体感温度：{live['humidity']}%")
    else:
        print("❌ 天气查询失败")
else:
    print("❌ 城市查询失败")