"""Input Sanitization, Rate Limiting, Audit Chain – Defense in Depth."""
import re, hashlib, time, json
from pathlib import Path

MAX_STRING_LENGTH = 5000
FORBIDDEN_PATTERNS = [
    r"<script[^>]*>", r"javascript\s*:", r"\.\.\/",
    r"\bexec\b", r"\beval\b", r"__proto__", r"constructor\s*\[",
]

class SecurityError(Exception):
    pass

class InputSanitizer:
    @classmethod
    def sanitize(cls, text: str) -> str:
        if len(text) > MAX_STRING_LENGTH:
            raise ValueError(f"Text too long: {len(text)} (max {MAX_STRING_LENGTH})")
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                raise SecurityError(f"Blocked pattern: {pat}")
        return text.strip()

class RateLimiter:
    def __init__(self, max_per_second: int = 20):
        self.max = max_per_second
        self.window = []

    def allow(self) -> bool:
        now = time.time()
        self.window = [t for t in self.window if now - t < 1.0]
        if len(self.window) >= self.max:
            return False
        self.window.append(now)
        return True

class AuditChain:
    def __init__(self, filepath: str = "/tmp/audit_chain.json"):
        self.path = Path(filepath)
        self.chain = []
        if self.path.exists():
            self.chain = json.loads(self.path.read_text())

    def add_entry(self, event: str, data: dict) -> str:
        last_hash = self.chain[-1]["hash"] if self.chain else "0"*64
        entry = {"timestamp": time.time(), "event": event, "data": data, "previous_hash": last_hash}
        entry["hash"] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        self.chain.append(entry)
        self.path.write_text(json.dumps(self.chain, indent=2))
        return entry["hash"]

    def verify(self) -> bool:
        for i, entry in enumerate(self.chain):
            expected_prev = self.chain[i-1]["hash"] if i > 0 else "0"*64
            if entry["previous_hash"] != expected_prev:
                return False
            recomputed = hashlib.sha256(
                json.dumps({k: entry[k] for k in entry if k != "hash"}, sort_keys=True).encode()
            ).hexdigest()
            if recomputed != entry["hash"]:
                return False
        return True
