from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import SessionLocal
from db import get_dept_fee_summary, search_patients_by_keyword
from models import Patient
from sqlalchemy import func, select
from models import Patient, Visit

app = FastAPI(title="门诊数据接口", version="0.1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PatientIn(BaseModel):
    patient_id: str = Field(
        pattern=r"^P\d{3}$", description="格式 P + 3 位数字，如 P001"
    )
    name: str = Field(min_length=1, max_length=20)
    dept: str = Field(min_length=1, max_length=20)


@app.get("/")
def root():
    return {"message": "门诊数据接口已启动"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    rows = db.execute(select(Patient)).scalars().all()
    return rows


@app.get("/patients/search")
def search(name: str):
    return search_patients_by_keyword(name)


@app.get("/stats")
def stats(dept: str, start: str, end: str, db: Session = Depends(get_db)):
    stmt = (
        select(
            func.count(),
            func.sum(Visit.total_fee),
            func.avg(Visit.total_fee),
        )
        .join(Patient, Visit.patient_id == Patient.patient_id)
        .where(Patient.dept == dept, Visit.visit_date.between(start, end))
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



@app.post(
    "/patients",
    status_code=201,
    summary="新增患者",
    responses={409: {"description": "患者编号已存在"}},
)
def add_patient(p: PatientIn, db: Session = Depends(get_db)):
    obj = Patient(patient_id=p.patient_id, name=p.name, dept=p.dept)
    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"患者编号 {p.patient_id} 已存在，请换一个编号",
        )
    return obj


