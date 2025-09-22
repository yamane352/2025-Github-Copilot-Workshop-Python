# ポモドーロタイマーアプリケーション 段階的実装計画

## 📋 概要

本文書は、Flask + HTML/CSS/JavaScript を使用したポモドーロタイマーWebアプリケーションの段階的実装計画を定義しています。アーキテクチャ設計書と機能一覧に基づき、実装の粒度と順序を具体的に設計し、各段階で動作確認可能な実装戦略を提案します。

---

## 🎯 **実装戦略**

### **基本方針**
1. **MVP First**: 最小限動作バージョンを最初に完成
2. **Incremental Development**: 各段階で動作確認可能
3. **Test-Driven**: 各機能に対応するテストを同時実装
4. **User-Centric**: ユーザー体験を重視した機能追加順序

### **技術的アプローチ**
- **Bottom-Up**: データモデルから開始
- **Outside-In**: UI → API → ビジネスロジックの順
- **Continuous Integration**: 各段階でテスト実行
- **Refactoring**: Phase間でのコード整理

---

## 🚀 **Phase 1: MVP (Minimum Viable Product)**
**期間**: 2-3日 | **目標**: 基本的なポモドーロタイマーの動作

### **Step 1.1: プロジェクト基盤構築**
**所要時間**: 2-3時間

#### **実装項目**
1. **プロジェクト構造作成**
   ```
   pomodoro_app/
   ├── app.py
   ├── models/
   │   ├── __init__.py
   │   └── timer_model.py
   ├── static/
   │   ├── css/
   │   │   └── main.css
   │   └── js/
   │       └── app.js
   ├── templates/
   │   └── index.html
   ├── tests/
   │   ├── __init__.py
   │   └── test_timer_model.py
   └── requirements.txt
   ```

2. **依存関係セットアップ**
   ```txt
   Flask==2.3.3
   pytest==7.4.0
   ```

3. **基本設定ファイル**
   - `app.py`: Flask アプリケーション初期化
   - `requirements.txt`: 依存パッケージ定義

#### **成果物**
- 動作するFlaskアプリケーション（Hello World）
- テスト実行環境

#### **確認方法**
```bash
python app.py  # サーバー起動確認
pytest         # テスト実行確認
```

### **Step 1.2: データモデル実装**
**所要時間**: 3-4時間

#### **実装項目**
1. **タイマー状態ENUM**
   ```python
   # models/timer_model.py
   from enum import Enum
   
   class TimerState(Enum):
       IDLE = "idle"
       WORK = "work"
       SHORT_BREAK = "short_break"
       PAUSED = "paused"
   ```

2. **ポモドーロセッション**
   ```python
   @dataclass
   class PomodoroSession:
       work_duration: int = 25
       short_break_duration: int = 5
       current_session: int = 0
       state: TimerState = TimerState.IDLE
       remaining_time: int = 0
       start_time: datetime = None
   ```

3. **基本メソッド**
   - `start_work_session()`
   - `pause_session()`
   - `reset_session()`
   - `to_dict()` - JSON変換用

#### **テスト項目**
- 初期状態の確認
- 状態遷移テスト
- 時間計算テスト

#### **成果物**
- 完全にテストされたデータモデル
- ドキュメント化されたAPI

### **Step 1.3: 基本UI実装**
**所要時間**: 4-5時間

#### **実装項目**
1. **HTML構造**
   ```html
   <!-- templates/index.html -->
   <div class="timer-container">
       <div class="timer-display">25:00</div>
       <div class="controls">
           <button id="start-btn">開始</button>
           <button id="pause-btn">一時停止</button>
           <button id="reset-btn">リセット</button>
       </div>
       <div class="session-info">
           <span>セッション: 1/4</span>
           <span class="status">作業時間</span>
       </div>
   </div>
   ```

