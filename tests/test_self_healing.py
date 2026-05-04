import pytest
from stealth_sota.self_healing import DaemonSupervisor

class TestSelfHealing:
    def test_supervisor_detects_dead(self):
        sv = DaemonSupervisor(socket_path="/tmp/nonexistent.sock", pid_file="/tmp/nonexistent.pid")
        assert sv.is_alive() is False

    def test_supervisor_max_restarts(self):
        sv = DaemonSupervisor(socket_path="/tmp/nonexistent.sock", pid_file="/tmp/nonexistent.pid")
        sv.restart_count = 5
        with pytest.raises(RuntimeError, match="Max restarts"):
            sv.restart()
