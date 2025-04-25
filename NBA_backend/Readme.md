# Backend Andy

此資料夾包含一個與 NBA 相關的 Django 應用程序，提供了多種功能來管理和查詢球員和球隊的信息。

## 文件結構

- `manage.py`：Django 的管理腳本，用於運行伺服器、遷移數據庫等。
- `poetry.lock` 和 `pyproject.toml`：用於管理 Python 依賴的 Poetry 配置文件。

### NBA 應用

- `Utils.py`：包含輔助函數，如 `get_team_state_by_player_name` 和 `chat_with_LLM`。
- `apps.py`：定義應用配置類 `NbaConfig`。
- `middleware.py`：定義中間件 `TokenAuthMiddleware`，用於請求處理和令牌驗證。
- `models.py`：定義數據模型 `PlayerIndex`。
- `views.py`：提供多個視圖函數，用於管理和查詢球員和球隊的信息。

## 視圖使用說明

### 創建、更新和刪除球員

- **create_player**：使用 POST 請求創建新的球員記錄。需要提供球員的詳細信息，如 `person_id`、`player_last_name`、`player_first_name` 等。
- **update_player**：使用 PUT 請求更新現有的球員記錄。需要提供球員的唯一 ID 和要更新的字段。
- **delete_player**：使用 DELETE 請求刪除現有的球員記錄。需要提供球員的唯一 ID。

### 檢索球員和球隊信息

- **get_player**：使用 GET 請求根據球員 ID 檢索球員的詳細信息。
- **get_player_by_team**：使用 GET 請求根據球隊名稱檢索球員，並根據指定選項排序。
- **get_item_by_position**：使用 GET 請求根據球員位置和統計項目檢索平均統計數據。
- **get_team_id_by_name**：使用 GET 請求根據球員姓名檢索球隊 ID。
- **get_team_state**：使用 GET 請求從外部 API 檢索球隊的統計數據。
- **get_profile_player**：使用 GET 請求，使用 LLM 獲取球員資料。
- **search_players_by_team**：使用 GET 請求查找屬於特定球隊的所有球員。

### 登錄和受保護的視圖

- **login**：使用 POST 請求模擬用戶登錄並生成 JWT。


應用程序使用 JWT（JSON Web Token）來驗證用戶請求。中間件 `TokenAuthMiddleware` 負責從請求中提取 JWT，並驗證其有效性。具體步驟如下：

- **Token 提取**：從請求的 cookies 中提取 `jwt_token`。
- **Token 驗證**：使用 `jwt.decode` 方法解碼 token，並使用應用的 `SECRET_KEY` 進行驗證。
- **錯誤處理**：如果 token 過期或無效，返回 401 未授權錯誤。

## 使用方式
1. **安裝依賴**：
   - 使用 Poetry 安裝依賴：`poetry install`

2. **運行伺服器**：
   - 使用 Django 的管理命令運行伺服器：`poetry rjun python manage.py runserver`

3. **使用時記得要先login，確保token存放在cookies中**

## 注意事項

- 確保數據庫已正確配置並遷移。
- 根據需要調整中間件和視圖的配置。
