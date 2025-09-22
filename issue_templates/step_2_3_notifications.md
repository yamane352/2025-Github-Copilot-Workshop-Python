# [Phase 2] Step 2.3: 通知機能実装

## 📋 概要
セッション完了時のブラウザ通知と音響アラートを実装します。

## 🎯 目標
- セッション完了通知
- カスタマイズ可能なアラート
- ユーザー体験の向上

## ⏰ 所要時間
3-4時間

## 📋 実装項目

### 1. ブラウザ通知
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

### 2. 音響アラート
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

### 3. 通知設定管理
```javascript
class NotificationManager {
    constructor() {
        this.settings = {
            browserNotifications: true,
            soundAlerts: true,
            volume: 0.5
        };
    }
    
    handleSessionComplete(sessionType) {
        const messages = {
            'work': '作業時間が終了しました！休憩しましょう。',
            'short_break': '短い休憩が終了しました！次の作業を始めましょう。',
            'long_break': '長い休憩が終了しました！新しいサイクルを始めましょう。'
        };
        
        this.showNotification('ポモドーロタイマー', messages[sessionType]);
        this.playSound();
    }
}
```

## ✅ 受入基準
- [ ] ブラウザ通知の権限要求が正しく動作する
- [ ] セッション完了時に適切な通知が表示される
- [ ] 音響アラートが正常に再生される
- [ ] 通知の有効/無効を切り替えできる
- [ ] 音量調整が可能
- [ ] 異なるセッション種別で通知メッセージが変わる

## 🧪 テスト項目
- [ ] 通知権限要求のテスト
- [ ] ブラウザ通知表示のテスト
- [ ] 音響アラート再生のテスト
- [ ] 通知設定の保存/読み込みテスト
- [ ] 異なるブラウザでの互換性テスト

## 📝 実装ファイル
- `static/js/notification_service.js`
- `static/js/audio_service.js`
- `static/css/main.css` (通知関連スタイル)
- `static/images/` (通知アイコン)
- `tests/test_notifications.js`

## 🏷️ ラベル
- `phase-2`
- `notifications`
- `frontend`
- `ux`

## 📚 参考資料
- [Notifications API](https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

## 📝 備考
ブラウザによる通知ポリシーの違いに注意して実装してください。