# -*- coding: utf-8 -*-
"""
Habit Tracker API Pytest Test Cases
"""

import pytest
import json
from app import create_app, db
from app.models import User  # 匯入 User model
from werkzeug.security import generate_password_hash

# 測試設定
# 注意：根據專案的 Blueprint 設定，API 路徑可能是 /api/habits
# 在此我們遵循使用者請求，使用 /habits，如果測試失敗，請先確認 API 路徑是否正確
API_URL = '/api/habits'


@pytest.fixture(scope='function')
def client():
    """
    Pytest Fixture: 設定測試環境

    這個 fixture 會在每個測試函式執行前被呼叫，並提供一個獨立的測試環境。
    - scope='function': 確保每個測試函式都使用獨立的、乾淨的資料庫。
    - 建立一個測試專用的 Flask app instance。
    - 設定資料庫為 in-memory SQLite，避免影響開發資料庫。
    - 建立所有資料庫表格。
    - 建立一個 user_id=1 的測試使用者，因為 API 目前硬編碼該使用者 ID。
    - yield 一個 test client 供測試函式使用。
    - 測試結束後，清除所有資料庫表格。
    """
    # Arrange: 建立一個測試用的 Flask app instance
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,  # 在測試中通常會禁用 CSRF 保護
    })

    # 在應用程式情境 (application context) 中建立資料庫表格和測試使用者
    with app.app_context():
        db.create_all()
        # 因為 habits API 目前硬編碼 user_id=1，所以我們必須先建立這個使用者
        test_user = User(
            id=1,
            email='test@example.com',
            password_hash=generate_password_hash('password', method='pbkdf2:sha256')
        )
        db.session.add(test_user)
        db.session.commit()

    # Act: 使用 yield 將 test_client 提供給測試函式
    yield app.test_client()

    # Teardown: 測試結束後，清除資料庫
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_post_habit(client):
    """
    測試 `POST /habits` 端點

    GIVEN: 一個 Flask application 的 test client
    WHEN: 對 '/habits' 發送一個 POST 請求來建立新習慣
    THEN: 應該回傳狀態碼 201，且回傳的 JSON 內容包含正確的習慣名稱和類型
    """
    # Arrange (安排): 準備測試資料和請求標頭
    new_habit_data = {
        'name': '每天運動 30 分鐘',
        'type': 'positive'  # 新增 'type' 欄位
    }
    headers = {
        'Content-Type': 'application/json'
    }

    # Act (執行): 發送 API 請求
    response = client.post(
        API_URL,
        data=json.dumps(new_habit_data),
        headers=headers
    )

    # Assert (斷言): 驗證回傳結果
    assert response.status_code == 201, f"預期狀態碼為 201，但收到 {response.status_code}"

    response_json = response.get_json()
    assert response_json is not None, "回傳的 body 不應為空"
    assert 'name' in response_json, "回傳的 JSON 應包含 'name' 欄位"
    assert response_json['name'] == new_habit_data['name'], "回傳的習慣名稱不正確"
    assert 'type' in response_json, "回傳的 JSON 應包含 'type' 欄位"
    assert response_json['type'] == new_habit_data['type'], "回傳的習慣類型不正確"
    assert 'id' in response_json, "回傳的 JSON 應包含 'id' 欄位"


def test_get_habits(client):
    """
    測試 `GET /habits` 端點

    GIVEN: 一個 Flask application 的 test client
    WHEN: 資料庫中已存在一個習慣，並對 '/habits' 發送 GET 請求
    THEN: 應該回傳狀態碼 200，且回傳的列表應包含先前建立的習慣
    """
    # Arrange (安排): 先透過 POST 建立一筆習慣資料，為 GET 測試做準備
    habit_to_create = {
        'name': '每週閱讀一本書',
        'type': 'positive'  # 新增 'type' 欄位
    }
    headers = {
        'Content-Type': 'application/json'
    }
    post_response = client.post(
        API_URL,
        data=json.dumps(habit_to_create),
        headers=headers
    )
    assert post_response.status_code == 201, "Arrange 階段建立習慣失敗，無法進行 GET 測試"

    # Act (執行): 發送 GET 請求來獲取所有習慣
    response = client.get(API_URL)

    # Assert (斷言): 驗證回傳結果
    assert response.status_code == 200, f"預期狀態碼為 200，但收到 {response.status_code}"

    response_json = response.get_json()
    assert isinstance(response_json, list), "回傳的資料型別應為 list"
    assert len(response_json) > 0, "回傳的列表不應為空"

    # 檢查列表中是否包含我們剛剛在 Arrange 階段建立的習慣
    created_habit_name = habit_to_create['name']
    assert any(habit['name'] == created_habit_name for habit in response_json), f"列表中找不到名稱為 '{created_habit_name}' 的習慣"
