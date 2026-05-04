import pytest
from stealth_sota.security_hardening import InputSanitizer, RateLimiter, AuditChain, SecurityError

class TestSecurity:
    def test_sanitizer_blocks_script(self):
        with pytest.raises(SecurityError):
            InputSanitizer.sanitize("<script>alert(1)</script>")

    def test_sanitizer_blocks_path_traversal(self):
        with pytest.raises(SecurityError):
            InputSanitizer.sanitize("../../../etc/passwd")

    def test_sanitizer_blocks_eval(self):
        with pytest.raises(SecurityError):
            InputSanitizer.sanitize("eval(malicious)")

    def test_sanitizer_allows_normal(self):
        assert InputSanitizer.sanitize("normal text") == "normal text"

    def test_sanitizer_blocks_too_long(self):
        with pytest.raises(ValueError):
            InputSanitizer.sanitize("x" * 6000)

    def test_rate_limiter_allows(self):
        limiter = RateLimiter(max_per_second=5)
        for _ in range(5):
            assert limiter.allow() is True
        assert limiter.allow() is False

    def test_audit_chain_verifies(self, tmp_path):
        chain = AuditChain(str(tmp_path / "audit.json"))
        h1 = chain.add_entry("login", {"user": "test"})
        h2 = chain.add_entry("click", {"element": "button"})
        assert chain.verify() is True
        assert h1 != h2

    def test_audit_chain_detects_tamper(self, tmp_path):
        chain = AuditChain(str(tmp_path / "audit.json"))
        chain.add_entry("login", {"user": "test"})
        chain.chain[0]["event"] = "hacked"
        assert chain.verify() is False
