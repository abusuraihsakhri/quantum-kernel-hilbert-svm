# Quantum Kernel Hilbert SVM

A small **noiseless quantum-kernel simulator and SVM adapter**, with a separate legacy threshold-assessment service. The quantum component computes the fidelity kernel K(x, z) = |⟨φ(x)|φ(z)⟩|² using a data-dependent H/ZZ feature map and optionally trains an SVM via scikit-learn's precomputed-kernel interface.

The classical statevector simulator is **Havlíček-inspired**, not an implementation validated against any quantum-hardware protocol. It does not demonstrate quantum advantage. The threshold-assessment agents are deterministic rules, **not SVM predictions** and not implementations of NIST cryptographic standards.

## Features

- Statevector features for 1–6 qubits, 1–4 repetitions; symmetric, positive-semidefinite Gram matrices
- Optional scikit-learn SVM training, prediction and scoring using a precomputed fidelity kernel
- Browser workspace: calculate and export a kernel matrix, and evaluate an explicitly **unsigned** local preview of legacy threshold rules
- Legacy Python CLI, CSV batch assessment, FastAPI endpoints, in-memory HMAC-chained audit records, and configurable audit key
- Automated validation and mathematical-invariant tests

## Browser workspace

Open [`web/index.html`](web/index.html) in a browser to perform local, noiseless kernel calculations without installing Python or uploading data. Choose feature vectors (CSV without a header), repetitions, and **Compute Fidelity Matrix**. You can export the resulting matrix as CSV.

The browser's separate threshold assessment works locally unless **Use same-origin FastAPI backend** is selected. Browser-only results do not carry cryptographic signatures. No browser storage or remote processing is used by the local mode. The browser version is written in JavaScript; Python is **not** executed in the browser.

A GitHub Pages deployment workflow is included, but the live URL should not be considered active until GitHub Pages is enabled and deployment verified.

## Install and run

Requires Python 3.10–3.12 for the tested CI configurations; package metadata permits Python >=3.9.

```bash
python -m pip install -e ".[api,ml,dev]"
pytest -q
```

Compute a fidelity Gram matrix using the installed command (no optional scientific packages required for kernel evaluation):

```bash
quantum-kernel-hilbert-svm kernel-matrix --points '[[0.1,0.3],[0.2,2.1],[1.7,0.8]]' --reps 2
```

Use the SVM adapter in Python:

```python
from quantum_kernel_svm.kernel import QuantumKernelSVM, kernel_matrix

X = [[0.2, 0.2], [2.8, 2.8], [0.2, 2.8], [2.8, 0.2]]
y = [-1, -1, 1, 1]
model = QuantumKernelSVM(C=10).fit(X, y)
print(kernel_matrix(X))
print(model.predict(X))
```

The SVM adapter requires the optional `ml` extra. Keep training and test data separate when evaluating predictive performance; examples are not benchmarks.

## Legacy threshold evaluation

The original deterministic task assessments remain available. Their thresholds are arbitrary repository settings, not validated scientific or clinical limits.

```bash
python cli.py audit --task-id TASK-001 --target TARGET-01 --primary 28.5 --secondary 14.2 --status DISCORDANT
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
python cli.py serve --host 127.0.0.1 --port 8000
```

The API provides `GET /` (browser interface), `GET /health`, `POST /api/kernel`, `POST /api/audit`, `POST /api/chat`, `GET /api/audit/logs`, and `GET /metrics` (a JSON summary, **not** Prometheus exposition text).

Example kernel API request:

```bash
curl -s http://127.0.0.1:8000/api/kernel -H 'Content-Type: application/json' \
  -d '{"points":[[0.1,0.3],[0.2,2.1]],"reps":2}'
```

## Docker

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

The Compose port binds to `127.0.0.1:8000` by default. Set a strong audit key through the environment; never commit it. For production exposure, add authentication, TLS, persistence, operational limits, and an appropriate security review.

## Privacy and limitations

- Browser kernel computations and unsigned previews run locally; selecting the FastAPI backend transmits the task to that backend.
- Do **not** submit patient identifiers or protected health information. The server's regex guard is a best-effort filter, not a HIPAA de-identification system.
- Audit logs and registry state are held **in memory only**. HMAC verification detects changes to signed record fields but does not constitute persistent, independently anchored audit storage.
- The legacy mock chat returns template text; it does not call a generative model or conduct scientific verification.
- Current API routes have no authentication. Use localhost or a trusted, access-controlled deployment.
- The kernel uses an exact **classical** statevector simulation, not Pyodide, Qiskit or quantum hardware. Memory and computational work grow rapidly with qubit count.

## Technology

Python standard library (kernel and legacy agents), Pydantic, optional FastAPI/Uvicorn and scikit-learn; HTML, CSS, and vanilla JavaScript browser workspace; pytest and GitHub Actions. Tested CI Python versions: 3.10, 3.11, 3.12. Modern browsers supporting ES2020+ are recommended.

## License

[MIT](LICENSE).
