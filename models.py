from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """所有模型的基类，SQLAlchemy 靠它收集表定义"""
    pass


class Patient(Base):
    __tablename__ = "patients"          # ← 对应数据库里已有的表名

    patient_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    dept: Mapped[str] = mapped_column(String(50))


class Visit(Base):
    __tablename__ = "visits"

    visit_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[str] = mapped_column(String(20))
    visit_date: Mapped[str] = mapped_column(String(20))
    total_fee: Mapped[float] = mapped_column(Float)
    diagnosis: Mapped[str | None] = mapped_column(String(200))
