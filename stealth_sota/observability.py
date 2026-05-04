"""Prometheus Metriken – Echtzeit-Überwachung für die Stealth Suite."""
import time, functools

class _FakeCounter:
    def inc(self, *a, **kw): pass
    def labels(self, **kw): return self

class _FakeHistogram:
    def observe(self, *a, **kw): pass
    def labels(self, **kw): return self

class _FakeGauge:
    def set(self, *a, **kw): pass
    def labels(self, **kw): return self

try:
    from prometheus_client import Counter, Histogram, Gauge, start_http_server
    HAVE_PROMETHEUS = True
except ImportError:
    Counter = Histogram = Gauge = lambda *a, **kw: _FakeCounter()
    start_http_server = lambda *a, **kw: None
    HAVE_PROMETHEUS = False

SURVEYS_TOTAL = Counter("stealth_surveys_total", "Surveys total", ["provider", "status"])
COMMAND_LATENCY = Histogram("stealth_command_latency_ms", "Command latency", ["tool", "action"])
ERRORS_TOTAL = Counter("stealth_errors_total", "Errors total", ["type"])
DAEMON_UPTIME = Gauge("stealth_daemon_uptime_seconds", "Daemon uptime")

def observe_latency(tool: str, action: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                COMMAND_LATENCY.labels(tool=tool, action=action).observe((time.time()-start)*1000)
        return wrapper
    return decorator

def start_metrics(port=9090):
    start_http_server(port)
