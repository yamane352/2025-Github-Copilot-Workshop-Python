// app.js for Pomodoro Timer
class PomodoroTimer {
    constructor() {
        this.state = {
            isRunning: false,
            remainingTime: 1500, // 25分
            sessionCount: 1
        };
        this.initEventListeners();
    }
    initEventListeners() {
        document.getElementById('start-btn')
            .addEventListener('click', () => this.startTimer());
        // ... その他のイベントリスナー
    }
}
