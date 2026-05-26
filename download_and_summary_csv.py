import csv
import urllib.request
import ssl

# 1. 設定新北市政府開放資料 API 網址
url = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"

try:
    # 2. 忽略 SSL 憑證檢查
    context = ssl._create_unverified_context()
    
    # 3. 發送 Header 請求並讀取網路 CSV 資料
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=context) as response:
        # 使用 utf-8-sig 可以自動移除檔案開頭可能存在的 BOM 隱藏字元
        html_content = response.read().decode('utf-8-sig')
        
        # 4. 解析 CSV 內容
        lines = html_content.strip().split('\n')
        csv_data = list(csv.reader(lines))
        
        # 取得標題列與資料列
        header = [col.strip() for col in csv_data[0]] # 移除欄位名稱前後的空白
        records = csv_data[1:]
        
        # 預設索引位置（若找不到欄位時的安全安全防護）
        idx_title = 0
        idx_type = 1
        idx_start = 2
        idx_end = 3
        idx_pub = 4
        idx_link = 5
        idx_desc = 6
        
        # 動態尋找欄位，包含關鍵字即可，避免完全比對出錯
        for i, col_name in enumerate(header):
            if "標題" in col_name: idx_title = i
            elif "類型" in col_name: idx_type = i
            elif "開始日期" in col_name: idx_start = i
            elif "結束日期" in col_name: idx_end = i
            elif "發佈時間" in col_name or "發布時間" in col_name: idx_pub = i
            elif "連結" in col_name: idx_link = i
            elif "簡介" in col_name: idx_desc = i

        # 5. 依序顯示所有資料項目
        for index, row in enumerate(records, start=1):
            if len(row) < len(header):
                continue
                
            print(f"==== 第{index}筆資料 ====")
            print(f"【標題】 {row[idx_title]}")
            print(f"【類型】 {row[idx_type]}")
            print(f"【開始日期】 {row[idx_start]}")
            print(f"【結束日期】 {row[idx_end]}")
            print(f"【發佈時間】 {row[idx_pub]}")
            print(f"【連結】 {row[idx_link]}")
            print(f"【簡介】 {row[idx_desc]}")
            print() # 輸出空白行以區隔每筆資料

except Exception as e:
    print(f"程式執行發生錯誤: {e}")