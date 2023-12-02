import pandas as pd
import re

# 檔案路徑
file_path = 'final_output.txt'

# 讀取檔案內容
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# 分隔每個案件，每個案件由雙換行符（\n\n）分隔
cases = file_content.split('\n\n')

# 正則表達式模式
url_pattern = r'此案網址:\s*(https?://[^\s]+)'
date_pattern = r'(\d{4}-\d{2}-\d{2})'

# 處理每個案件以提取所需信息
extracted_cases = []
for case in cases:
    # 提取 URL 和日期
    url_match = re.search(url_pattern, case)
    date_match = re.search(date_pattern, case)

    if url_match and date_match:
        url = url_match.group(0)
        date = date_match.group(0)
        # 從案件內容中移除 URL 部分
        case_modified = case.replace(url, '').strip()
        extracted_cases.append((date, url, case_modified))

# 創建 DataFrame
df_modified = pd.DataFrame(extracted_cases, columns=['更新日期', '此案網址', '案件內容'])

# 保存為 Excel 檔案
excel_file_path_modified = 'converted_data.xlsx'
df_modified.to_excel(excel_file_path_modified, index=False)
