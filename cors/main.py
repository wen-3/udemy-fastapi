from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 設定允許的來源
origins = [
  "http://localhost",
  "http://localhost:5500",    # 假設前端在此運行
  "https://yourfrontenddomain.com"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,     # 允許的來源
  allow_credentials = True,    # 是否允許攜帶憑證
  allow_methods=["*"],         # 允許的 http 方法
  allow_headers=["*"]          # 允許的 http 標頭
)

@app.get("/")
async def root():
  return {"message": "CORS 設定成功"}