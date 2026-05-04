# stealth-sota 🔬

> **SOTA-Erweiterungen** für die Stealth Suite.  
> Chaos Engineering, Security Hardening, Self-Healing, Observability, Determinismus.

## Module

| Modul | Klasse | Zweck |
|-------|--------|-------|
| `chaos_engine.py` | `ChaosMonkey` | 5 Chaos-Angriffe (kill Chrome, corrupt Cache, High CPU) |
| `security_hardening.py` | `InputSanitizer`, `RateLimiter`, `AuditChain` | Defense in Depth |
| `self_healing.py` | `DaemonSupervisor` | Auto-Neustart bei Crash (max 5 Versuche) |
| `observability.py` | Metriken (Prometheus) | Command-Latenz, Survey-Counts, Error-Rate |
| `determinism.py` | `Seeder` | Reproduzierbare Seeds aus Survey-IDs |

## Quick Start

```bash
pip install -e .[all]

pytest tests/ -v
```

## Lizenz

MIT – Teil der [SIN-CLIs Stealth Suite](https://github.com/SIN-CLIs).
