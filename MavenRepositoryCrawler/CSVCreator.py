import csv
# 開啟輸出的 CSV 檔案

class CSVCreator:

    def __init__(self, filename):
        if not filename.endswith(".csv"):
            filename = filename + '.csv'

        self.filename = filename

    def add_header(self, header):
        with open(self.filename, 'a', newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

    def save_data(self, project_meta_data):
        with open(self.filename, 'a', newline='', encoding='UTF-8') as csvfile:
            # 建立 CSV 檔寫入器
            writer = csv.writer(csvfile)

            for data in project_meta_data:
              row = list(data)
              writer.writerow(row)
