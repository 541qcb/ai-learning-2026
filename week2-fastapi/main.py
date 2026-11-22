from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from models import Patient, Visit

app = FastAPI(title="Clinic API", version="0.3.0")


class PatientIn(BaseModel):
    patient_id: str = Field(pattern=r"^P\d{3}$", description="患者编号，形如 P001")
    name: str = Field(min_length=1, max_length=50)
    dept: str = Field(min_length=1, max_length=50)


@app.get("/")
def root():
    return {"service": "clinic-api", "docs": "/docs"}


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(select(func.count()).select_from(Patient))
    return {"status": "ok", "database": "up"}


@app.get("/patients")
def list_patients(db: Session = Depends(get_db)):
    rows = db.execute(select(Patient).order_by(Patient.patient_id)).scalars().all()
    return [
        {"patient_id": p.patient_id, "name": p.name, "dept": p.dept}
        for p in rows
    ]


@app.get("/patients/search")
def search_patients(name: str, db: Session = Depends(get_db)):
    stmt = select(Patient).where(Patient.name.like(f"%{name}%"))
    rows = db.execute(stmt).scalars().all()
    return [
        {"patient_id": p.patient_id, "name": p.name, "dept": p.dept}
        for p in rows
    ]


@app.get("/stats")
def dept_stats(dept: str, year: int = 2026, month: int = 10, db: Session = Depends(get_db)):
    start = f"{year:04d}-{month:02d}-01"
    if month == 12:
        end = f"{year + 1:04d}-01-01"
    else:
        end = f"{year:04d}-{month + 1:02d}-01"

    stmt = (
        select(
            func.count(),
            func.sum(Visit.total_fee),
            func.avg(Visit.total_fee),
        )
        .join(Patient, Visit.patient_id == Patient.patient_id)
        .where(Patient.dept == dept)
        .where(Visit.visit_date >= start, Visit.visit_date < end)
    )
    visits, total_fee, avg_fee = db.execute(stmt).one()

    total_fee = total_fee if total_fee is not None else 0
    avg_fee = round(avg_fee, 2) if avg_fee is not None else 0

    return {
        "dept": dept,
        "visits": visits,
        "total_fee": round(total_fee, 2),
        "avg_fee": avg_fee,
    }


@app.post("/patients", status_code=201, summary="新增患者",
          responses={409: {"description": "患者编号已存在"}})
def add_patient(p: PatientIn, db: Session = Depends(get_db)):
    obj = Patient(patient_id=p.patient_id, name=p.name, dept=p.dept)
    db.add(obj)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"患者编号 {p.patient_id} 已存在，请换一个编号",
        )
    return {"patient_id": obj.patient_id, "name": obj.name, "dept": obj.dept}
