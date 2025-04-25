from .models import PlayerIndex
from openai import OpenAI
from dotenv import load_dotenv
import os


def get_team_state_by_player_name(name):
    """
    查找資料庫中是否有與提供的 ID 匹配的記錄。
    """
    try:
        # 根據 ID 查找記錄
        records = PlayerIndex.objects.filter(player_slug=name)

        # 返回記錄的詳細信息
        data = [{"team_id": record.team_id} for record in records]

        return data

    except PlayerIndex.DoesNotExist:
        # 如果找不到記錄，返回 404 錯誤
        return "NoData"

    except Exception as e:
        # 處理其他異常
        return "Error"


def chat_with_LLM(name):
    load_dotenv()
    # 設置 OpenAI API Key
    api_key = os.getenv("api_key")
    print(api_key)
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"告訴我{name}相關的資料, 他是一名NBA球員我希望可以獲得他屬於哪支球隊打什麼位置及生涯成就與數據",
            },
        ],
    )

    return completion.choices[0].message.content
