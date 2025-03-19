from fastapi import FastAPI, BackgroundTasks
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 建立 SQLite 資料庫連結
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 創建資料庫基礎類別
Base = declarative_base()

# 模擬資料庫模型
class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, index=True)
  created_at = Column(DateTime, default=datetime.now(timezone.utc))

# 建立資料庫和資料表
Base.metadata.create_all(bind=engine)

# 建立 Session 類型
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化 FastAPI 應用
app = FastAPI()

# 插入5筆初始資料
def insert_initial_data():
  db = SessionLocal()
  initial_users = [
    User(username="user1"),
    User(username="user2"),
    User(username="user3"),
    User(username="user4"),
    User(username="user5")
  ]
  db.add_all(initial_users)
  db.commit()
  db.close()

# 初始化資料庫資料
insert_initial_data()

# 清理過期用戶的背景
def clean_expired_users():
  db = SessionLocal()
  # expiration_time = datetime.now(timezone.utc) - timedelta(days=30)
  expiration_time = datetime.now(timezone.utc) - timedelta(seconds=30)
  # expired_count = db.query(User).filter(User.created_at < expiration_time).delete()
  db.query(User).filter(User.created_at < expiration_time).delete()
  db.commit()
  db.close()
  # logging.info(f"Cleaned {expired_count} expired users.")

# 建立背景排程器
scheduler = BackgroundScheduler()

# 定義定期清理任務，每30秒執行一次
scheduler.add_job(clean_expired_users, IntervalTrigger(seconds=30))

# 啟動排程器
scheduler.start()

# 當應用結束時關閉排程器
@app.on_event("shutdown")
def shutdown_event():
  scheduler.shutdown()

# FastAPI API 端點來立即啟動清理過期用戶
@app.get("/clean-users/")
async def clean_users(background_tasks: BackgroundTasks):
  # 將清理操作放入背景執行
  background_tasks.add_task(clean_expired_users)
  return {"message": "User cleanup task started"}

@app.get("/check-users/")
async def check_users():
    db = SessionLocal()
    current_time = datetime.now(timezone.utc)
    users = db.query(User).all()
    expired_users = [user for user in users if user.created_at < current_time - timedelta(seconds=10)]  # 這裡10秒是過期的判斷標準
    db.close()
    return {"total_users": len(users), "expired_users": len(expired_users), "users": [user.username for user in users]}