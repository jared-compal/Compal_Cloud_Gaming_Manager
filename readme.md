# Compal Cloud Gaming Manager
____________________________________________
## 環境設定
* **python 環境和套件安裝**
<br>安裝完 python3 後，安裝相關 python 套件

`pip install virtualenv` : 安裝virtualenv

`virtualenv env`  : 創建新環境

`activate` : 啟動安裝環境 *(至activate檔所在file)*

`pip list` : 顯示 pip 安裝目錄

`pip install -r requirements.txt` : 從requirements.txt安裝 site-pkg

* **安裝 MySQL 和 MySQLWorkbench**

1. 安裝完 MySQL 和 MySQLWorkbench 後，如果沒有還沒有建置 DB，可以透過 Workbench 的 data import 功能，將 `db_replica.sql` 匯入至 MySQL 中，[教學網站在此](https://mnya.tw/cc/word/1395.html)
  

2. 需要在 /manager/config.py 中更改連線資料庫帳密和 IP address
  
`SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{IP address}:{port}/cloud_game_db"`

username: compal_admin
<br>password: admin
<br>IP: 10.113.8.192
<br>port: 3306
_____________________________________________
## 運行 Compal Cloud Gaming Manager
兩種方法
1. `activate` 啟動虛擬環境後，輸入 `python -m run.py `啟動 flask
2. 點擊 start.bat 程式自動進入 virualenv 並運行 flask

從瀏覽器輸入 `{IP address}:5000` 即可看到 "Welcome to the Compal VR Cloud Gaming"

可以使用 MySQLWorkbench 遠端連線檢視資料庫 schema 和資料
