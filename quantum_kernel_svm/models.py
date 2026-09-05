"""
Data Models & Telemetry Definitions for Quantum Kernel Hilbert Space Support Vector Machine Agent.
Domain: Quantum Machine Learning
Standard: Havlicek 2019 Quantum Kernel Protocol
"""
import datetime
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any


class ExecutionStatus(str, Enum):
    NOMINAL = "NOMINAL_OPTIMAL"
    ELEVATED_RISK = "ELEVATED_RISK_WARNING"
    CRITICAL_INTERVENTION = "CRITICAL_INTERVENTION_REQUIRED"


@dataclass
class FrontierPayload:
    task_id: str
    target_identifier: str
    primary_metric: float
    secondary_metric: float
    status_descriptor: str
    is_critical_flag: bool = False
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def __post_init__(self):
        if math.isnan(self.primary_metric) or math.isinf(self.primary_metric):
            raise ValueError(f"primary_metric must be finite, got {self.primary_metric}")
        if math.isnan(self.secondary_metric) or math.isinf(self.secondary_metric):
            raise ValueError(f"secondary_metric must be finite, got {self.secondary_metric}")


@dataclass
class AgentTelemetryAlert:
    alert_id: str
    origin_agent: str
    status: ExecutionStatus
    summary: str
    technical_details: str
    actionable_remediation: str
    standard_reference: str = "Havlicek 2019 Quantum Kernel Protocol"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "origin_agent": self.origin_agent,
            "status": self.status.value,
            "summary": self.summary,
            "technical_details": self.technical_details,
            "actionable_remediation": self.actionable_remediation,
            "standard_reference": self.standard_reference,
            "timestamp": self.timestamp,
        }
