# [Phase 4] Step 4.2: 統計ダッシュボード

## 📋 概要
セッション履歴を基にした統計データの表示とデータ可視化機能を実装します。

## 🎯 目標
- 統計ダッシュボード
- データ可視化
- 生産性指標の表示

## ⏰ 所要時間
6-7時間

## 📋 実装項目

### 1. 統計計算サービス
```python
class StatisticsService:
    def __init__(self, db: SessionHistory):
        self.db = db
    
    def get_daily_stats(self, date: str) -> Dict:
        """日別統計を取得"""
        sessions = self.db.get_sessions_by_date(date)
        
        work_sessions = [s for s in sessions if s['session_type'] == 'work']
        break_sessions = [s for s in sessions if 'break' in s['session_type']]
        
        return {
            'date': date,
            'completed_sessions': len(work_sessions),
            'total_focus_time': sum(s['duration'] for s in work_sessions),
            'total_break_time': sum(s['duration'] for s in break_sessions),
            'completion_rate': self.calculate_completion_rate(work_sessions),
            'average_session_length': self.calculate_average_length(work_sessions),
            'productivity_score': self.calculate_productivity_score(work_sessions)
        }
    
    def get_weekly_stats(self, week_start: str) -> Dict:
        """週別統計を取得"""
        # 週間データの集計
        pass
    
    def get_monthly_trend(self, month: str) -> List[Dict]:
        """月間トレンドを取得"""
        # 月間トレンドデータの計算
        pass
```

### 2. 統計API
```python
@app.route('/api/stats/daily/<date>', methods=['GET'])
def get_daily_stats(date):
    stats = stats_service.get_daily_stats(date)
    return jsonify(stats)

@app.route('/api/stats/weekly/<week_start>', methods=['GET'])
def get_weekly_stats(week_start):
    stats = stats_service.get_weekly_stats(week_start)
    return jsonify(stats)

@app.route('/api/stats/trend/<month>', methods=['GET'])
def get_monthly_trend(month):
    trend = stats_service.get_monthly_trend(month)
    return jsonify(trend)

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    sessions = session_db.get_sessions(start_date, end_date)
    csv_data = generate_csv(sessions)
    
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=pomodoro_sessions.csv'}
    )
```

### 3. ダッシュボードUI
```html
<div class="stats-dashboard">
    <div class="stats-header">
        <h2>統計ダッシュボード</h2>
        <div class="date-selector">
            <input type="date" id="stats-date" value="">
            <button id="today-btn">今日</button>
            <button id="week-btn">今週</button>
            <button id="month-btn">今月</button>
        </div>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h3>完了セッション</h3>
            <div class="stat-value" id="completed-sessions">0</div>
            <div class="stat-label">セッション</div>
        </div>
        
        <div class="stat-card">
            <h3>集中時間</h3>
            <div class="stat-value" id="focus-time">0</div>
            <div class="stat-label">分</div>
        </div>
        
        <div class="stat-card">
            <h3>完了率</h3>
            <div class="stat-value" id="completion-rate">0</div>
            <div class="stat-label">%</div>
        </div>
        
        <div class="stat-card">
            <h3>生産性スコア</h3>
            <div class="stat-value" id="productivity-score">0</div>
            <div class="stat-label">ポイント</div>
        </div>
    </div>
    
    <div class="charts-container">
        <div class="chart-section">
            <h3>週間トレンド</h3>
            <canvas id="weekly-chart" width="400" height="200"></canvas>
        </div>
        
        <div class="chart-section">
            <h3>セッション分布</h3>
            <canvas id="session-distribution-chart" width="400" height="200"></canvas>
        </div>
    </div>
</div>
```

### 4. データ可視化
```javascript
class ChartManager {
    constructor() {
        this.weeklyChart = null;
        this.distributionChart = null;
    }
    
    initCharts() {
        this.initWeeklyChart();
        this.initDistributionChart();
    }
    
    initWeeklyChart() {
        const ctx = document.getElementById('weekly-chart').getContext('2d');
        this.weeklyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: '完了セッション数',
                    data: [],
                    borderColor: '#ff6b6b',
                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
    
    updateWeeklyChart(data) {
        this.weeklyChart.data.labels = data.labels;
        this.weeklyChart.data.datasets[0].data = data.values;
        this.weeklyChart.update();
    }
}
```

### 5. データエクスポート
```javascript
class DataExporter {
    async exportCSV(startDate, endDate) {
        const response = await fetch(`/api/export/csv?start_date=${startDate}&end_date=${endDate}`);
        const blob = await response.blob();
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `pomodoro_sessions_${startDate}_to_${endDate}.csv`;
        a.click();
        window.URL.revokeObjectURL(url);
    }
}
```

## ✅ 受入基準
- [ ] 統計データが正確に計算される
- [ ] 日別・週別・月別の統計が表示される
- [ ] チャートが正しく描画される
- [ ] データエクスポート機能が動作する
- [ ] レスポンシブな統計表示
- [ ] パフォーマンスが良好（大量データでも高速）

## 🧪 テスト項目
- [ ] 統計計算の精度テスト
- [ ] チャート描画テスト
- [ ] データエクスポートテスト
- [ ] 大量データでのパフォーマンステスト
- [ ] 異なる期間での統計表示テスト

## 📝 実装ファイル
- `services/statistics_service.py`
- `static/js/chart_manager.js`
- `static/js/data_exporter.js`
- `static/css/dashboard.css`
- `templates/dashboard.html`
- `tests/test_statistics.py`

## 🏷️ ラベル
- `phase-4`
- `statistics`
- `dashboard`
- `visualization`
- `frontend`
- `backend`

## 📚 参考資料
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [CSV Export Best Practices](https://developer.mozilla.org/en-US/docs/Web/API/Blob)

## 📝 備考
チャートライブラリはChart.jsまたは軽量な代替ライブラリを使用してください。