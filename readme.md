# Compal Cloud Gaming Manager

## 環境設定
* **python 環境和套件安裝**
<br>安裝完 python3 後，安裝相關 python 套件

`pip install virtualenv` : 安裝virtualenv

`virtualenv env`  : 創建新環境

`activate` : 啟動安裝環境 *(至activate檔所在file)*

`pip list` : 顯示 pip 安裝目錄

`pip install -r requirements.txt` : 從requirements.txt安裝 site-pkg

* **安裝 MySQL 和 MySQLWorkbench**

1. 安裝完 MySQL 和 MySQLWorkbench 後，透過 Workbench 的 data import 功能，將 `db_replica.sql` 匯入至 MySQL 中，[教學網站在此](https://mnya.tw/cc/word/1395.html)
  

2. 需要在 /manager/config.py 中更改連線資料庫帳密和 IP address
  
`SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{IP address}:{port}/cloud_game_db"`

## 運行 Compal Cloud Gaming Manager
兩種方法
1. `activate` 啟動虛擬環境後，輸入 `python -m run.py `啟動 flask
2. 點擊 start.bat 程式自動進入 virualenv 並運行 flask

使用 MySQLWorkbench 檢視 schema 和資料
