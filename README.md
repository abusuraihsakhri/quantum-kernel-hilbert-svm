# Quantum Kernel Hilbert Svm

> **Domain:** Post-Quantum Cryptography & Quantum Machine Learning
> **Standards:** NIST FIPS 203/204/205, ISO/IEC 17825, Havlicek 2019 Quantum Kernel Protocol

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

Quantum Kernel Hilbert Svm is an enterprise-grade analytical platform that orchestrates multi-agent evaluation of task payloads through specialized worker agents. The system classifies operational parameters into risk tiers (ROUTINE, ELEVATED, CRITICAL) using deterministic threshold logic, and maintains a cryptographically tamper-evident HMAC-SHA256 audit trail for every evaluation.

The platform provides two parallel agent systems:
- **Primary System** (`agents/`): Multi-worker evaluation with PHI outbound guarding and Bayesian calibration
- **Quantum Kernel SVM System** (`quantum_kernel_svm/`): Havlicek-protocol-based quantum kernel evaluation with feature map agents

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.
- **PHI Outbound Guard**: AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
- **HMAC-SHA256 Audit Trail**: Chained, cryptographically signed logs for every evaluation and state transition.
- **FastAPI REST API**: OpenAPI 3.1 endpoints for programmatic access.
- **Prometheus Telemetry**: Operational metrics export (`/metrics`).

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/quantum-kernel-hilbert-svm.git
cd quantum-kernel-hilbert-svm

# Install dependencies
pip install -e ".[dev]"

# Or install runtime dependencies only
pip install fastapi uvicorn pydantic pytest
```

---

## 🚀 CLI Quickstart & Usage

### 1. Run Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch FastAPI REST Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
- `--task-id`: Unique task identifier (default: TASK-2026-001)
- `--target`: Target entity identifier (default: KEY-TARGET-01)
- `--primary`: Primary measurement value (float, default: 28.5)
- `--secondary`: Secondary measurement value (float, default: 14.2)
- `--critical`: Flag for emergency escalation (boolean)
- `--status`: Status descriptor (default: DISCORDANT)

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Unique task identifier | Required |
| `target_identifier` | Target entity identifier | Required |
| `primary_metric` | Primary measurement value | Required |
| `secondary_metric` | Secondary measurement value | Optional |
| `is_critical_flag` | Emergency escalation flag | Optional |
| `status_descriptor` | Status code descriptor | Optional |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Secure Key Management:** Audit signing keys sourced from environment variables (`AUDIT_SECRET_KEY`) or generated securely at runtime.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

Run with Docker:

```bash
docker build -t quantum-kernel-hilbert-svm .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key quantum-kernel-hilbert-svm
```

---

## 🐳 Container Deployment

```bash
docker-compose up -d
```

The service will be available at `http://localhost:8000`.

API Endpoints:
- `GET /health` - Health check
- `POST /api/audit` - Submit task evaluation
- `POST /api/chat` - Supervisory chat query
- `GET /api/audit/logs` - Retrieve audit trail
- `GET /metrics` - Prometheus metrics

---

## 📁 Project Structure

```
quantum-kernel-hilbert-svm/
├── agents/                      # Primary multi-agent evaluation system
│   ├── __init__.py
│   ├── api.py                   # FastAPI REST server
│   ├── base.py                  # Security, PHI guard, audit trail
│   ├── learning.py              # Bayesian calibration engine
│   ├── llm_factory.py           # LLM provider factory
│   ├── metrics.py               # Prometheus metrics collector
│   ├── models.py                # Pydantic data models
│   ├── streamer.py              # WebSocket telemetry streamer
│   ├── supervisor.py            # Master orchestrator
│   └── workers.py               # Specialized evaluation workers
├── quantum_kernel_svm/           # Quantum kernel SVM agent system
│   ├── __init__.py
│   ├── agents.py                # Quantum kernel agents
│   ├── cli.py                   # Quantum kernel CLI
│   ├── engine.py                # Core algorithmic engine
│   ├── models.py                # Data models
│   └── server.py                # FastAPI server factory
├── tests/                       # Test suite
│   ├── test_enrichment.py
│   ├── test_quantum_kernel_hilbert_svm.py
│   └── test_quantum_kernel_svm.py
├── web/
│   └── index.html               # Operations console UI
├── cli.py                       # Primary CLI entry point
├── simulator.py                 # High-throughput simulation
├── enrichment.py                # Enrichment feature suite
├── pyproject.toml               # Project configuration
├── Dockerfile                   # Container build
├── docker-compose.yml           # Container orchestration
└── sample.csv                   # Sample batch input data
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
