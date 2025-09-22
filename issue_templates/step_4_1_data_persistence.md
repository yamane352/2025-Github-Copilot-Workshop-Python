# [Phase 4] Step 4.1: データ永続化

## 📋 概要
セッション履歴をSQLiteデータベースに永続化し、履歴取得APIを実装します。

## 🎯 目標
- セッション履歴の永続化
- 履歴取得API
- データの整合性確保

## ⏰ 所要時間
5-6時間

## 📋 実装項目

### 1. SQLiteデータベース
```python
# models/database.py
import sqlite3
from datetime import datetime
from typing import List, Dict

class SessionHistory:
    def __init__(self, db_path="pomodoro.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """データベースとテーブルを初期化"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_type TEXT NOT NULL,
                    duration INTEGER NOT NULL,
                    planned_duration INTEGER NOT NULL,
                    completed_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def save_session(self, session_type: str, duration: int, planned_duration: int, completed_at: datetime):
        """セッションを保存"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO sessions (session_type, duration, planned_duration, completed_at)
                VALUES (?, ?, ?, ?)
            ''', (session_type, duration, planned_duration, completed_at))
```

### 2. 履歴API
```python
@app.route('/api/sessions/history', methods=['GET'])
def get_session_history():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', 50, type=int)
    
    history = session_db.get_sessions(start_date, end_date, limit)
    return jsonify({
        'sessions': history,
        'total': len(history)
    })

@app.route('/api/sessions/stats', methods=['GET'])
def get_session_stats():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    stats = session_db.get_daily_stats(date)
    return jsonify(stats)
```

### 3. セッション完了時の自動保存
```python
def on_session_complete(session: PomodoroSession):
    """セッション完了時の処理"""
    session_db.save_session(
        session_type=session.state.value,
        duration=session.elapsed_time,
        planned_duration=session.get_planned_duration(),
        completed_at=datetime.now()
    )
    
    # WebSocket通知
    socketio.emit('session_completed', {
        'session_type': session.state.value,
        'stats': session_db.get_daily_stats()
    })
```

### 4. データマイグレーション
```python
class DatabaseMigration:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def migrate(self):
        """データベーススキーマのマイグレーション"""
        version = self.get_schema_version()
        
        if version < 1:
            self.migrate_v1()
        if version < 2:
            self.migrate_v2()
    
    def migrate_v1(self):
        """初期スキーマ作成"""
        # 初期テーブル作成
        pass
```

## ✅ 受入基準
- [ ] SQLiteデータベースが正しく初期化される
- [ ] セッション完了時に履歴が自動保存される
- [ ] 履歴取得APIが正しいデータを返す
- [ ] 日付範囲での履歴フィルタリングが動作する
- [ ] データベースの接続エラーが適切にハンドリングされる
- [ ] データマイグレーションが正常に動作する

## 🧪 テスト項目
- [ ] データベース初期化テスト
- [ ] セッション保存テスト
- [ ] 履歴取得APIテスト
- [ ] 日付フィルタリングテスト
- [ ] データベース接続エラーハンドリングテスト
- [ ] 大量データでのパフォーマンステスト

## 📝 実装ファイル
- `models/database.py`
- `models/migration.py`
- `app.py` (API追加)
- `tests/test_database.py`
- `tests/test_migration.py`

## 🏷️ ラベル
- `phase-4`
- `database`
- `persistence`
- `backend`
- `api`

## 📚 参考資料
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)

## 📝 備考
データベースファイルのバックアップ機能も考慮してください。