from datetime import datetime
from gettext import translation
from fastapi import FastAPI, Request
from fastapi_babel import Babel, BabelConfigs, BabelMiddleware
from babel import Locale, dates, numbers
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# 定義一個函數來動態加載翻譯
def get_translations(language: str):
  try:
    translations = translation('messages', localedir='translations', languages=[language])
    return translations   # 返回翻譯對象，而不是安裝全局 _ 函數
  except Exception as e:
    print(f"Error loading translations: {e}")
    return None

# ==========================
# 國際化設置 (i18n)
# ==========================

# 設置 Babel 中介軟體，指定翻譯文件的目錄和預設語言
babel_configs = BabelConfigs(
  ROOT_DIR=__file__,
  BABEL_DEFAULT_LOCALE="en",
  BABEL_TRANSLATION_DIRECTORY="translations"
)

app.add_middleware(BabelMiddleware, babel_configs=babel_configs)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# 國際化演示： 顯示根據當前語言設置的國際化訊息
@app.get("/")
async def read_root(request: Request):
  # 如果 session 中有設置語言，則使用 session 中的語言
  language = request.session.get('language', None)

  # 如果 session 沒有語言設置，則使用 Accept-Language 標頭來確定語言
  if not language:
      language = request.headers.get('accept-language', 'en').split(',')[0]  # 默認為 'en' (英文)
    
  # 加載翻譯文件
  translations = get_translations(language)
  
  if translations is None:
    return {"error": "Could not load translations."}
  
  # 使用當前翻譯對象進行翻譯
  _ = translations.gettext

  return {"message": _("Hello, world!")}

# 語言切換端點。用於用戶根據請求切換語言
@app.get("/set_language/{language}")
async def set_language(language: str, request: Request):
  try:
    # 儲存語言選擇到 session
    request.session['language'] = language
    
    # 加載翻譯文件
    language = request.session.get('language', 'en')   # 默認使用英語
    translations = get_translations(language)

    if translations is None:
      return {"error": "Could not load translations."}
    
    # 使用當前翻譯對象來翻譯字串
    _ = translations.gettext

    return {"message": _("Language has been set to: ") + language}
  
  except Exception as e:
    return {"error": f"Failed to set language: {e}"}



# =========================
# 本地化設置 (i10n)
# =========================

# 本地化內容演示：根據當前語言設置顯示本地化的日期和數字
@app.get("/localized_content")
async def localized_content(request: Request):
  # 從 session 中獲取當前語言，如果沒有，使用默認語言 'en'
  language = request.session.get('language', 'en')
  translations = get_translations(language)

  if translations is None:
    return {"error": "Cloud not load translations."}
  
  # 使用當前翻譯對象進行翻譯
  _ = translations.gettext

  # 使用 Babel 格式化日期和數字，根據當前語言格式化
  today = datetime.today()    # 使用 datetime.today() 來獲取今天的日期
  formatted_date = dates.format_date(today, locale=language)
  formatted_number =  numbers.format_decimal(1234567.89, locale=language)

  # 返回本地化的日期和數字
  return {
    "message": _("Localized content"),
    "formatted_date": formatted_date,
    "formatted_number": formatted_number
  }