2. **CSS スタイリング**
   ```css
   /* static/css/main.css */
   .timer-container {
       text-align: center;
       max-width: 400px;
       margin: 50px auto;
   }
   
   .timer-display {
       font-size: 4rem;
       font-family: 'Courier New', monospace;
       margin: 2rem 0;
   }
   
   .controls button {
       padding: 1rem 2rem;
       margin: 0 0.5rem;
       font-size: 1.2rem;
   }
   ```

3. **JavaScript基本機能**
   ```javascript
   // static/js/app.js
   class PomodoroTimer {
       constructor() {
           this.state = {
               isRunning: false,
               remainingTime: 1500, // 25分
               sessionCount: 1
           };
           this.initEventListeners();
       }
       
       initEventListeners() {
           document.getElementById('start-btn')
               .addEventListener('click', () => this.startTimer());
           // ... その他のイベントリスナー
       }
   }
   ```

#### **成果物**
- 機能的なUIコンポーネント
- レスポンシブデザイン
- ブラウザ互換性

### **Step 1.4: 基本API実装**
**所要時間**: 3-4時間

#### **実装項目**
1. **REST API エンドポイント**
   ```python
   # app.py
   @app.route('/api/timer/status', methods=['GET'])
   def get_timer_status():
       return jsonify(session.to_dict())
   
   @app.route('/api/timer/start', methods=['POST'])
   def start_timer():
       # タイマー開始ロジック
       return jsonify({'status': 'started'})
   
   @app.route('/api/timer/pause', methods=['POST'])
   def pause_timer():
       # タイマー一時停止ロジック
       return jsonify({'status': 'paused'})
   
   @app.route('/api/timer/reset', methods=['POST'])
   def reset_timer():
       # タイマーリセットロジック
       return jsonify({'status': 'reset'})
   ```

2. **フロントエンド連携**
   ```javascript
   async function startTimer() {
       const response = await fetch('/api/timer/start', {
           method: 'POST'
       });
       const result = await response.json();
       this.updateUI(result);
   }
   ```

#### **テスト項目**
- API レスポンス確認
- エラーハンドリング
- 状態管理整合性

#### **成果物**
- 動作するREST API
- フロントエンドとの連携

### **Phase 1 完了基準**
- ✅ 25分タイマーの開始/停止/リセット
- ✅ 基本的なUI表示
- ✅ API経由での状態管理
- ✅ 単体テスト済み

---

## 🔄 **Phase 2: リアルタイム機能**
**期間**: 3-4日 | **目標**: WebSocketとポモドーロロジック完成

### **Step 2.1: WebSocket基盤実装**
**所要時間**: 4-5時間

#### **実装項目**
1. **Flask-SocketIO導入**
   ```python
   # app.py
   from flask_socketio import SocketIO, emit
   
   socketio = SocketIO(app, cors_allowed_origins="*")
   
   @socketio.on('connect')
   def handle_connect():
       print('Client connected')
       emit('status', session.to_dict())
   ```

2. **リアルタイム時間更新**
   ```python
   import threading
   import time
   
   def timer_thread():
       while True:
           if session.state == TimerState.WORK:
               session.remaining_time -= 1
               socketio.emit('timer_update', {
                   'remaining_time': session.remaining_time
               })
           time.sleep(1)
   ```

3. **フロントエンドWebSocket**
   ```javascript
   // static/js/websocket_client.js
   class WebSocketClient {
       constructor() {
           this.socket = io();
           this.initEventListeners();
       }
       
       initEventListeners() {
           this.socket.on('timer_update', (data) => {
               this.updateTimerDisplay(data.remaining_time);
           });
       }
   }
   ```

#### **成果物**
- リアルタイム時間表示
- 複数クライアント同期

### **Step 2.2: ポモドーロロジック完成**
**所要時間**: 5-6時間

#### **実装項目**
1. **自動状態遷移**
   ```python
   def handle_timer_complete():
       if session.state == TimerState.WORK:
           session.current_session += 1
           if session.current_session % 4 == 0:
               session.state = TimerState.LONG_BREAK
               session.remaining_time = session.long_break_duration * 60
           else:
               session.state = TimerState.SHORT_BREAK
               session.remaining_time = session.short_break_duration * 60
   ```

