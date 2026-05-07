from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from fastapi.templating import Jinja2Templates
from fastapi import Request
#uvicorn main:app --reload
# 1. Avval APP obyektini yaratamiz
app = FastAPI(title="Mahalla Boshqaruv API (To'liq)")

# 2. Keyin ma'lumotlar bazasini ulaymiz
models.Base.metadata.create_all(bind=models.engine)

# 3. Shablonlarni sozlaymiz
templates = Jinja2Templates(directory="templates")
# Python 3.14 dagi kesh xatoligini bartaraf etish uchun:
templates.env.cache = None

# 4. Dependency funksiyasini yozamiz
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. ENDI yo'nalishlarni (Routes) yozish mumkin
@app.get("/", tags=["Frontend"])
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # Ma'lumotlarni bazadan yuklash
    xonadonlar = db.query(models.Xonadon).all()
    aholi = db.query(models.Aholi).all()
    arizalar = db.query(models.Arizalar).all()
    infra = db.query(models.Infratuzilmalar).all()
    xodimlar = db.query(models.Xodimlar).all()
    hodisalar = db.query(models.Hodisalar).all() 
    for h in hodisalar:
        if h.vaqti:
            h.formatted_date = h.vaqti.strftime("%d.%m.%Y %H:%M")
        
    context = {
        "request": request,
        "xonadonlar": xonadonlar,
        "aholi": aholi,
        "arizalar": arizalar,
        "infra": infra,
        "xodimlar": xodimlar,
        "hodisalar": hodisalar, 
        "stats": {
            "aholi_soni": len(aholi),
            "xonadonlar_soni": len(xonadonlar),
            "arizalar_soni": len(arizalar),
            "infratuzilmalar_soni":len(infra), 
            "hodisalar_soni": len(hodisalar),
            "xodimlar_soni": len(xodimlar)
        }
    }
    return templates.TemplateResponse(
    request=request, 
    name="index.html", 
    context=context
)
# Qolgan @app.post va boshqa funksiyalar shu yerda davom etadi...

# --- 1. XONADONLAR ---
@app.post("/xonadonlar/", tags=["Xonadonlar"])
def add_xonadon(manzili: str, uy_egasi: str, qarzlar: int = 0, db: Session = Depends(get_db)):
    obj = models.Xonadon(manzili=manzili, uy_egasi=uy_egasi, qarzlar=qarzlar)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/xonadonlar/", tags=["Xonadonlar"])
def get_xonadonlar(db: Session = Depends(get_db)):
    return db.query(models.Xonadon).all()

# --- 2. AHOLI ---
@app.post("/aholi/", tags=["Aholi"])
def add_aholi(xonadon_id: int, fio: str, tugilgan_sana: str, jinsi: str, pasport: str, tel: str, holati: str, db: Session = Depends(get_db)):
    obj = models.Aholi(xonadon_id=xonadon_id, fio=fio, tugilgan_sana=tugilgan_sana, jinsi=jinsi, pasport_malumot=pasport, telefon=tel, ijtimoiy_holati=holati)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/aholi/", tags=["Aholi"])
def get_aholi(db: Session = Depends(get_db)):
    return db.query(models.Aholi).all()

# --- 3. ARIZALAR ---
@app.post("/arizalar/", tags=["Arizalar"])
def add_ariza(kimdan: str, ariza_tafsiloti: str,aholi_id:int, db: Session = Depends(get_db)):
    obj = models.Arizalar(ariza_beruvchi=kimdan, tafsilotlari=ariza_tafsiloti,aholi_id=aholi_id)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/arizalar/", tags=["Arizalar"])
def get_arizalar(db: Session = Depends(get_db)):
    return db.query(models.Arizalar).all()

# --- 4. INFRATUZILMA ---
@app.post("/infratuzilma/", tags=["Infratuzilma"])
def add_infra(turi: str, holati: str, manzili: str, tashkilot: str, db: Session = Depends(get_db)):
    obj = models.Infratuzilmalar(turi=turi, holati=holati, manzili=manzili, masul_tashkilot=tashkilot)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/infratuzilma/", tags=["Infratuzilma"])
def get_infra(db: Session = Depends(get_db)):
    return db.query(models.Infratuzilmalar).all()

# --- 5. XODIMLAR ---
@app.post("/xodimlar/", tags=["Xodimlar"])
def add_xodim(fio: str, lavozimi: str, tel: str, db: Session = Depends(get_db)):
    obj = models.Xodimlar(fio=fio, lavozimi=lavozimi, aloqa_nomeri=tel)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/xodimlar/", tags=["Xodimlar"])
def get_xodimlar(db: Session = Depends(get_db)):
    return db.query(models.Xodimlar).all()

# --- 6. HODISALAR ---
@app.post("/hodisalar/", tags=["Hodisalar"])
def add_hodisa(xodim_id: int, joyi: str, hodisa_turi: str, db: Session = Depends(get_db)):
    obj = models.Hodisalar(xodim_id=xodim_id, joyi=joyi, zarar=hodisa_turi)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/hodisalar/", tags=["Hodisalar"])
def get_hodisalar(db: Session = Depends(get_db)):
    return db.query(models.Hodisalar).all()