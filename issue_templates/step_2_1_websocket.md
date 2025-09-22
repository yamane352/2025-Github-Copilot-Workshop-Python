# [Phase 2] Step 2.1: WebSocket基盤実装

## 📋 概要
Flask-SocketIOを使用したリアルタイム通信機能を実装し、タイマーの時間更新をリアルタイムで配信します。

## 🎯 目標
- リアルタイム時間表示
- 複数クライアント同期
- WebSocket通信の安定性

## ⏰ 所要時間
4-5時間

## 📋 実装項目

### 1. Flask-SocketIO導入
```python
# app.py
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', session.to_dict())
```

### 2. リアルタイム時間更新
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

### 3. フロントエンドWebSocket
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

## ✅ 受入基準
- [ ] Flask-SocketIOが正しく設定されている
- [ ] WebSocket接続が正常に確立される
- [ ] リアルタイムでタイマー時間が更新される
- [ ] 複数ブラウザタブで状態が同期される
- [ ] 接続エラー時の適切なハンドリング
- [ ] メモリリークがない

## 🧪 テスト項目
- [ ] WebSocket接続テスト
- [ ] リアルタイム更新テスト
- [ ] 複数クライアント同期テスト
- [ ] 接続切断・再接続テスト
- [ ] エラーハンドリングテスト

## 📝 実装ファイル
- `app.py` (SocketIO設定)
- `static/js/websocket_client.js`
- `requirements.txt` (Flask-SocketIO追加)
- `tests/test_websocket.py`

## 🏷️ ラベル
- `phase-2`
- `realtime`
- `websocket`
- `backend`
- `frontend`

## 📚 参考資料
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Socket.IO Client Documentation](https://socket.io/docs/v4/client-api/)

## 📝 備考
この機能は複数ユーザーでの同期使用も考慮した設計にしてください。