"""Mathematical and integration tests for the exact statevector kernel."""
import math
import pytest
from quantum_kernel_svm.kernel import feature_state, fidelity_kernel, kernel_matrix, QuantumKernelSVM
from quantum_kernel_svm.cli import main as quantum_cli
from agents.base import AuditTrail


def test_statevector_normalization_and_fidelity():
    for reps in (1, 2, 4):
        for x in ([0.0], [0.1, 2.0], [0.2, 0.4, 0.7]):
            s = feature_state(x, reps)
            assert sum(abs(a) ** 2 for a in s) == pytest.approx(1.0, abs=1e-12)
            assert fidelity_kernel(x, x, reps) == pytest.approx(1.0, abs=1e-12)


def test_gram_is_symmetric_positive_semidefinite():
    np = pytest.importorskip("numpy")
    points = [[0.1, 0.3], [0.2, 2.1], [1.7, 0.8], [2.4, 2.8]]
    K = np.array(kernel_matrix(points))
    assert np.allclose(K, K.T)
    assert np.allclose(np.diag(K), 1)
    assert np.linalg.eigvalsh(K).min() >= -1e-12
    assert not np.allclose(K, np.ones_like(K))
    assert np.allclose(kernel_matrix(points[:2], points[2:]), K[:2, 2:])


def test_invalid_parameters():
    for value in ([], [float("nan")], [float("inf")], ["word"], [1] * 7):
        with pytest.raises(ValueError):
            feature_state(value)
    with pytest.raises(ValueError):
        fidelity_kernel([0.2], [0.2, 0.3])
    with pytest.raises(ValueError):
        feature_state([0.1], reps=0)
    with pytest.raises(ValueError):
        kernel_matrix([[0.1], [0.1, 0.2]])
    with pytest.raises(ValueError):
        kernel_matrix([])
    assert quantum_cli(["kernel-matrix", "--points", "[[0.1,0.2],[0.2,0.1]]"]) == 0
    assert quantum_cli(["kernel-matrix", "--points", "[[1],[1,2]]"]) == 2


def test_svm_adapter_fit_predict():
    pytest.importorskip("sklearn")
    X = [[0.2, 0.2], [2.8, 2.8], [0.2, 2.8], [2.8, 0.2]]
    y = [-1, -1, 1, 1]
    m = QuantumKernelSVM(C=10)
    assert m.fit(X, y) is m
    assert len(m.predict(X)) == 4
    assert all(math.isfinite(float(v)) for v in m.decision_function(X))
    assert 0 <= m.score(X, y) <= 1
    with pytest.raises(RuntimeError):
        QuantumKernelSVM().predict(X)


def test_audit_hmac_detects_tampering_and_defensive_copy():
    trail = AuditTrail(secret_key="test-key")
    trail.log("auditor", "test", "EVALUATE", {"score": 2})
    assert trail.verify_integrity()
    copy = trail.get_trail()
    copy[0]["actor"] = "attacker"
    assert trail.verify_integrity()  # exported records cannot mutate the ledger
    trail.logs[0]["actor"] = "attacker"
    assert not trail.verify_integrity()


def test_audit_signature_rejects_modified_payload_hash():
    trail = AuditTrail(secret_key="test-key")
    trail.log("auditor", "test", "EVALUATE", {"score": 2})
    trail.logs[0]["payload_hash"] = "0" * 64
    assert not trail.verify_integrity()