2. **セッションカウンター**
   - 作業セッション追跡
   - 休憩種別の自動判定
   - プログレス表示

3. **長い休憩実装**
   ```python
   @dataclass
   class PomodoroSession:
       # 既存フィールド +
       long_break_duration: int = 15
       sessions_until_long_break: int = 4
   ```

#### **成果物**
- 完全なポモドーロサイクル
- 自動状態遷移
- セッション進捗表示

### **Step 2.3: 通知機能実装**
**所要時間**: 3-4時間

#### **実装項目**
1. **ブラウザ通知**
   ```javascript
   class NotificationService {
       async requestPermission() {
           if ('Notification' in window) {
               await Notification.requestPermission();
           }
       }
       
       showNotification(title, message) {
           if (Notification.permission === 'granted') {
               new Notification(title, {
                   body: message,
                   icon: '/static/images/pomodoro-icon.png'
               });
           }
       }
   }
   ```

2. **音響アラート**
   ```javascript
   class AudioService {
       constructor() {
           this.audioContext = new AudioContext();
       }
       
       playNotificationSound() {
           // Web Audio API使用
           const oscillator = this.audioContext.createOscillator();
           oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
           oscillator.connect(this.audioContext.destination);
           oscillator.start();
           oscillator.stop(this.audioContext.currentTime + 0.5);
       }
   }
   ```

#### **成果物**
- セッション完了通知
- カスタマイズ可能なアラート

### **Phase 2 完了基準**
- ✅ リアルタイムタイマー表示
- ✅ 完全なポモドーロサイクル
- ✅ 通知機能（ブラウザ + 音響）
- ✅ WebSocket通信

---

## ⚙️ **Phase 3: カスタマイズ機能**
**期間**: 2-3日 | **目標**: ユーザー設定とカスタマイズ

### **Step 3.1: 設定管理実装**
**所要時間**: 4-5時間

#### **実装項目**
1. **設定データモデル**
   ```python
   @dataclass
   class AppConfig:
       work_duration: int = 25
       short_break_duration: int = 5
       long_break_duration: int = 15
       sessions_until_long_break: int = 4
       notification_enabled: bool = True
       sound_enabled: bool = True
       auto_start: bool = False
   ```

2. **設定UI**
   ```html
   <div class="settings-panel" id="settings-panel">
       <h3>設定</h3>
       <div class="setting-group">
           <label>作業時間 (分)</label>
           <input type="number" id="work-duration" min="1" max="60" value="25">
       </div>
       <!-- その他設定項目 -->
   </div>
   ```

3. **ローカルストレージ**
   ```javascript
   class SettingsManager {
       saveSettings(settings) {
           localStorage.setItem('pomodoro-settings', JSON.stringify(settings));
       }
       
       loadSettings() {
           const saved = localStorage.getItem('pomodoro-settings');
           return saved ? JSON.parse(saved) : this.getDefaultSettings();
       }
   }
   ```

#### **成果物**
- カスタマイズ可能な時間設定
- 設定の永続化

### **Step 3.2: 視覚的改善**
**所要時間**: 4-5時間

#### **実装項目**
1. **状態別テーマ**
   ```css
   .timer-container.work-mode {
       background: linear-gradient(135deg, #ff6b6b, #ffa500);
   }
   
   .timer-container.break-mode {
       background: linear-gradient(135deg, #4ecdc4, #44a08d);
   }
   ```

2. **プログレスバー**
   ```html
   <div class="progress-container">
       <div class="progress-bar" id="session-progress"></div>
       <div class="progress-text">セッション 2/4</div>
   </div>
   ```

3. **アニメーション**
   ```css
   .timer-display {
       transition: all 0.3s ease;
   }
   
   .timer-display.pulse {
       animation: pulse 1s infinite;
   }
   
   @keyframes pulse {
       0% { transform: scale(1); }
       50% { transform: scale(1.05); }
       100% { transform: scale(1); }
   }
   ```

#### **成果物**
- 視覚的フィードバック
- ユーザビリティ向上

