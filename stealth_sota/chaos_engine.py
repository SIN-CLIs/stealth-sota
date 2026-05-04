"""ChaosMonkey – Zerstört aktiv Komponenten, um Resilienz zu beweisen."""
import psutil, time, logging, random, subprocess
from threading import Thread
logger = logging.getLogger(__name__)

class ChaosMonkey:
    def __init__(self, daemon_pid: int = None, target_pids: list = None):
        self.daemon_pid = daemon_pid
        self.target_pids = target_pids or []
        self.attack_log = []
        self.attacks = [
            "kill_chrome", "kill_daemon", "fill_disk_5mb",
            "corrupt_cache", "high_cpu_10s",
        ]

    def unleash_random(self, duration_seconds: int = 30):
        deadline = time.time() + duration_seconds
        while time.time() < deadline:
            attack = random.choice(self.attacks)
            try:
                getattr(self, attack)()
                self.attack_log.append({"attack": attack, "time": time.time()})
                logger.warning("CHAOS: %s executed", attack)
            except Exception as e:
                logger.error("Chaos %s failed: %s", attack, e)
            time.sleep(random.uniform(2, 5))

    def kill_chrome(self):
        for p in psutil.process_iter(["name"]):
            if "Google Chrome" in p.name():
                p.kill(); break

    def kill_daemon(self):
        if self.daemon_pid and psutil.pid_exists(self.daemon_pid):
            psutil.Process(self.daemon_pid).kill()
        for pid in self.target_pids:
            if psutil.pid_exists(pid):
                psutil.Process(pid).kill()

    def fill_disk_5mb(self):
        with open("/tmp/chaos_fill.tmp", "wb") as f:
            f.write(b"0" * 5_000_000)

    def corrupt_cache(self):
        try:
            with open("/tmp/stealth-session-cache.json", "w") as f:
                f.write("CORRUPTED{{{")
        except: pass

    def high_cpu_10s(self):
        def _burn():
            deadline = time.time() + 10
            while time.time() < deadline:
                _ = sum(i * i for i in range(10000))
        Thread(target=_burn).start()
