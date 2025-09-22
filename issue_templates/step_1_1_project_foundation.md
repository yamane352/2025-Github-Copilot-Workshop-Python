# [Phase 1] Step 1.1: プロジェクト基盤構築

## 📋 概要
ポモドーロタイマーアプリケーションの基本的なプロジェクト構造とFlaskアプリケーションの初期化を行います。

## 🎯 目標
- 動作するFlaskアプリケーション（Hello World）の構築
- テスト実行環境の整備
- 基本的なプロジェクト構造の作成

## ⏰ 所要時間
2-3時間

## 📋 実装項目

### 1. プロジェクト構造作成
以下のディレクトリ構造を作成：
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

### 2. 依存関係セットアップ
`requirements.txt` に以下を追加：
```txt
Flask==2.3.3
pytest==7.4.0
```

### 3. 基本設定ファイル
- `app.py`: Flask アプリケーション初期化
- 基本的なルート設定（Hello World）

## ✅ 受入基準
- [ ] プロジェクト構造が正しく作成されている
- [ ] `python app.py` でサーバーが起動する
- [ ] `pytest` でテストが実行される（テストファイルが存在する）
- [ ] ブラウザで http://localhost:5000 にアクセスして "Hello, Pomodoro!" が表示される

## 🧪 確認方法
```bash
python app.py  # サーバー起動確認
pytest         # テスト実行確認
```

## 📚 参考資料
- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

## 🏷️ ラベル
- `phase-1`
- `mvp`
- `setup`
- `infrastructure`

## 📝 備考
この作業は既に完了していますが、Issueとして記録しています。