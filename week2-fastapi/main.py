import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


from db import (
    list_patients,
    search_patients_by_keyword,
    get_dept_fee_summary,
    create_patient,
)

app = FastAPI(title="门诊数据接口", version="0.1.0")


@app.get("/")
def root():
    return {"message": "门诊数据接口已启动"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/patients")
def get_patients():
    return list_patients()


@app.get("/patients/search")
def search(name: str):
    return search_patients_by_keyword(name)


@app.get("/stats")
def stats(dept: str, start: str, end: str):
    return get_dept_fee_summary(dept, start, end)


class PatientIn(BaseModel):
    patient_id: str
    name: str
    dept: str


@app.post("/patients", status_code=201)
def add_patient(p: PatientIn):
    try:
        return create_patient(p.patient_id, p.name, p.dept)
    except sqlite3.IntegrityError:
        raise HTTPException (
            status_code = 409,
            detail=f"患者编号{p.patient_id}已存在, 请换个编号",
        )



