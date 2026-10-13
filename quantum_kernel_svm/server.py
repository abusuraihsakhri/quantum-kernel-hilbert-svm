"""
FastAPI REST API Server for Quantum Kernel Hilbert Space Support Vector Machine Agent.
"""
from typing import Dict, List
from .models import FrontierPayload
from .kernel import kernel_matrix
from .agents import QuantumKernelCoordinator

coordinator = QuantumKernelCoordinator()


def create_app():
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel, Field

        app = FastAPI(
            title="Quantum Kernel Hilbert Space Support Vector Machine Agent",
            description="Provides a separate legacy alert workflow and a noiseless simulated quantum fidelity kernel endpoint.",
            version="2.0.0-FRONTIER",
        )

        class TaskRequest(BaseModel):
            task_id: str = "TASK-2026-001"
            target_identifier: str = "TARGET-BIO-KEY"
            primary_metric: float = 28.5
            secondary_metric: float = 14.2
            status_descriptor: str = "DISCORDANT_ANOMALY"
            is_critical_flag: bool = True
            attributes: Dict[str, Any] = {}

        class ChatRequest(BaseModel):
            query: str

        class KernelRequest(BaseModel):
            points: List[List[float]] = Field(..., min_length=1, max_length=24)
            reps: int = Field(default=2, ge=1, le=4)

        @app.post("/api/kernel")
        def api_kernel(req: KernelRequest):
            from fastapi import HTTPException
            try:
                return {"kernel_matrix": kernel_matrix(req.points, reps=req.reps)}
            except (ValueError, TypeError) as exc:
                raise HTTPException(status_code=422, detail=str(exc))

        @app.get("/health")
        def health():
            return {"status": "HEALTHY", "system": "quantum-kernel-hilbert-svm", "domain": "Quantum Machine Learning", "version": "2.0.0-FRONTIER"}

        @app.post("/api/audit")
        def api_audit(req: TaskRequest):
            payload = FrontierPayload(
                task_id=req.task_id,
                target_identifier=req.target_identifier,
                primary_metric=req.primary_metric,
                secondary_metric=req.secondary_metric,
                status_descriptor=req.status_descriptor,
                is_critical_flag=req.is_critical_flag,
                attributes=req.attributes,
            )
            return coordinator.process(payload)

        @app.post("/api/chat")
        def api_chat(req: ChatRequest):
            return {"response": coordinator.query_supervisory_chat(req.query)}

        return app
    except ImportError:
        return None
