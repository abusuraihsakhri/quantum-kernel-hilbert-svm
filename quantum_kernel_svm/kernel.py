"""Small exact-statevector simulator for a ZZ-feature-map fidelity kernel.

Noiseless, Havlicek-inspired feature map. No quantum hardware/advantage claims.
"""
import cmath
import math
from typing import Iterable, List, Sequence

MAX_QUBITS = 6


def _validate_vector(vector: Sequence[float]) -> tuple:
    try:
        values = tuple(float(v) for v in vector)
    except (ValueError, TypeError) as exc:
        raise ValueError("Features must be a sequence of real numbers") from exc
    if not (1 <= len(values) <= MAX_QUBITS):
        raise ValueError(f"Expected between 1 and {MAX_QUBITS} features/qubits")
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Features must be finite")
    return values


def feature_state(features: Sequence[float], reps: int = 2) -> List[complex]:
    """Normalized statevector of repeated H / ZZ-diagonal feature-map layers."""
    x = _validate_vector(features)
    if type(reps) is not int or not (1 <= reps <= 4):
        raise ValueError("reps must be an integer from 1 to 4")
    count = 1 << len(x)
    state = [0j] * count
    state[0] = 1.0 + 0j
    for _ in range(reps):
        for bit in range(len(x)):
            mask = 1 << bit
            for pos in range(count):
                if not pos & mask:
                    a, b = state[pos], state[pos | mask]
                    state[pos] = (a + b) / math.sqrt(2)
                    state[pos | mask] = (a - b) / math.sqrt(2)
        for pos in range(count):
            z = [1 if pos & (1 << bit) == 0 else -1 for bit in range(len(x))]
            angle = sum(val * sign for val, sign in zip(x, z))
            angle += sum((math.pi - x[i]) * (math.pi - x[j]) * z[i] * z[j]
                         for i in range(len(x)) for j in range(i + 1, len(x)))
            state[pos] *= cmath.exp(1j * angle)
    return state


def _fidelity(left: Sequence[complex], right: Sequence[complex]) -> float:
    overlap = sum(a.conjugate() * b for a, b in zip(left, right))
    return max(0.0, min(1.0, abs(overlap) ** 2))


def fidelity_kernel(x: Sequence[float], y: Sequence[float], reps: int = 2) -> float:
    """K(x,y) = |<phi(x)|phi(y)>|^2."""
    a, b = _validate_vector(x), _validate_vector(y)
    if len(a) != len(b):
        raise ValueError("Feature dimensions must match")
    return _fidelity(feature_state(a, reps), feature_state(b, reps))


def kernel_matrix(X: Iterable[Sequence[float]], Y=None, reps: int = 2) -> List[List[float]]:
    """Compute the PSD Gram matrix; symmetric when Y is omitted."""
    rows = [_validate_vector(x) for x in X]
    if not rows:
        raise ValueError("X cannot be empty")
    cols = rows if Y is None else [_validate_vector(y) for y in Y]
    if not cols:
        raise ValueError("Y cannot be empty")
    n = len(rows[0])
    if any(len(v) != n for v in rows + cols):
        raise ValueError("All feature vectors must have the same dimension")
    states_x = [feature_state(x, reps) for x in rows]
    states_y = states_x if Y is None else [feature_state(y, reps) for y in cols]
    result = [[0.0] * len(cols) for _ in rows]
    if Y is None:
        for i in range(len(rows)):
            for j in range(i, len(rows)):
                result[i][j] = result[j][i] = _fidelity(states_x[i], states_y[j])
    else:
        for i, s in enumerate(states_x):
            result[i] = [_fidelity(s, t) for t in states_y]
    return result


class QuantumKernelSVM:
    """scikit-learn SVC using the fidelity kernel; install the ml extra."""

    def __init__(self, C: float = 1.0, reps: int = 2):
        if not isinstance(C, (int, float)) or not math.isfinite(C) or C <= 0:
            raise ValueError("C must be positive and finite")
        self.C = C
        self.reps = reps
        self._model = None
        self._train = None

    def fit(self, X, y):
        try:
            from sklearn.svm import SVC
        except ImportError as exc:
            raise ImportError("Install quantum-kernel-hilbert-svm[ml] to train an SVM") from exc
        rows = [_validate_vector(x) for x in X]
        if len(rows) != len(y):
            raise ValueError("X and y must have equal numbers of observations")
        model = SVC(C=self.C, kernel="precomputed")
        model.fit(kernel_matrix(rows, reps=self.reps), y)
        self._train, self._model = rows, model
        return self

    def _matrix(self, X):
        if self._model is None:
            raise RuntimeError("Call fit before prediction")
        return kernel_matrix(X, self._train, reps=self.reps)

    def predict(self, X):
        return self._model.predict(self._matrix(X)) if self._model is not None else self._not_fitted()

    def decision_function(self, X):
        return self._model.decision_function(self._matrix(X)) if self._model is not None else self._not_fitted()

    def score(self, X, y):
        return self._model.score(self._matrix(X), y) if self._model is not None else self._not_fitted()

    @staticmethod
    def _not_fitted():
        raise RuntimeError("Call fit before prediction")
