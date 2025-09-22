# [Phase 5] Step 5.2: 本番対応

## 📋 概要
本番環境でのデプロイメント準備として、Docker化、環境設定分離、セキュリティ対策を実装します。

## 🎯 目標
- 本番環境対応
- Docker化
- 環境設定管理
- セキュリティ強化

## ⏰ 所要時間
4-5時間

## 📋 実装項目

### 1. Docker化
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# 非rootユーザーの作成
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# ポート公開
EXPOSE 5000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# アプリケーション起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///data/pomodoro.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped
```

### 2. 環境設定分離
```python
# config/production.py
import os

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///pomodoro.db'
    
    # セキュリティ設定
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS設定
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    
    # ログ設定
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/pomodoro.log')

# config/development.py
class DevelopmentConfig:
    SECRET_KEY = 'dev-secret-key'
    DATABASE_URL = 'sqlite:///pomodoro_dev.db'
    DEBUG = True
    
# config/__init__.py
import os

def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        from .production import ProductionConfig
        return ProductionConfig
    else:
        from .development import DevelopmentConfig
        return DevelopmentConfig
```

### 3. セキュリティ強化
```python
# security/middleware.py
from flask import request, abort
import re

class SecurityMiddleware:
    def __init__(self, app):
        self.app = app
        self.setup_security_headers()
        self.setup_rate_limiting()
    
    def setup_security_headers(self):
        @self.app.after_request
        def add_security_headers(response):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            return response
    
    def setup_rate_limiting(self):
        # レート制限の実装
        pass

# security/validation.py
def validate_input(data, schema):
    """入力値の検証"""
    if not isinstance(data, dict):
        raise ValueError("Invalid data format")
    
    for field, rules in schema.items():
        if field in data:
            value = data[field]
            if 'type' in rules and not isinstance(value, rules['type']):
                raise ValueError(f"Invalid type for {field}")
            if 'min' in rules and value < rules['min']:
                raise ValueError(f"Value too small for {field}")
            if 'max' in rules and value > rules['max']:
                raise ValueError(f"Value too large for {field}")
```

### 4. ログ設定
```python
# logging_config.py
import logging
import logging.handlers
import os

def setup_logging(app):
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.handlers.RotatingFileHandler(
            'logs/pomodoro.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Pomodoro Timer startup')
```

### 5. 本番用requirements
```txt
# requirements-prod.txt
Flask==2.3.3
Flask-SocketIO==5.3.4
Flask-CORS==4.0.0
gunicorn==21.2.0
eventlet==0.33.3
python-dotenv==1.0.0
```

### 6. ヘルスチェックエンドポイント
```python
@app.route('/health')
def health_check():
    """ヘルスチェックエンドポイント"""
    try:
        # データベース接続確認
        db_status = check_database_connection()
        
        return jsonify({
            'status': 'healthy',
            'database': db_status,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503
```

### 7. Nginx設定
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream app {
        server web:5000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        
        location /socket.io/ {
            proxy_pass http://app;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

## ✅ 受入基準
- [ ] Dockerコンテナが正常に起動する
- [ ] 本番環境設定が適切に読み込まれる
- [ ] セキュリティヘッダーが設定されている
- [ ] ログが適切に出力される
- [ ] ヘルスチェックが動作する
- [ ] HTTPS通信が可能

## 🧪 テスト項目
- [ ] Docker buildの成功確認
- [ ] コンテナ起動テスト
- [ ] セキュリティヘッダーの確認
- [ ] ヘルスチェックエンドポイントのテスト
- [ ] 負荷テスト（基本的な）
- [ ] セキュリティスキャン

## 📝 実装ファイル
- `Dockerfile`
- `docker-compose.yml`
- `config/production.py`
- `security/middleware.py`
- `nginx.conf`
- `requirements-prod.txt`

## 🏷️ ラベル
- `phase-5`
- `production`
- `docker`
- `security`
- `deployment`

## 📚 参考資料
- [Docker Documentation](https://docs.docker.com/)
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Nginx Documentation](https://nginx.org/en/docs/)

## 📝 備考
SSL証明書の設定とバックアップ戦略も検討してください。