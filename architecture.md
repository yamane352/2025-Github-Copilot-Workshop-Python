# ポモドーロタイマー Webアプリケーション アーキテクチャ設計書

## 📋 概要

本文書は、Flask + HTML/CSS/JavaScript を使用したポモドーロタイマーWebアプリケーションのアーキテクチャ設計を記載しています。ユニットテストの容易性、保守性、拡張性を重視した設計となっています。

## 🏗️ アーキテクチャパターン

### 基本パターン: **MVC + Dependency Injection + WebSocket**

- **Model**: データとビジネスロジック（タイマー状態、セッション管理）
- **View**: フロントエンド UI（HTML/CSS/JavaScript）
- **Controller**: API エンドポイントとWebSocket通信制御
- **Service Layer**: 外部依存の抽象化とビジネスロジック
- **Dependency Injection**: テスト容易性とモック化対応

## 📁 プロジェクト構造

```
pomodoro_app/
├── app.py                          # Flaskアプリケーション本体
├── config/
│   ├── __init__.py
│   ├── settings.py                 # アプリケーション設定
│   └── test_settings.py            # テスト専用設定
├── interfaces/                     # 抽象インターフェース
│   ├── __init__.py
│   ├── timer_interface.py          # タイマー関連インターフェース
│   ├── notification_interface.py   # 通知サービスインターフェース
│   └── websocket_interface.py      # WebSocket通信インターフェース
├── models/                         # データモデル
│   ├── __init__.py
│   ├── timer_model.py             # タイマー状態管理
│   └── session_model.py           # セッション履歴管理
├── services/                       # ビジネスロジック・外部依存
│   ├── __init__.py
│   ├── timer_service.py           # タイマーサービス
│   ├── notification_service.py    # 通知機能
│   └── time_provider.py           # 時間制御サービス
├── controllers/                    # リクエスト制御
│   ├── __init__.py
│   ├── timer_controller.py        # タイマー制御ロジック
│   └── api_controller.py          # REST API エンドポイント
├── adapters/                       # 外部システム適応
│   ├── __init__.py
│   └── websocket_adapter.py       # WebSocket通信アダプター
├── dependency_injection/           # DI コンテナ
│   ├── __init__.py
│   └── container.py               # DIコンテナ実装
├── static/                         # 静的ファイル
│   ├── css/
│   │   ├── main.css
│   │   └── responsive.css
│   ├── js/
│   │   ├── pomodoro_timer.js
│   │   ├── websocket_client.js
│   │   └── ui_controller.js
│   └── images/
├── templates/                      # HTMLテンプレート
│   └── index.html
├── tests/                          # テストスイート
│   ├── unit/                      # ユニットテスト
│   │   ├── test_timer_model.py
│   │   ├── test_timer_service.py
│   │   └── test_timer_controller.py
│   ├── integration/               # 統合テスト
│   │   ├── test_api_endpoints.py
│   │   └── test_websocket_communication.py
│   ├── e2e/                       # E2Eテスト
│   │   └── test_user_flows.py
│   ├── fixtures/                  # テスト用フィクスチャ
│   │   ├── mock_services.py
│   │   └── test_data.py
│   └── conftest.py               # pytest設定
├── requirements.txt               # 依存パッケージ
├── requirements-test.txt          # テスト用依存パッケージ
├── pytest.ini                    # pytest設定
├── Makefile                       # 開発用コマンド
└── README.md                      # プロジェクト説明
```

## 🔧 技術スタック

### バックエンド
- **Framework**: Flask 2.3+
- **WebSocket**: Flask-SocketIO
- **Testing**: pytest, pytest-cov
- **Type Hints**: Python 3.9+ with typing

### フロントエンド
- **Core**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Layout**: CSS Grid/Flexbox
- **Real-time**: WebSocket API
- **Audio**: Web Audio API (通知音)
- **Testing**: Jest (オプション)

### 開発・テスト
- **Linting**: flake8, black
- **Type Checking**: mypy
- **Coverage**: pytest-cov
- **CI/CD**: GitHub Actions (推奨)

## 🏛️ アーキテクチャ詳細

### 1. 依存性注入設計

#### インターフェース定義
```python
# interfaces/timer_interface.py
from abc import ABC, abstractmethod
from datetime import datetime

class TimeProvider(ABC):
    @abstractmethod
    def now(self) -> datetime:
        """現在時刻を取得"""
        pass
    
    @abstractmethod
    def sleep(self, seconds: float) -> None:
        """指定時間待機"""
        pass

class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: str) -> None:
        """通知を送信"""
        pass

class WebSocketService(ABC):
    @abstractmethod
    def broadcast(self, event: str, data: dict) -> None:
        """WebSocket経由でブロードキャスト"""
        pass
```

