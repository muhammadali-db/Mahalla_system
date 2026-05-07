from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone

SQLALCHEMY_DATABASE_URL = "sqlite:///./mahalla_tizimi.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False,"timeout": 30})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Xonadon(Base):
    __tablename__ = "xonadon"
    xonadon_id = Column(Integer, primary_key=True, index=True)
    manzili = Column(String(400))
    uy_egasi = Column(String(255))
    qarzlar = Column(Integer, default=0)
    aholilar = relationship("Aholi", back_populates="xonadon")

class Aholi(Base):
    __tablename__ = "aholi"
    aholi_id = Column(Integer, primary_key=True, index=True)
    xonadon_id = Column(Integer, ForeignKey("xonadon.xonadon_id"),index=True)
    fio = Column(String(255))
    tugilgan_sana = Column(String)
    jinsi = Column(String(10))
    pasport_malumot = Column(String(50))
    telefon = Column(String(20))
    ijtimoiy_holati = Column(String(255))
    xonadon = relationship("Xonadon", back_populates="aholilar")
    arizalari = relationship("Arizalar", back_populates="muallif")

class Arizalar(Base):
    __tablename__ = "arizalar"
    ariza_id = Column(Integer, primary_key=True, index=True)
    ariza_beruvchi = Column(String(255))
    tafsilotlari = Column(String(1000))
    ariza_holati = Column(String(100), default="Yangi")
    aholi_id = Column(Integer, ForeignKey("aholi.aholi_id"),index=True,nullable=True)
    muallif = relationship("Aholi", back_populates="arizalari")

class Infratuzilmalar(Base):
    __tablename__ = "infratuzilmalar"
    obyekt_id = Column(Integer, primary_key=True, index=True)
    turi = Column(String(100))
    holati = Column(String(100))
    manzili = Column(String(400))
    masul_tashkilot = Column(String(200))

class Xodimlar(Base):
    __tablename__ = "xodimlar"
    xodim_id = Column(Integer, primary_key=True, index=True)
    fio = Column(String(255))
    lavozimi = Column(String(100))
    aloqa_nomeri = Column(String(20))

class Hodisalar(Base):
    __tablename__ = "hodisalar"
    hodisa_id = Column(Integer, primary_key=True, index=True)
    xodim_id = Column(Integer, ForeignKey("xodimlar.xodim_id"),index=True)
    vaqti = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    joyi = Column(String(300))
    zarar = Column(String(300))
