import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from django.db.models import Avg, Count, Sum
from django.views.decorators.csrf import csrf_exempt

from .models import PlayerIndex
from .Utils import chat_with_LLM, get_team_state_by_player_name

from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.conf import settings
import jwt


@csrf_exempt
def create_player(request):
    """
    創建新的球員記錄。

    此視圖函數處理 POST 請求，並創建新的 PlayerIndex 記錄。
    如果創建成功，返回 201 狀態碼和新創建的球員詳細資訊。
    如果發生任何異常，則返回 400 錯誤。

    Args:
        request: Django HttpRequest 物件。

    Returns:
        JsonResponse: 包含新創建球員詳細資訊的 JSON 回應，或錯誤訊息。
    """
    if request.method == "POST":
        try:
            # 確保支持 JSON 格式的請求數據
            if request.content_type == "application/json":
                data = json.loads(request.body)
            else:
                data = request.POST
            player = PlayerIndex.objects.create(
                person_id=data.get("person_id"),
                player_last_name=data.get("player_last_name"),
                player_first_name=data.get("player_first_name"),
                team_id=data.get("team_id"),
                team_name=data.get("team_name"),
                country=data.get("country"),
                # 添加其他字段
            )
            return JsonResponse(
                {
                    "person_id": player.person_id,
                    "player_last_name": player.player_last_name,
                    "player_first_name": player.player_first_name,
                    "team_id": player.team_id,
                    "team_name": player.team_name,
                    "country": player.country,
                },
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


@csrf_exempt
def update_player(request, id):
    """
    更新現有的球員記錄。

    此視圖函數處理 PUT 請求，並更新 PlayerIndex 中的現有記錄。
    如果更新成功，返回 200 狀態碼和更新後的球員詳細資訊。
    如果找不到記錄，則返回 404 錯誤。如果發生任何其他異常，則返回 400 錯誤。

    Args:
        request: Django HttpRequest 物件。
        id: 要更新的球員的唯一 ID。

    Returns:
        JsonResponse: 包含更新後球員詳細資訊的 JSON 回應，或錯誤訊息。
    """
    if request.method == "PUT":
        try:
            data = QueryDict(request.body)
            player = PlayerIndex.objects.get(person_id=id)
            player.player_last_name = data.get(
                "player_last_name", player.player_last_name
            )
            player.player_first_name = data.get(
                "player_first_name", player.player_first_name
            )
            player.team_id = data.get("team_id", player.team_id)
            player.team_name = data.get("team_name", player.team_name)
            player.country = data.get("country", player.country)
            # 更新其他字段
            player.save()
            return JsonResponse(
                {
                    "person_id": player.person_id,
                    "player_last_name": player.player_last_name,
                    "player_first_name": player.player_first_name,
                    "team_id": player.team_id,
                    "team_name": player.team_name,
                    "country": player.country,
                },
                status=200,
            )
        except PlayerIndex.DoesNotExist:
            return JsonResponse({"error": "Record not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


@csrf_exempt
def delete_player(request, id):
    """
    刪除現有的球員記錄。

    此視圖函數處理 DELETE 請求，並刪除 PlayerIndex 中的現有記錄。
    如果刪除成功，返回 204 狀態碼。
    如果找不到記錄，則返回 404 錯誤。如果發生任何其他異常，則返回 400 錯誤。

    Args:
        request: Django HttpRequest 物件。
        id: 要刪除的球員的唯一 ID。

    Returns:
        JsonResponse: 成功刪除的回應，或錯誤訊息。
    """
    if request.method == "DELETE":
        try:
            player = PlayerIndex.objects.get(person_id=id)
            player.delete()
            return JsonResponse({}, status=204)
        except PlayerIndex.DoesNotExist:
            return JsonResponse({"error": "Record not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


def get_player(request, id):
    """
    根據提供的球員 ID，從資料庫中檢索球員的詳細資訊。

    此視圖函數處理 GET 請求，並嘗試從 PlayerIndex 模型中獲取與給定 ID 匹配的記錄。
    如果找到記錄，它將以 JSON 格式返回球員的姓名、國家和球隊名稱。
    如果找不到記錄，則返回 404 錯誤。如果發生任何其他異常，則返回 400 錯誤。

    Args:
        request: Django HttpRequest 物件。
        id: 要檢索的球員的唯一 ID。

    Returns:
        JsonResponse: 包含球員詳細資訊的 JSON 回應，或錯誤訊息。
    """
    if request.method == "GET":
        try:
            # 根據 ID 查找記錄
            record = PlayerIndex.objects.get(person_id=id)

            # 返回記錄的詳細信息
            return JsonResponse(
                {
                    "PLAYER_LAST_NAME": record.player_last_name,
                    "PLAYER_FIRST_NAME": record.player_first_name,
                    "COUNTRY": record.country,
                    "team_name": record.team_name,
                },
                status=200,
            )

        except PlayerIndex.DoesNotExist:
            # 如果找不到記錄，返回 404 錯誤
            return JsonResponse({"error": "Record not found"}, status=404)

        except Exception as e:
            # 處理其他異常
            return JsonResponse({"error": str(e)}, status=400)

    # 不支持的請求方法
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


# Create your views here.
def get_player_by_team(request, team_name, option):
    """
    根據提供的球隊名稱，從資料庫中檢索屬於該球隊的所有球員，並根據指定的選項進行排序。

    此視圖函數處理 GET 請求，並從 PlayerIndex 模型中篩選出 team_name 字段與給定 team_name 匹配的記錄。
    結果會根據 URL 中提供的 'option' 參數進行排序。
    返回的 JSON 響應包含球員的姓名、國家、球隊名稱以及根據 'option' 參數動態獲取的字段值。
    如果找不到記錄，則返回 404 錯誤。如果發生任何其他異常，則返回 400 錯誤。

    Args:
        request: Django HttpRequest 物件。
        team_name: 要檢索球員的球隊名稱。
        option: 用於排序球員記錄的字段名稱。

    Returns:
        JsonResponse: 包含球員詳細資訊的 JSON 回應，或錯誤訊息。
    """
    if request.method == "GET":
        try:
            # 根據 ID 查找記錄
            records = PlayerIndex.objects.filter(team_name=team_name).order_by(option)

            # 返回記錄的詳細信息
            data = [
                {
                    "PLAYER_LAST_NAME": record.player_last_name,
                    "PLAYER_FIRST_NAME": record.player_first_name,
                    "COUNTRY": record.country,
                    "team_name": record.team_name,
                    "ITEM": getattr(record, option, None),  # 動態獲取字段值
                }
                for record in records
            ]

            return JsonResponse(data, status=200, safe=False)

        except PlayerIndex.DoesNotExist:
            # 如果找不到記錄，返回 404 錯誤
            return JsonResponse({"error": "Record not found"}, status=404)

        except Exception as e:
            # 處理其他異常
            return JsonResponse({"error": str(e)}, status=400)

    # 不支持的請求方法
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


# Create your views here.
def get_item_by_position(request, position, item):
    """
    根據提供的球員位置和統計項目，從資料庫中檢索按位置分組的平均統計數據。

    此視圖函數處理 GET 請求，並使用 Django 的聚合功能（Avg）計算 PlayerIndex 模型中，
    按指定 'position' 分組的特定 'item' 的平均值。
    返回的 JSON 響應包含每個位置及其對應的平均 'item' 值。
    如果找不到記錄，則返回 404 錯誤。如果發生任何其他異常，則返回 400 錯誤。

    Args:
        request: Django HttpRequest 物件。
        position: 用於分組的球員位置字段名稱。
        item: 要計算平均值的統計項目字段名稱。

    Returns:
        JsonResponse: 包含按位置分組的平均統計數據的 JSON 回應，或錯誤訊息。
    """
    if request.method == "GET":
        try:
            # 根據 ID 查找記錄
            records = PlayerIndex.objects.values(position).annotate(ans=Avg(item))

            # 返回記錄的詳細信息
            data = [
                {
                    "position": record[position],
                    "item": record["ans"],
                }
                for record in records
            ]

            return JsonResponse(data, status=200, safe=False)

        except PlayerIndex.DoesNotExist:
            # 如果找不到記錄，返回 404 錯誤
            return JsonResponse({"error": "Record not found"}, status=404)

        except Exception as e:
            # 處理其他異常
            return JsonResponse({"error": str(e)}, status=400)

    # 不支持的請求方法
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


# 從球員找球隊數據
def get_team_id_by_name(request, name):
    """
    根據提供的球員姓名，從資料庫中檢索球員所屬的球隊 ID。

    此視圖函數處理 GET 請求，並從 PlayerIndex 模型中篩選出 player_slug 字段與給定球員姓名匹配的記錄。
    返回的 JSON 響應包含球隊的 ID。
    如果找不到記錄，則返回 404 錯誤。如果發生任何其他異常，則返回 400 錯誤。

    Args:
        request: Django HttpRequest 物件。
        name: 要檢索球隊 ID 的球員姓名。

    Returns:
        JsonResponse: 包含球隊 ID 的 JSON 回應，或錯誤訊息。
    """
    if request.method == "GET":
        try:
            # 根據 ID 查找記錄
            records = PlayerIndex.objects.filter(player_slug=name)

            # 返回記錄的詳細信息
            data = [{"team_id": record.team_id} for record in records]

            return JsonResponse(data, status=200, safe=False)

        except PlayerIndex.DoesNotExist:
            # 如果找不到記錄，返回 404 錯誤
            return JsonResponse({"error": "Record not found"}, status=404)

        except Exception as e:
            # 處理其他異常
            return JsonResponse({"error": str(e)}, status=400)

    # 不支持的請求方法
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


def get_team_state(request, name):
    """
    根據提供的球員姓名，從外部 NBA 統計 API 檢索該球員所屬球隊的統計數據。

    此視圖函數處理 GET 請求，並首先使用 `get_team_state_by_player_name` 輔助函數獲取球員的球隊 ID。
    然後，它向 NBA 官方統計 API 發出請求，檢索該球隊的傳統統計數據（例如，每場得分、籃板、助攻等）。
    使用 BeautifulSoup 解析 API 返回的 HTML 內容，提取相關的統計數據標籤、排名和數值。
    最終將這些統計數據以 JSON 格式返回。
    如果找不到記錄或 API 請求失敗，則返回相應的錯誤訊息。

    Args:
        request: Django HttpRequest 物件。
        name: 要檢索球隊統計數據的球員姓名。

    Returns:
        JsonResponse: 包含球隊統計數據的 JSON 回應，或錯誤訊息。
    """
    if request.method == "GET":
        try:
            # 根據 ID 查找記錄
            records = get_team_state_by_player_name(name)

            context = requests.get(
                f"https://www.nba.com/stats/team/{records[0]['team_id']}/traditional?PerMode=PerGame"
            )
            soup = BeautifulSoup(context.text)
            stats_divs = soup.find_all("div", class_="TeamHeader_rank__lMnzF")

            stats = {}
            # 找到統計類型（PPG、RPG 等）
            for stat_div in stats_divs:
                label = stat_div.find("div", class_="TeamHeader_rankLabel__5mPf9").text

                # 找到排名（Ordinal）
                ordinal = stat_div.find(
                    "div", class_="TeamHeader_rankOrdinal__AaXPR"
                ).text

                # 找到統計數值（Value）
                value = stat_div.find("div", class_="TeamHeader_rankValue__ZGDCq").text

                stats[label] = {"rank": ordinal, "value": value}

                # print(stats)
            print(type(stats))
            return JsonResponse(stats, status=200)

        except PlayerIndex.DoesNotExist:
            # 如果找不到記錄，返回 404 錯誤
            return JsonResponse({"error": "Record not found"}, status=404)

        except Exception as e:
            # 處理其他異常
            return JsonResponse({"error": str(e)}, status=400)

    # 不支持的請求方法
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


def get_profile_player(request, name):
    if request.method == "GET":
        ans = chat_with_LLM(name)
        print(ans)
    return JsonResponse({"profile": ans})


def search_players_by_team(request, team_name):
    """
    查找屬於特定球隊的所有球員。
    """
    if request.method == "GET":
        try:
            players = PlayerIndex.objects.filter(team_name=team_name)
            data = [
                {
                    "PLAYER_LAST_NAME": player.player_last_name,
                    "PLAYER_FIRST_NAME": player.player_first_name,
                    "POSITION": player.position,
                    "JERSEY_NUMBER": player.jersey_number,
                }
                for player in players
            ]
            return JsonResponse(data, status=200, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "只允許 POST"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    # **模擬用戶驗證**
    if username == "admin" and password == "password123":
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(hours=1),  # 設定 1 小時過期
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        # **將 Token 存入 Cookie**
        response = JsonResponse({"message": "登入成功"})
        response.set_cookie(
            "jwt_token", token, httponly=True, max_age=300
        )  # 5 分鐘過期
        return response
    response = JsonResponse({"error": "登入失敗"})
    response.delete_cookie("jwt_token")
    return JsonResponse({"error": "無效的憑證"}, status=401)
