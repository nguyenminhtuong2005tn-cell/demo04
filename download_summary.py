import csv
import json
import ssl
import urllib.error
import urllib.request
from flask import Flask, jsonify, render_template

# 初始化 Flask 應用程式
app = Flask(__name__)

@app.route('/')
def home():
    # 設定新北市政府開放資料 API 網址
    url = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"
    
    data_list = []
    
    try:
        # 建立忽略 SSL 憑證檢查 COMNTEXT，修復 CERTIFICATE_VERIFY_FAILED 錯誤
        context = ssl._create_unverified_context()
        
        # 模擬瀏覽器發送請求下載網路 CSV 資料
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=context) as response:
            # 讀取並使用 utf-8-sig 解碼，自動移除可能引發錯誤的 BOM 隱藏字元
            html_content = response.read().decode('utf-8-sig')
            
            # 解析 CSV 內容
            lines = html_content.strip().split('\n')
            csv_data = list(csv.reader(lines))
            
            # 取得並清理標題列
            header = [col.strip() for col in csv_data[0]]
            records = csv_data[1:]
            
            # 預設欄位索引位置（安全防護機制）
            idx_title = 0
            idx_type = 1
            idx_start = 2
            idx_end = 3
            idx_pub = 4
            idx_link = 5
            idx_desc = 6
            
            # 遍歷標題列，動態對應欄位名稱的正確位置
            for i, col_name in enumerate(header):
                if "標題" in col_name: idx_title = i
                elif "類型" in col_name: idx_type = i
                elif "開始日期" in col_name: idx_start = i
                elif "結束日期" in col_name: idx_end = i
                elif "發佈時間" in col_name or "發布時間" in col_name: idx_pub = i
                elif "連結" in col_name: idx_link = i
                elif "簡介" in col_name: idx_desc = i

            # 將所有資料列整理成網頁範本需要的字典列表
            for row in records:
                if len(row) < len(header):
                    continue
                data_list.append({
                    "title": row[idx_title],
                    "type": row[idx_type],
                    "start_date": row[idx_start],
                    "end_date": row[idx_end],
                    "publish_time": row[idx_pub],
                    "link": row[idx_link],
                    "desc": row[idx_desc]
                })
                
    except Exception as e:
        print(f"網頁伺服器處理資料時發生錯誤: {e}")
        
    # 將資料傳遞給 templates/index.html 進行網頁內容渲染
    return render_template('index.html', data_list=data_list)

if __name__ == '__main__':
    # 啟動本地端網頁伺服器，使用通用的 Port 5000
    app.run(debug=True, port=5000)