### **Phase 3 完了基準**
- ✅ カスタマイズ可能な設定
- ✅ 設定の永続化
- ✅ 視覚的改善
- ✅ アニメーション効果

---

## 📊 **Phase 4: データ分析機能**
**期間**: 3-4日 | **目標**: 履歴管理と統計

### **Step 4.1: データ永続化**
**所要時間**: 5-6時間

#### **実装項目**
1. **SQLite データベース**
   ```python
   # models/database.py
   import sqlite3
   from datetime import datetime
   
   class SessionHistory:
       def __init__(self, db_path="pomodoro.db"):
           self.db_path = db_path
           self.init_database()
       
       def save_session(self, session_type, duration, completed_at):
           # セッション記録保存
           pass
   ```

2. **履歴API**
   ```python
   @app.route('/api/sessions/history', methods=['GET'])
   def get_session_history():
       start_date = request.args.get('start_date')
       end_date = request.args.get('end_date')
       # 履歴取得ロジック
       return jsonify(sessions)
   ```

#### **成果物**
- セッション履歴の永続化
- 履歴取得API

### **Step 4.2: 統計ダッシュボード**
**所要時間**: 6-7時間

#### **実装項目**
1. **統計計算**
   ```python
   class StatisticsService:
       def get_daily_stats(self, date):
           # 日別統計
           return {
               'completed_sessions': 6,
               'total_focus_time': 150,
               'completion_rate': 85
           }
       
       def get_weekly_stats(self, week_start):
           # 週別統計
           pass
   ```

2. **可視化UI**
   ```html
   <div class="stats-dashboard">
       <div class="stat-card">
           <h3>今日</h3>
           <div class="stat-value">6</div>
           <div class="stat-label">完了セッション</div>
       </div>
       <div class="chart-container">
           <canvas id="weekly-chart"></canvas>
       </div>
   </div>
   ```

#### **成果物**
- 統計ダッシュボード
- データ可視化

### **Phase 4 完了基準**
- ✅ セッション履歴保存
- ✅ 統計データ表示
- ✅ データエクスポート機能

---

## 🧪 **Phase 5: テストとデプロイ**
**期間**: 2-3日 | **目標**: 品質保証と本番対応

### **Step 5.1: テスト完備**
**所要時間**: 6-8時間

#### **実装項目**
1. **ユニットテスト**
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
   ```

2. **統合テスト**
   ```python
   # tests/integration/test_api_endpoints.py
   def test_start_timer_endpoint(client):
       response = client.post('/api/timer/start')
       assert response.status_code == 200
       assert response.json['status'] == 'started'
   ```

3. **E2Eテスト**
   ```python
   # tests/e2e/test_user_flows.py
   def test_complete_pomodoro_cycle(browser):
       browser.get('http://localhost:5000')
       start_button = browser.find_element_by_id('start-btn')
       start_button.click()
       # タイマー動作確認
   ```

#### **成果物**
- 80%以上のテストカバレッジ
- CI/CD パイプライン

### **Step 5.2: 本番対応**
**所要時間**: 4-5時間

#### **実装項目**
1. **Docker化**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```

2. **環境設定分離**
   ```python
   # config/production.py
   class ProductionConfig:
       SECRET_KEY = os.environ.get('SECRET_KEY')
       DATABASE_URL = os.environ.get('DATABASE_URL')
   ```

#### **成果物**
- 本番環境対応
- Docker化
- 環境設定管理

---

## 📅 **実装スケジュール**

### **全体タイムライン（10-14日）**

| Phase | 期間 | 主要成果物 | 確認方法 |
|-------|------|------------|----------|
| **Phase 1** | 2-3日 | 基本タイマー機能 | ブラウザでタイマー動作確認 |
| **Phase 2** | 3-4日 | リアルタイム機能 | WebSocket通信確認 |
| **Phase 3** | 2-3日 | カスタマイズ機能 | 設定変更・保存確認 |
| **Phase 4** | 3-4日 | データ分析機能 | 履歴・統計表示確認 |
| **Phase 5** | 2-3日 | テスト・デプロイ | 全機能統合テスト |

