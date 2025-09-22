# [Phase 2] Step 2.2: ポモドーロロジック完成

## 📋 概要
完全なポモドーロテクニックのサイクル（作業→短い休憩→作業→...→長い休憩）を実装します。

## 🎯 目標
- 完全なポモドーロサイクル
- 自動状態遷移
- セッション進捗表示

## ⏰ 所要時間
5-6時間

## 📋 実装項目

### 1. 自動状態遷移
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

### 2. セッションカウンター
- 作業セッション追跡
- 休憩種別の自動判定
- プログレス表示

### 3. 長い休憩実装
```python
@dataclass
class PomodoroSession:
    # 既存フィールド +
    long_break_duration: int = 15
    sessions_until_long_break: int = 4
```

### 4. 状態管理の拡張
```python
class TimerState(Enum):
    IDLE = "idle"
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"
    PAUSED = "paused"
```

## ✅ 受入基準
- [ ] 25分作業→5分休憩のサイクルが正しく動作する
- [ ] 4セッション後に15分の長い休憩が始まる
- [ ] セッションカウンターが正しく更新される
- [ ] 状態遷移が自動で行われる
- [ ] 各状態でUI表示が適切に変更される
- [ ] 一時停止・再開が全ての状態で動作する

## 🧪 テスト項目
- [ ] 作業セッション完了後の短い休憩遷移テスト
- [ ] 4セッション後の長い休憩遷移テスト
- [ ] セッションカウンターの正確性テスト
- [ ] 状態遷移ロジックのテスト
- [ ] タイマー完了イベントのテスト

## 📝 実装ファイル
- `models/timer_model.py` (PomodoroSession拡張)
- `app.py` (タイマーロジック)
- `static/js/app.js` (フロントエンド状態管理)
- `tests/test_pomodoro_logic.py`

## 🏷️ ラベル
- `phase-2`
- `core-logic`
- `pomodoro`
- `backend`

## 📚 参考資料
- [Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique)
- [Python threading](https://docs.python.org/3/library/threading.html)

## 📝 備考
この機能はポモドーロタイマーの核となる部分です。正確な時間管理と状態遷移が重要です。