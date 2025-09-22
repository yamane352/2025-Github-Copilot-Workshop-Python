from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TimerState(Enum):
    IDLE = "idle"
    WORK = "work"
    SHORT_BREAK = "short_break"
    PAUSED = "paused"


@dataclass
class PomodoroSession:
    work_duration: int = 25
    short_break_duration: int = 5
    current_session: int = 0
    state: TimerState = TimerState.IDLE
    remaining_time: int = 0
    start_time: datetime = None

    def to_dict(self):
        return {
            "work_duration": self.work_duration,
            "short_break_duration": self.short_break_duration,
            "current_session": self.current_session,
            "state": self.state.value,
            "remaining_time": self.remaining_time,
            "start_time": self.start_time.isoformat() if self.start_time else None,
        }
