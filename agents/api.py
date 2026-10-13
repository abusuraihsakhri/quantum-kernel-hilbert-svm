"""
FastAPI REST API Server for Quantum Kernel Hilbert Svm.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
from fastapi.responses import FileResponse
from quantum_kernel_svm.kernel import kernel_matrix
from .base import AuditLogger, PHIGuard, SecurityException
from .models import SystemTaskPayload
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Quantum Kernel Hilbert Svm API",
    description="Enterprise Distributed Component Platform (Deterministic Threshold Assessment)",
    version="3.0.0-ENTERPRISE",
)


class ChatRequest(BaseModel):
    query: str


class KernelRequest(BaseModel):
    points: list[list[float]] = Field(..., min_length=1, max_length=24)
    reps: int = Field(default=2, ge=1, le=4)


@app.post("/api/kernel")
def api_kernel(request: KernelRequest):
    try:
        return {"kernel_matrix": kernel_matrix(request.points, reps=request.reps)}
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@app.get("/")
def home():
    index = Path(__file__).resolve().parent.parent / "web" / "index.html"
    if not index.is_file():
        raise HTTPException(status_code=404, detail="Browser UI not installed")
    return FileResponse(index)


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "quantum-kernel-hilbert-svm", "domain": "Deterministic Threshold Assessment", "standard": "Repository-defined threshold rules (not externally validated)", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    try:
        dossier = supervisor.process_task(payload)
    except SecurityException:
        raise HTTPException(status_code=422, detail="Input includes a potentially sensitive identifier")
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
