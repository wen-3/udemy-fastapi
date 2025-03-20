- 安裝套件
    
    `pip install Babel fastapi-babel`
    
    `pip install python-gettext starlette`
    
- 產生 message.pot 檔案
    
    `pybabel extract -F babel.cfg -o message.pot .`
    
- 在 translations 產生 xxx.po 檔案
    
    `pybabel init -i message.pot -d translations -l en`
    
    `pybabel init -i message.pot -d translations -l zh_TW`
    
    `pybabel init -i message.pot -d translations -l fa`
    
    產生內容大致如下
    
    ```
    #: i18n.py:49
    msgid "Language has been set to: "
    msgstr ""
    
    #: i18n.py:57
    msgid "Hello, world!"
    msgstr ""
    
    #: i18n.py:82
    msgid "Localized content"
    msgstr ""
    ```
    
    => 接著透過 ChatGPT 提示詞翻譯，再將結果貼回對應檔案中
    
    - 中文
        
        ```
        將下面 msgid 的字串轉成中文放置在 msgstr 的字串中
        #: i18n.py:49
        msgid "Language has been set to: "
        msgstr ""
        
        #: i18n.py:57
        msgid "Hello, world!"
        msgstr ""
        
        #: i18n.py:82
        msgid "Localized content"
        msgstr ""
        ```
        
    - 英文
        
        ```
        將下面 msgid 的字串，複製到 msgstr 的字串中
        #: i18n.py:49
        msgid "Language has been set to: "
        msgstr ""
        
        #: i18n.py:57
        msgid "Hello, world!"
        msgstr ""
        
        #: i18n.py:82
        msgid "Localized content"
        msgstr ""
        ```
        
    - 法文
        
        ```
        將下面 msgid 的字串轉成法文放置在 msgstr 的字串中
        #: i18n.py:49
        msgid "Language has been set to: "
        msgstr ""
        
        #: i18n.py:57
        msgid "Hello, world!"
        msgstr ""
        
        #: i18n.py:82
        msgid "Localized content"
        msgstr ""
        ```
        
- 產生 xxx.mo (對應 xxx.po 檔案)
    
    `pybabel compile -d translations`
    

【補充】

將 translations 檔案中的檔名 `zh_TW` 改成 `zh-TW`

因為 `main.py` 中的 accept-language header 繁體中文為 `zh-TW`

- 執行
    
    `uvicorn main:app --reload`