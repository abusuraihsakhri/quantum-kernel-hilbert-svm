"""
Security and Input Validation Tests for Quantum Kernel Hilbert Svm.
Tests for metric validation, file error handling, and secure key generation.
"""
import sys
import math
import os
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import AuditTrail, PHIGuard, SecurityException
from agents.models import SystemTaskPayload
from quantum_kernel_svm.models import FrontierPayload
from cli import main as primary_cli_main
from quantum_kernel_svm.cli import main as qkernel_cli_main


class TestMetricValidation:
    """Tests for NaN and Inf input validation."""

    def test_system_task_payload_rejects_nan_primary(self):
        with pytest.raises(ValueError, match="finite"):
            SystemTaskPayload(
                task_id="T1",
                target_identifier="KEY-01",
                primary_metric=float("nan"),
                secondary_metric=5.0,
            )

    def test_system_task_payload_rejects_nan_secondary(self):
        with pytest.raises(ValueError, match="finite"):
            SystemTaskPayload(
                task_id="T1",
                target_identifier="KEY-01",
                primary_metric=10.0,
                secondary_metric=float("nan"),
            )

    def test_system_task_payload_rejects_inf_primary(self):
        with pytest.raises(ValueError, match="finite"):
            SystemTaskPayload(
                task_id="T1",
                target_identifier="KEY-01",
                primary_metric=float("inf"),
                secondary_metric=5.0,
            )

    def test_system_task_payload_rejects_neg_inf_secondary(self):
        with pytest.raises(ValueError, match="finite"):
            SystemTaskPayload(
                task_id="T1",
                target_identifier="KEY-01",
                primary_metric=10.0,
                secondary_metric=float("-inf"),
            )

    def test_system_task_payload_accepts_valid_metrics(self):
        payload = SystemTaskPayload(
            task_id="T1",
            target_identifier="KEY-01",
            primary_metric=10.0,
            secondary_metric=5.0,
        )
        assert payload.primary_metric == 10.0
        assert payload.secondary_metric == 5.0

    def test_frontier_payload_rejects_nan_primary(self):
        with pytest.raises(ValueError, match="finite"):
            FrontierPayload(
                task_id="T1",
                target_identifier="KEY-01",
                primary_metric=float("nan"),
                secondary_metric=5.0,
                status_descriptor="NOMINAL",
            )

    def test_frontier_payload_rejects_inf_secondary(self):
        with pytest.raises(ValueError, match="finite"):
            FrontierPayload(
                task_id="T1",
                target_identifier="KEY-01",
                primary_metric=10.0,
                secondary_metric=float("inf"),
                status_descriptor="NOMINAL",
            )

    def test_frontier_payload_accepts_valid_metrics(self):
        payload = FrontierPayload(
            task_id="T1",
            target_identifier="KEY-01",
            primary_metric=10.0,
            secondary_metric=5.0,
            status_descriptor="NOMINAL",
        )
        assert payload.primary_metric == 10.0
        assert payload.secondary_metric == 5.0


class TestFileErrorHandling:
    """Tests for batch command file error handling."""

    def test_primary_cli_batch_missing_file(self):
        result = primary_cli_main(["batch", "-i", "/nonexistent/path/file.csv"])
        assert result == 1

    def test_qkernel_cli_batch_missing_file(self):
        result = qkernel_cli_main(["batch", "-i", "/nonexistent/path/file.csv"])
        assert result == 1

    def test_primary_cli_batch_valid_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            f.write("task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n")
            f.write("TASK-001,TARGET-01,12.0,4.1,False,NOMINAL\n")
            temp_path = f.name
        try:
            result = primary_cli_main(["batch", "-i", temp_path, "-o", temp_path + ".out.csv"])
            assert result == 0
            os.unlink(temp_path + ".out.csv")
        finally:
            os.unlink(temp_path)


class TestSecureKeyGeneration:
    """Tests for secure audit key generation."""

    def test_audit_trail_generates_random_key_when_no_env(self):
        """When no key is provided and no env var is set, a random key should be generated."""
        original = os.environ.pop("AUDIT_SECRET_KEY", None)
        try:
            trail = AuditTrail()
            assert len(secret_key := trail.secret_key) > 0
            # Key should be bytes
            assert isinstance(trail.secret_key, bytes)
        finally:
            if original is not None:
                os.environ["AUDIT_SECRET_KEY"] = original

    def test_audit_trail_uses_env_var_when_set(self):
        os.environ["AUDIT_SECRET_KEY"] = "test-secret-key-12345"
        try:
            trail = AuditTrail()
            assert trail.secret_key == b"test-secret-key-12345"
        finally:
            os.environ.pop("AUDIT_SECRET_KEY", None)

    def test_audit_trail_uses_provided_key(self):
        trail = AuditTrail(secret_key="explicit-key")
        assert trail.secret_key == b"explicit-key"

    def test_different_instances_get_different_random_keys(self):
        """Two instances without explicit keys should have different random keys."""
        original = os.environ.pop("AUDIT_SECRET_KEY", None)
        try:
            trail1 = AuditTrail()
            trail2 = AuditTrail()
            assert trail1.secret_key != trail2.secret_key
        finally:
            if original is not None:
                os.environ["AUDIT_SECRET_KEY"] = original


class TestPHIGuardRedaction:
    """Tests for PHI guard redaction functionality."""

    def test_redact_phi_email(self):
        text = "Contact user@example.com for details"
        redacted = PHIGuard.redact_phi(text)
        assert "[REDACTED_IDENTIFIER]" in redacted
        assert "user@example.com" not in redacted

    def test_redact_phi_ssn(self):
        text = "Patient SSN: 123-45-6789"
        redacted = PHIGuard.redact_phi(text)
        assert "[REDACTED_IDENTIFIER]" in redacted
        assert "123-45-6789" not in redacted

    def test_redact_phi_mrn(self):
        text = "MRN-12345678 recorded"
        redacted = PHIGuard.redact_phi(text)
        assert "[REDACTED_IDENTIFIER]" in redacted

    def test_clean_text_unchanged(self):
        text = "Analytical specimen KEY-001 optimal"
        assert PHIGuard.redact_phi(text) == text
