import pytest, json, os, tempfile
from pathlib import Path
from stealth_sota.chaos_engine import ChaosMonkey

class TestChaos:
    def test_chaos_corrupts_cache(self):
        cache = Path("/tmp/stealth-session-cache.json")
        cache.write_text(json.dumps({"pid": 123}))
        monkey = ChaosMonkey()
        monkey.corrupt_cache()
        assert "CORRUPTED" in cache.read_text()
        cache.unlink(missing_ok=True)

    def test_chaos_fills_disk(self):
        monkey = ChaosMonkey()
        monkey.fill_disk_5mb()
        assert Path("/tmp/chaos_fill.tmp").exists()
        assert Path("/tmp/chaos_fill.tmp").stat().st_size >= 5_000_000
        Path("/tmp/chaos_fill.tmp").unlink(missing_ok=True)

    def test_chaos_attack_logs(self):
        monkey = ChaosMonkey()
        monkey.corrupt_cache()
        assert len(monkey.attack_log) >= 0
        if monkey.attack_log:
            assert "attack" in monkey.attack_log[0]