#### DIコンテナ
```python
# dependency_injection/container.py
class DIContainer:
    def __init__(self, config: AppConfig):
        self._config = config
        self._services = {}
    
    def get_timer_controller(self) -> TimerController:
        return TimerController(
            time_provider=self.get_time_provider(),
            notification_service=self.get_notification_service(),
            websocket_service=self.get_websocket_service(),
            config=self._config
        )
```

### 2. タイマーモデル設計

```python
# models/timer_model.py
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

class TimerState(Enum):
    IDLE = "idle"
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"
    PAUSED = "paused"

@dataclass
class PomodoroSession:
    work_duration: int = 25         # 分
    short_break_duration: int = 5
    long_break_duration: int = 15
    sessions_until_long_break: int = 4
    current_session: int = 0
    state: TimerState = TimerState.IDLE
    remaining_time: int = 0         # 秒
    start_time: datetime = None
    
    def to_dict(self) -> dict:
        """辞書形式に変換（WebSocket送信用）"""
        return {
            'work_duration': self.work_duration,
            'short_break_duration': self.short_break_duration,
            'long_break_duration': self.long_break_duration,
            'current_session': self.current_session,
            'state': self.state.value,
            'remaining_time': self.remaining_time
        }
```

### 3. コントローラー設計

```python
# controllers/timer_controller.py
class TimerController:
    def __init__(self, 
                 time_provider: TimeProvider,
                 notification_service: NotificationService,
                 websocket_service: WebSocketService,
                 config: AppConfig):
        self._time_provider = time_provider
        self._notification_service = notification_service
        self._websocket_service = websocket_service
        self._config = config
        self._session = PomodoroSession()
    
    def start_timer(self) -> dict:
        """タイマー開始"""
        self._session.start_time = self._time_provider.now()
        self._session.state = TimerState.WORK
        self._session.remaining_time = self._session.work_duration * 60
        
        self._websocket_service.broadcast('timer_started', self._session.to_dict())
        return {'status': 'started', 'session': self._session.to_dict()}
    
    def pause_timer(self) -> dict:
        """タイマー一時停止"""
        if self._session.state != TimerState.IDLE:
            self._session.state = TimerState.PAUSED
            self._websocket_service.broadcast('timer_paused', self._session.to_dict())
        return {'status': 'paused', 'session': self._session.to_dict()}
    
    def reset_timer(self) -> dict:
        """タイマーリセット"""
        self._session = PomodoroSession()
        self._websocket_service.broadcast('timer_reset', self._session.to_dict())
        return {'status': 'reset', 'session': self._session.to_dict()}
```

## 🌐 API設計

### REST API エンドポイント

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/timer/status` | 現在のタイマー状態取得 | - | `PomodoroSession` |
| POST | `/api/timer/start` | タイマー開始 | - | `{'status': 'started', 'session': {...}}` |
| POST | `/api/timer/pause` | タイマー一時停止 | - | `{'status': 'paused', 'session': {...}}` |
| POST | `/api/timer/reset` | タイマーリセット | - | `{'status': 'reset', 'session': {...}}` |
| PUT | `/api/timer/settings` | 設定変更 | `{'work_duration': 25, ...}` | `{'status': 'updated', 'settings': {...}}` |
| GET | `/api/sessions/history` | セッション履歴取得 | - | `[{'date': '2025-01-01', ...}]` |

### WebSocket イベント

| Event | Direction | Data | Description |
|-------|-----------|------|-------------|
| `timer_started` | Server → Client | `PomodoroSession` | タイマー開始通知 |
| `timer_paused` | Server → Client | `PomodoroSession` | タイマー一時停止通知 |
| `timer_reset` | Server → Client | `PomodoroSession` | タイマーリセット通知 |
| `timer_update` | Server → Client | `{'remaining_time': 1500}` | リアルタイム時間更新 |
| `timer_complete` | Server → Client | `{'session_type': 'work'}` | タイマー完了通知 |
| `settings_update` | Server → Client | `AppConfig` | 設定変更通知 |

## 🧪 テスト戦略

### テストピラミッド

1. **ユニットテスト (70%)**
   - モデル、サービス、コントローラーの個別テスト
   - モック化された依存関係でのテスト
   - 高速実行（1秒未満）

2. **統合テスト (20%)**
   - API エンドポイントのテスト
   - WebSocket通信のテスト
   - データベース連携テスト

3. **E2Eテスト (10%)**
   - ユーザーフローのテスト
   - ブラウザ自動化テスト
   - パフォーマンステスト

### テスト用モック設計

```python
# tests/fixtures/mock_services.py
class MockTimeProvider(TimeProvider):
    def __init__(self, initial_time: datetime):
        self._current_time = initial_time
    
    def now(self) -> datetime:
        return self._current_time
    
    def advance_time(self, seconds: int):
        """テスト用：時間を進める"""
        self._current_time += timedelta(seconds=seconds)
    
    def sleep(self, seconds: float) -> None:
        pass  # テスト時は実際には待機しない

