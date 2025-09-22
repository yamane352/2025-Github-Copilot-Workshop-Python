# [Phase 3] Step 3.1: 設定管理実装

## 📋 概要
ユーザーがタイマーの時間設定や動作設定をカスタマイズできる機能を実装します。

## 🎯 目標
- カスタマイズ可能な時間設定
- 設定の永続化
- 直感的な設定UI

## ⏰ 所要時間
4-5時間

## 📋 実装項目

### 1. 設定データモデル
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

### 2. 設定UI
```html
<div class="settings-panel" id="settings-panel">
    <h3>設定</h3>
    <div class="setting-group">
        <label>作業時間 (分)</label>
        <input type="number" id="work-duration" min="1" max="60" value="25">
    </div>
    <div class="setting-group">
        <label>短い休憩時間 (分)</label>
        <input type="number" id="short-break-duration" min="1" max="30" value="5">
    </div>
    <div class="setting-group">
        <label>長い休憩時間 (分)</label>
        <input type="number" id="long-break-duration" min="1" max="60" value="15">
    </div>
    <div class="setting-group">
        <label>
            <input type="checkbox" id="notifications-enabled" checked>
            通知を有効にする
        </label>
    </div>
    <div class="setting-group">
        <label>
            <input type="checkbox" id="sound-enabled" checked>
            音響アラートを有効にする
        </label>
    </div>
</div>
```

### 3. ローカルストレージ
```javascript
class SettingsManager {
    saveSettings(settings) {
        localStorage.setItem('pomodoro-settings', JSON.stringify(settings));
    }
    
    loadSettings() {
        const saved = localStorage.getItem('pomodoro-settings');
        return saved ? JSON.parse(saved) : this.getDefaultSettings();
    }
    
    getDefaultSettings() {
        return {
            workDuration: 25,
            shortBreakDuration: 5,
            longBreakDuration: 15,
            sessionsUntilLongBreak: 4,
            notificationEnabled: true,
            soundEnabled: true,
            autoStart: false
        };
    }
}
```

### 4. 設定API
```python
@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(app_config.to_dict())

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    data = request.get_json()
    # 設定更新ロジック
    return jsonify({'status': 'updated'})
```

## ✅ 受入基準
- [ ] 設定パネルが正しく表示される
- [ ] 時間設定の変更が即座に反映される
- [ ] 設定がローカルストレージに保存される
- [ ] ブラウザを再起動しても設定が保持される
- [ ] 設定の妥当性チェックが動作する
- [ ] デフォルト設定へのリセット機能が動作する

## 🧪 テスト項目
- [ ] 設定保存/読み込みのテスト
- [ ] 設定変更時の即座反映テスト
- [ ] 入力値の妥当性チェックテスト
- [ ] デフォルト設定リセットテスト
- [ ] 異なるブラウザでの設定独立性テスト

## 📝 実装ファイル
- `models/config.py` (設定データモデル)
- `static/js/settings_manager.js`
- `static/css/settings.css`
- `templates/settings_panel.html`
- `tests/test_settings.py`

## 🏷️ ラベル
- `phase-3`
- `customization`
- `settings`
- `frontend`
- `backend`

## 📚 参考資料
- [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API)
- [HTML Form Validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation)

## 📝 備考
設定変更時にアクティブなタイマーに影響しないよう注意してください。