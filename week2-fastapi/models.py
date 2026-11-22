from datetime import date
from sqlalchemy import String, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    dept: Mapped[str] = mapped_column(String(50), nullable=False)


class Visit(Base):
    __tablename__ = "visits"

    visit_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[str] = mapped_column(
        String(10), ForeignKey("patients.patient_id"), nullable=False
    )
    visit_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_fee: Mapped[float] = mapped_column(Float, nullable=False)
    diagnosis: Mapped[str] = mapped_column(String(100))
