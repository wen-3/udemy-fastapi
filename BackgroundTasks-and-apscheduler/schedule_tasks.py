from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

def scheduled_task():
  # 定期任務的執行內容
  with open("scheduled_log.txt", "a") as log_file:
    log_file.write("Scheduled task executed\n")
    
# 初始化排程器
scheduler = BackgroundScheduler()

# 每 10 秒執行一次
scheduler.add_job(scheduled_task, "interval", seconds=10)
scheduler.start()

@app.get("/")
async def root():
  return {"message": "Scheduler is running in the background"}