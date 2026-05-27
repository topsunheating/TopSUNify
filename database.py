# database.py
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./topsun_floor.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_ARCHIVE_DIR = os.path.join(BASE_DIR, "Projects_Archive")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    agency_code = Column(String, unique=True, index=True, nullable=False) # ورود بر اساس کد نمایندگی
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)                            # نام نصاب / تیم / نماینده
    role_level = Column(Integer, default=4)                               # سطوح ۱ تا ۵ طبق سند
    is_active = Column(Boolean, default=True)                             # سیستم امنیتی Kill Switch
    needs_pass_reset = Column(Boolean, default=False)                     # پاپ‌آپ اختیاری/اجباری تغییر رمز
    created_at = Column(DateTime, default=datetime.utcnow)

class ProjectArchive(Base):
    __tablename__ = "project_archives"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String, unique=True, index=True, nullable=False)
    client_name = Column(String, nullable=False)
    system_type = Column(String, nullable=False)                          # گرمایش از کف، یخ‌زدایی و...
    user_id = Column(Integer, ForeignKey("users.id"))
    folder_path = Column(String, nullable=False)                          # مسیر فولدر اختصاصی پروژه
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """ایجاد جداول و ساخت کاربر مدیر کل اولیه سیستم"""
    Base.metadata.create_all(bind=engine)
    os.makedirs(PROJECTS_ARCHIVE_DIR, exist_ok=True)
    
    db = SessionLocal()
    admin = db.query(User).filter(User.agency_code == "TOPSUN-ADMIN").first()
    if not admin:
        root_admin = User(
            agency_code="TOPSUN-ADMIN",
            password_hash="admin1234",  # در فاز بعدی مکانیزم هش فعال می‌شود
            full_name="مدیریت کل سیستم Topsun Floor",
            role_level=1,
            is_active=True
        )
        db.add(root_admin)
        db.commit()
    db.close()

def create_project_folders(project_code, client_name):
    """
    بند ۷ سند: ساختار بایگانی سرور محلی
    ایجاد خودکار ۴ پوشه اختصاصی برای هر پروژه
    """
    safe_client_name = "".join([c for c in client_name if c.isalnum() or c in [' ', '_', '-']]).strip().replace(' ', '_')
    project_folder_name = f"{project_code}_{safe_client_name}"
    project_path = os.path.join(PROJECTS_ARCHIVE_DIR, project_folder_name)
    
    subfolders = [
        "Technical",               # فایل DXF مدیر، PDF مشتری، لیست BOM
        "Financial",               # پیش‌فاکتورها، رسیدها، فاکتور نهایی
        "Installation_Warranty",   # تصاویر، فیلم‌ها، فرم امضا تحویل، برگه گارانتی
        "Logs"                     # تاریخچه خدمات و رفع خرابی
    ]
    
    folder_mapping = {}
    for sub in subfolders:
        sub_path = os.path.join(project_path, sub)
        os.makedirs(sub_path, exist_ok=True)
        folder_mapping[sub] = sub_path
        
    return project_path, folder_mapping

def check_kill_switch(agency_code):
    """استعلام لحظه‌ای وضعیت کاربر برای خروج اجباری سریع در صورت غیرفعال شدن"""
    db = SessionLocal()
    user = db.query(User).filter(User.agency_code == agency_code).first()
    db.close()
    if user and not user.is_active:
        return False
    return True

if __name__ == "__main__":
    init_db()
    print("🎯 دیتابیس با قابلیت ساختار درختی بایگانی آماده استفاده است.")