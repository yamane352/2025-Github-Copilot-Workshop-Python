import unittest
from datetime import datetime

from pomodoro_app.models.timer_model import PomodoroSession, TimerState


class TestPomodoroSession(unittest.TestCase):
    def test_initial_state(self):
        session = PomodoroSession()
        self.assertEqual(session.state, TimerState.IDLE)
        self.assertEqual(session.work_duration, 25)
        self.assertEqual(session.short_break_duration, 5)
        self.assertEqual(session.current_session, 0)
        self.assertEqual(session.remaining_time, 0)
        self.assertIsNone(session.start_time)


if __name__ == "__main__":
    unittest.main()
