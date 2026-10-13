"""Regression tests for CSV booleans and API error handling."""
import csv
import json
import pytest

from agents.base import SecurityException
from quantum_kernel_svm.validation import parse_boolean
from cli import main as primary_main
from quantum_kernel_svm.cli import main as secondary_main


@pytest.mark.parametrize("raw,expected", [
    ("False", False), ("false", False), ("0", False), ("no", False),
    ("", False), ("True", True), ("1", True), ("yes", True),
])
def test_parse_boolean(raw, expected):
    assert parse_boolean(raw) is expected


def test_invalid_boolean_rejected():
    with pytest.raises(ValueError):
        parse_boolean("sometimes")


@pytest.mark.parametrize("main", [primary_main, secondary_main])
def test_csv_false_does_not_trigger_critical_flag(main, tmp_path):
    source = tmp_path / "inputs.csv"
    target = tmp_path / "results.csv"
    source.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "T1,TARGET-01,2,2,False,NOMINAL\n"
        "T2,TARGET-02,2,2,True,NOMINAL\n", encoding="utf-8")
    assert main(["batch", "-i", str(source), "-o", str(target)]) == 0
    with target.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    key = "overall_urgency" if main == primary_main else "overall_status"
    assert rows[0][key] in ("ROUTINE", "NOMINAL_OPTIMAL")
    assert "CRITICAL" in rows[1][key]


def test_api_kernel_and_sensitive_identifier():
    from fastapi.testclient import TestClient
    from agents.api import app
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    assert client.get("/").status_code == 200
    response = client.post("/api/kernel", json={"points": [[0.1, 0.3], [0.2, 2.1]]})
    assert response.status_code == 200
    matrix = response.json()["kernel_matrix"]
    assert len(matrix) == 2 and matrix[0][0] == pytest.approx(1.0)
    assert client.post("/api/kernel", json={"points": [[0.1], [0.2, 0.3]]}).status_code == 422
    payload = {
        "task_id": "T1", "target_identifier": "TARGET-01", "primary_metric": 1,
        "attributes": {"note": "user@example.com"}
    }
    denied = client.post("/api/audit", json=payload)
    assert denied.status_code == 422
    assert "user@example.com" not in denied.text
