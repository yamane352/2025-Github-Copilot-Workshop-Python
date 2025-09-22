# [Phase 1] Step 1.4: 基本API実装

## 📋 概要
ポモドーロタイマーの基本的なREST APIエンドポイントを実装し、フロントエンドとの連携を構築します。

## 🎯 目標
- 動作するREST API
- フロントエンドとの連携
- 状態管理の実装

## ⏰ 所要時間
3-4時間

## 📋 実装項目

### 1. REST APIエンドポイント
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

### 2. フロントエンド連携
```javascript
async function startTimer() {
    const response = await fetch('/api/timer/start', {
        method: 'POST'
    });
    const result = await response.json();
    this.updateUI(result);
}
```

### 3. 状態管理実装
- セッション状態のメモリ管理
- タイマーロジックの実装
- エラーハンドリング

## ✅ 受入基準
- [ ] 全APIエンドポイントが正しく動作する
- [ ] APIレスポンスが正しいJSON形式で返される
- [ ] フロントエンドからAPIが正常に呼び出せる
- [ ] 状態管理が正しく動作する
- [ ] エラーハンドリングが適切に実装されている
- [ ] CORS設定が適切に行われている

## 🧪 テスト項目
- [ ] `/api/timer/status` GETリクエストのテスト
- [ ] `/api/timer/start` POSTリクエストのテスト
- [ ] `/api/timer/pause` POSTリクエストのテスト
- [ ] `/api/timer/reset` POSTリクエストのテスト
- [ ] エラーケースのテスト
- [ ] 状態管理整合性のテスト

## 📝 実装ファイル
- `app.py` (APIエンドポイント)
- `static/js/app.js` (フロントエンド連携)
- `tests/test_api.py` (APIテスト)

## 🏷️ ラベル
- `phase-1`
- `mvp`
- `backend`
- `api`

## 📚 参考資料
- [Flask Documentation - API](https://flask.palletsprojects.com/en/2.3.x/api/)
- [Flask Documentation - JSON](https://flask.palletsprojects.com/en/2.3.x/quickstart/#json)
- [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 📝 備考
この機能は基本的なタイマー動作の核となる部分です。