class MockWebSocketService(WebSocketService):
    def __init__(self):
        self.broadcast_calls = []
    
    def broadcast(self, event: str, data: dict) -> None:
        self.broadcast_calls.append({'event': event, 'data': data})
```

## 🎨 フロントエンド設計

### JavaScript クラス構造

```javascript
// static/js/pomodoro_timer.js
class PomodoroTimer {
    constructor(websocketUrl) {
        this.socket = new WebSocket(websocketUrl);
        this.state = {
            isRunning: false,
            remainingTime: 1500,
            currentSession: 0,
            timerState: 'idle'
        };
        
        this.initEventListeners();
        this.initWebSocket();
    }
    
    initEventListeners() {
        document.getElementById('start-btn').addEventListener('click', () => this.startTimer());
        document.getElementById('pause-btn').addEventListener('click', () => this.pauseTimer());
        document.getElementById('reset-btn').addEventListener('click', () => this.resetTimer());
    }
    
    initWebSocket() {
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.state.remainingTime / 60);
        const seconds = this.state.remainingTime % 60;
        document.getElementById('timer-display').textContent = 
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
}
```

### レスポンシブ対応

```css
/* static/css/responsive.css */
/* デスクトップ */
@media (min-width: 1024px) {
    .timer-container {
        display: grid;
        grid-template-columns: 300px 1fr;
        gap: 2rem;
    }
}

/* タブレット */
@media (max-width: 1023px) and (min-width: 768px) {
    .timer-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
}

/* モバイル */
@media (max-width: 767px) {
    .timer-container {
        padding: 1rem;
    }
    
    .timer-display {
        font-size: 3rem;
    }
}
```

## 📦 設定管理

### アプリケーション設定

```python
# config/settings.py
from dataclasses import dataclass

@dataclass
class AppConfig:
    # タイマー設定
    work_duration: int = 25
    short_break_duration: int = 5
    long_break_duration: int = 15
    sessions_until_long_break: int = 4
    
    # アプリケーション設定
    websocket_url: str = "ws://localhost:5000"
    notification_enabled: bool = True
    sound_enabled: bool = True
    
    # セキュリティ設定
    secret_key: str = "your-secret-key"
    cors_origins: list = None

@dataclass 
class TestConfig(AppConfig):
    # テスト用短縮時間
    work_duration: int = 1
    short_break_duration: int = 1
    long_break_duration: int = 1
    
    # テスト用設定
    notification_enabled: bool = False
    sound_enabled: bool = False
```

## 🚀 開発・デプロイメント

### 開発環境セットアップ

```bash
# 依存関係インストール
pip install -r requirements.txt
pip install -r requirements-test.txt

# 開発サーバー起動
python app.py

# テスト実行
make test-all

# カバレッジレポート
make test-coverage
```

### Makefile コマンド

```makefile
# テスト関連
test-unit:
	pytest tests/unit -m unit -v

test-integration:
	pytest tests/integration -m integration -v

test-e2e:
	pytest tests/e2e -m e2e -v

test-all:
	pytest tests/ -v

test-coverage:
	pytest --cov=app --cov-report=html --cov-report=term-missing

# 開発関連
run-dev:
	python app.py

format:
	black .
	
lint:
	flake8 .
	mypy .

# 本番環境
build:
	docker build -t pomodoro-timer .

deploy:
	docker-compose up -d
```

## 🔒 セキュリティ考慮事項

### 実装項目
- **CSRF対策**: Flask-WTF使用
- **入力値検証**: 全API エンドポイントでバリデーション
- **WebSocket認証**: 必要に応じてトークンベース認証
- **セッション管理**: Flask-Session使用
- **HTTPS対応**: 本番環境での必須設定

## 📈 パフォーマンス最適化

### 実装項目
- **WebSocket効率化**: 必要最小限のデータ送信
- **フロントエンド最適化**: DOM操作の最小化
- **キャッシュ戦略**: 静的ファイルのキャッシュ
- **リソース圧縮**: CSS/JavaScript minify

## 🔄 CI/CD パイプライン

### GitHub Actions ワークフロー例

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
    - name: Run tests
      run: make test-all
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 📝 今後の拡張予定

### Phase 2 機能
- ユーザー認証・管理
- セッション履歴のデータベース保存
- 統計ダッシュボード
- カスタムテーマ機能

### Phase 3 機能
- マルチユーザー対応
- チーム機能（共同作業セッション）
- モバイルアプリ（PWA対応）
- 外部サービス連携（Slack、Discord）

---

## 📚 参考文献・リソース

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Clean Architecture Principles](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Test-Driven Development Guidelines](https://martinfowler.com/articles/practical-test-pyramid.html)

---

**Document Version**: 1.0  
**Last Updated**: 2025-09-22  
**Author**: AI Assistant  
**Review Status**: Draft