### **日別詳細計画**

#### **Week 1**
- **Day 1**: プロジェクト基盤 + データモデル
- **Day 2**: 基本UI + API実装
- **Day 3**: MVP統合テスト + WebSocket基盤
- **Day 4**: リアルタイム機能 + ポモドーロロジック
- **Day 5**: 通知機能 + Phase 2テスト

#### **Week 2**
- **Day 6**: 設定管理 + 視覚的改善
- **Day 7**: カスタマイズ機能完成
- **Day 8**: データ永続化 + 履歴API
- **Day 9**: 統計ダッシュボード
- **Day 10**: 総合テスト + デプロイ準備

---

## 🎯 **成功基準と検証方法**

### **各Phase完了時の検証**

#### **Phase 1 検証**
- [ ] タイマーが25分正確に動作する
- [ ] 開始/停止/リセットボタンが機能する
- [ ] API が正しいレスポンスを返す
- [ ] 基本UIが表示される

#### **Phase 2 検証**
- [ ] リアルタイムで時間が更新される
- [ ] ポモドーロサイクルが自動で進行する
- [ ] 通知が適切なタイミングで表示される
- [ ] 複数ブラウザで状態が同期される

#### **Phase 3 検証**
- [ ] 設定変更が即座に反映される
- [ ] 設定がブラウザを再起動しても保持される
- [ ] 視覚的フィードバックが機能する
- [ ] レスポンシブデザインが動作する

#### **Phase 4 検証**
- [ ] セッション履歴が正確に記録される
- [ ] 統計データが正しく計算される
- [ ] データエクスポートが機能する
- [ ] パフォーマンスが許容範囲内

#### **Phase 5 検証**
- [ ] 全機能が統合して動作する
- [ ] テストカバレッジが80%以上
- [ ] 本番環境でデプロイ可能
- [ ] セキュリティ要件を満たす

---

## 🔧 **開発環境・ツール**

### **必要なツール**
- **エディタ**: VS Code + Python拡張
- **ブラウザ**: Chrome（開発者ツール使用）
- **ターミナル**: PowerShell または WSL
- **バージョン管理**: Git

### **開発コマンド**
```bash
# 開発サーバー起動
python app.py

# テスト実行
pytest

# カバレッジ確認
pytest --cov=app --cov-report=html

# リンティング
flake8 .

# フォーマッティング
black .
```

### **デバッグ戦略**
1. **ログ出力**: 各フェーズで適切なログ
2. **ブラウザ開発者ツール**: フロントエンドデバッグ
3. **単体テスト**: 問題の早期発見
4. **統合テスト**: システム全体の動作確認

---

## 📚 **学習リソース**

### **技術習得順序**
1. **Flask基礎**: ルーティング、テンプレート
2. **JavaScript ES6+**: クラス、async/await
3. **WebSocket**: リアルタイム通信
4. **CSS Grid/Flexbox**: レスポンシブデザイン
5. **pytest**: テスト駆動開発

### **参考資料**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Tutorial](https://flask-socketio.readthedocs.io/)
- [MDN Web APIs](https://developer.mozilla.org/en-US/docs/Web/API)
- [pytest Documentation](https://docs.pytest.org/)

---

## 🚨 **リスク管理**

### **技術的リスク**
1. **WebSocket接続問題**: フォールバック機能の実装
2. **ブラウザ互換性**: ポリフィル追加
3. **パフォーマンス**: 最適化戦略
4. **データ損失**: バックアップ機能

### **スケジュールリスク**
1. **学習コスト**: 技術習得時間の確保
2. **統合問題**: Phase間の調整時間
3. **テスト不足**: 品質確保時間の確保

### **対策**
- 各Phase終了時の動作確認
- 定期的なコードレビュー
- 継続的なリファクタリング
- ドキュメント整備

---

**Document Version**: 1.0  
**Last Updated**: 2025-09-22  
**Author**: GitHub Copilot  
**Status**: Ready for Implementation