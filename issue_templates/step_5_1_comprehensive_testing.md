# [Phase 5] Step 5.1: テスト完備

## 📋 概要
アプリケーション全体の包括的なテストスイートを実装し、品質保証とCI/CDパイプラインを構築します。

## 🎯 目標
- 80%以上のテストカバレッジ
- CI/CDパイプライン
- 自動化された品質チェック

## ⏰ 所要時間
6-8時間

## 📋 実装項目

### 1. ユニットテスト
```python
# tests/unit/test_timer_model.py
def test_pomodoro_session_initialization():
    session = PomodoroSession()
    assert session.state == TimerState.IDLE
    assert session.work_duration == 25

def test_start_work_session():
    session = PomodoroSession()
    session.start_work_session()
    assert session.state == TimerState.WORK
    assert session.remaining_time == 1500

def test_session_state_transitions():
    session = PomodoroSession()
    session.start_work_session()
    session.complete_session()
    assert session.current_session == 1
    assert session.state == TimerState.SHORT_BREAK

# tests/unit/test_statistics_service.py
def test_daily_stats_calculation():
    # モックデータでの統計計算テスト
    pass

def test_productivity_score_calculation():
    # 生産性スコアの計算テスト
    pass
```

### 2. 統合テスト
```python
# tests/integration/test_api_endpoints.py
def test_start_timer_endpoint(client):
    response = client.post('/api/timer/start')
    assert response.status_code == 200
    assert response.json['status'] == 'started'

def test_websocket_connection(socketio_client):
    socketio_client.connect()
    received = socketio_client.get_received()
    assert len(received) > 0
    assert received[0]['name'] == 'status'

# tests/integration/test_database_operations.py
def test_session_save_and_retrieve():
    # データベース操作の統合テスト
    pass
```

### 3. E2Eテスト
```python
# tests/e2e/test_user_flows.py
def test_complete_pomodoro_cycle(browser):
    browser.get('http://localhost:5000')
    
    # タイマー開始
    start_button = browser.find_element_by_id('start-btn')
    start_button.click()
    
    # タイマー表示確認
    timer_display = browser.find_element_by_class_name('timer-display')
    assert '24:' in timer_display.text
    
    # 設定変更テスト
    settings_btn = browser.find_element_by_id('settings-btn')
    settings_btn.click()
    
    work_duration_input = browser.find_element_by_id('work-duration')
    work_duration_input.clear()
    work_duration_input.send_keys('30')
    
    save_btn = browser.find_element_by_id('save-settings-btn')
    save_btn.click()
    
    # 設定反映確認
    assert timer_display.text == '30:00'
```

### 4. テスト設定とFixtures
```python
# tests/conftest.py
import pytest
from app import create_app
from models.database import SessionHistory

@pytest.fixture
def app():
    app = create_app(testing=True)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_db():
    db = SessionHistory(':memory:')
    yield db
    # クリーンアップ

# tests/fixtures/mock_services.py
class MockTimeProvider(TimeProvider):
    def __init__(self, initial_time: datetime):
        self._current_time = initial_time
    
    def now(self) -> datetime:
        return self._current_time
    
    def advance_time(self, seconds: int):
        """テスト用：時間を進める"""
        self._current_time += timedelta(seconds=seconds)
```

### 5. CI/CDパイプライン
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run linting
      run: |
        flake8 .
        black --check .
    
    - name: Run unit tests
      run: pytest tests/unit -v --cov=app
    
    - name: Run integration tests
      run: pytest tests/integration -v
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### 6. テスト用requirements
```txt
# requirements-test.txt
pytest==7.4.0
pytest-cov==4.1.0
pytest-flask==1.2.0
pytest-socketio==0.14.0
selenium==4.10.0
black==23.7.0
flake8==6.0.0
mypy==1.5.0
```

## ✅ 受入基準
- [ ] ユニットテストのカバレッジが80%以上
- [ ] 全ての統合テストがパスする
- [ ] E2Eテストが主要フローをカバーする
- [ ] CI/CDパイプラインが正常に動作する
- [ ] コード品質チェックがパスする
- [ ] テスト実行時間が5分以内

## 🧪 テスト項目
- [ ] 全モデルクラスのユニットテスト
- [ ] 全APIエンドポイントの統合テスト
- [ ] WebSocket通信のテスト
- [ ] データベース操作のテスト
- [ ] フロントエンドユーザーフローのE2Eテスト
- [ ] エラーハンドリングのテスト

## 📝 実装ファイル
- `tests/unit/` (ユニットテスト)
- `tests/integration/` (統合テスト)
- `tests/e2e/` (E2Eテスト)
- `tests/conftest.py` (pytest設定)
- `.github/workflows/test.yml` (CI/CD)
- `requirements-test.txt`

## 🏷️ ラベル
- `phase-5`
- `testing`
- `quality-assurance`
- `ci-cd`

## 📚 参考資料
- [pytest Documentation](https://docs.pytest.org/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [GitHub Actions](https://docs.github.com/en/actions)

## 📝 備考
テストは継続的に実行され、新機能追加時にも回帰テストとして機能するよう設計してください。