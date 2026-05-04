"""DaemonSupervisor – Überwacht + startet den Daemon bei Bedarf neu."""
import subprocess, time, logging, psutil
from pathlib import Path
logger = logging.getLogger(__name__)

class DaemonSupervisor:
    def __init__(self, socket_path="/tmp/stealth-session.sock", pid_file="/tmp/stealth-session.pid"):
        self.socket_path = Path(socket_path)
        self.pid_file = Path(pid_file)
        self.max_restarts = 5
        self.restart_count = 0

    def is_alive(self) -> bool:
        if not self.socket_path.exists():
            return False
        if not self.pid_file.exists():
            return False
        try:
            pid = int(self.pid_file.read_text().strip())
            return psutil.pid_exists(pid)
        except (ValueError, OSError):
            return False

    def restart(self):
        if self.restart_count >= self.max_restarts:
            raise RuntimeError("Max restarts reached, giving up")
        self.restart_count += 1
        logger.warning("Daemon dead – restarting (%d/%d)", self.restart_count, self.max_restarts)
        self.socket_path.unlink(missing_ok=True)
        subprocess.Popen(["stealth-session", "start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(10):
            if self.socket_path.exists():
                self.restart_count = 0
                return
            time.sleep(1)
        logger.error("Daemon did not restart within 10s")

    def supervise(self):
        while True:
            if not self.is_alive():
                self.restart()
            time.sleep(5)
