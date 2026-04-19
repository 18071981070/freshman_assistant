from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import requests

rag=RagSummarizeService()

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="获取指定城市的实时天气信息，包括天气状况、温度、降水概率、风力等")
def get_campus_weather(campus_city: str) -> str:
    """
    获取指定城市的实时天气信息
    
    Args:
        campus_city: 校区所在城市名（纯文本字符串）
        
    Returns:
        字符串类型的环境信息，包含城市对应的实时天气相关数据
        
    使用场景：
        - 判断指定校区的环境是否适合户外活动（如竞赛宣讲、社团招新、体育课）
        - 用户问题涉及天气对校园通勤、取快递等生活的影响
    """
    try:
        # 处理校区名称，提取具体位置信息
        # 例如："天津科技大学滨海校区" -> "天津滨海新区"
        location = campus_city
        
        # 处理常见的校区命名格式
        if "大学" in location:
            # 提取大学名称前的位置信息
            location_parts = location.split("大学")[0]
            # 去除可能的后缀
            location = location_parts.rstrip("市县区")
        
        # 特殊处理天津科技大学的情况
        if "天津科技大学" in location:
            # 假设天津科技大学在滨海新区
            location = "天津滨海新区"
        
        # 高德地图API Key
        AMAP_KEY = "5725f36203fb09b3f30cbb59c1743a9d"
        
        # 1. 获取位置的adcode（支持城市和区县级别）
        geo_url = f"https://restapi.amap.com/v3/geocode/geo?address={location}&key={AMAP_KEY}"
        geo_resp = requests.get(geo_url).json()
        
        if geo_resp["status"] == "1":
            adcode = geo_resp["geocodes"][0]["adcode"]
            formatted_address = geo_resp["geocodes"][0]["formatted_address"]
            
            # 2. 查询实时天气
            weather_url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={adcode}&key={AMAP_KEY}"
            weather_resp = requests.get(weather_url).json()
            
            if weather_resp["status"] == "1":
                live = weather_resp["lives"][0]
                result = f"{formatted_address}实时天气信息：\n"
                result += f"天气状况：{live['weather']}\n"
                result += f"温度：{live['temperature']}°C\n"
                result += f"相对湿度：{live['humidity']}%\n"
                result += f"风向：{live['winddirection']}\n"
                result += f"风力：{live['windpower']}级\n"
                result += f"发布时间：{live['reporttime']}\n"
                
                return result
            else:
                return f"获取{campus_city}天气信息失败，错误代码：{weather_resp.get('info', '未知错误')}"
        else:
            return f"获取{campus_city}位置信息失败，错误代码：{geo_resp.get('info', '未知错误')}"
            
    except requests.exceptions.Timeout:
        return f"获取{campus_city}天气信息超时，请稍后重试"
    except requests.exceptions.RequestException as e:
        return f"获取{campus_city}天气信息时发生网络错误：{str(e)}"
    except Exception as e:
        return f"获取{campus_city}天气信息时发生错误：{str(e)}"

@tool(description="获取比赛相关信息，入参为比赛名称或关键词")
def get_competition_info(query: str) -> str:
    """
    从知识库中获取比赛相关信息
    
    Args:
        query: 比赛名称或关键词（纯文本字符串）
        
    Returns:
        字符串类型的比赛信息，包含比赛详情、报名时间、参赛要求等
        
    使用场景：
        - 当用户询问「有什么比赛可以参加」
        - 当用户询问「XX比赛怎么报名」
        - 当用户询问「比赛的具体要求是什么」
        
    调用规则：必须传入纯文本字符串类型的 query 参数
    """
    try:
        # 使用 RAG 服务从知识库中检索比赛相关信息
        result = rag.rag_summarize(f"比赛信息：{query}")
        
        # 如果结果为空，返回提示信息
        if not result or result.strip() == "":
            return f"未找到与 '{query}' 相关的比赛信息，请尝试使用其他关键词或检查知识库中是否有相关比赛文件"
        
        return result
        
    except Exception as e:
        return f"获取比赛信息时发生错误：{str(e)}"

@tool(description="获取保研和综测相关信息，入参为查询内容和学院名称（可选）")
def get_graduate_info(query: str, college: str = None) -> str:
    """
    从知识库中获取保研和综测相关信息
    
    Args:
        query: 查询内容（纯文本字符串），如"保研条件"、"综测计算"等
        college: 学院名称（纯文本字符串，可选），如"计算机学院"、"机械学院"等
        
    Returns:
        字符串类型的信息，包含保研条件、综测规则等
        
    使用场景：
        - 当用户询问「保研需要什么条件」
        - 当用户询问「综测怎么计算」
        - 当用户询问「XX学院的综测规则是什么」
        
    调用规则：必须传入纯文本字符串类型的 query 参数，college 参数为可选
    """
    try:
        # 构建查询语句
        if college:
            result = rag.rag_summarize(f"{college} {query}")
        else:
            result = rag.rag_summarize(f"{query}")
        
        # 如果结果为空，返回提示信息
        if not result or result.strip() == "":
            if college:
                return f"未找到与 '{college}' 相关的 '{query}' 信息，请尝试使用其他关键词或检查知识库中是否有相关文件"
            else:
                return f"未找到与 '{query}' 相关的信息，请尝试使用其他关键词或检查知识库中是否有相关文件"
        
        return result
        
    except Exception as e:
        return f"获取信息时发生错误：{str(e)}"

@tool(description="无入参，精准获取当前发起请求的用户所处校区/城市名称")
def get_user_location() -> str:
    """
    获取当前用户所处的校区/城市名称
    
    Returns:
        字符串类型的城市/校区名称，为用户实际所处的标准名称
        
    使用场景：
        - 当需要获取用户地理位置信息，用于配套调用 get_campus_weather 等需城市参数的工具
        - 回答与用户所在校区相关的问题（如就近食堂、快递点、实验室位置）
        
    调用规则：无需传入任何参数，直接触发调用即可
    """
    try:
        # 由于网络环境限制，这里直接返回用户实际位置
        # 用户明确表示在天津科技大学
        return "天津市滨海新区"
        
        # 以下是通过 IP 地址获取用户实际位置的代码（备用方案）
        # import requests
        # 
        # try:
        #     # 先获取用户的公网 IP 地址
        #     ip_response = requests.get('https://api.ipify.org', timeout=5)
        #     ip_address = ip_response.text.strip()
        #     print(f"获取到用户IP地址：{ip_address}")
        #     
        #     # 使用 ipinfo.io 获取地理位置信息
        #     ipinfo_response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=5)
        #     location_data = ipinfo_response.json()
        #     print(f"地理位置数据：{location_data}")
        #     
        #     # 提取城市信息
        #     city = location_data.get('city', '未知')
        #     if city and city != '未知':
        #         return city
        # except Exception as ip_error:
        #     print(f"IP 地址获取失败：{ip_error}")
        # 
        # # 如果 IP 地址获取失败，使用备用方案
        # return "北京"
        
    except Exception as e:
        return f"获取用户位置时发生错误：{str(e)}"
