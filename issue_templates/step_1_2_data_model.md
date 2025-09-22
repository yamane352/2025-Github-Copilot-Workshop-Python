# [Phase 1] Step 1.2: データモデル実装

## 📋 概要
ポモドーロタイマーのコアとなるデータモデル（TimerState、PomodoroSession）を実装します。

## 🎯 目標
- 完全にテストされたデータモデル
- JSON変換機能
- 状態管理とタイマーロジックの基盤

## ⏰ 所要時間
3-4時間

## 📋 実装項目

### 1. タイマー状態ENUM
```python
# models/timer_model.py
from enum import Enum

class TimerState(Enum):
    IDLE = "idle"
    WORK = "work"
    SHORT_BREAK = "short_break"
    PAUSED = "paused"
```

### 2. ポモドーロセッションクラス
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

### 3. 基本メソッド実装
- `start_work_session()`: 作業セッション開始
- `pause_session()`: セッション一時停止
- `reset_session()`: セッションリセット
- `to_dict()`: JSON変換用

## ✅ 受入基準
- [ ] TimerState ENUMが正しく定義されている
- [ ] PomodoroSessionクラスが適切なデフォルト値で初期化される
- [ ] `to_dict()` メソッドが正しくJSON形式のデータを返す
- [ ] 状態遷移メソッドが適切に動作する
- [ ] 全てのユニットテストがパスする
- [ ] テストカバレッジが90%以上

## 🧪 テスト項目
- [ ] 初期状態の確認
- [ ] 状態遷移テスト
- [ ] 時間計算テスト
- [ ] JSON変換テスト
- [ ] エラーケースのテスト

## 📝 実装ファイル
- `models/timer_model.py`
- `tests/test_timer_model.py`

## 🏷️ ラベル
- `phase-1`
- `mvp`
- `backend`
- `data-model`

## 📚 参考資料
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Python Enum](https://docs.python.org/3/library/enum.html)

## 📝 備考
この作業は既に完了していますが、機能拡張が必要な場合があります。