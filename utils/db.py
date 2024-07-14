import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        db_exists = os.path.exists(self.db_name)
        self.conn = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        if not db_exists:
            print(f"Database file {self.db_name} not found. Creating new database and table.")
            self.create_table()
        else:
            print(f"Connected to existing database: {self.db_name}")

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcriptions (
            id INTEGER PRIMARY KEY,
            url TEXT,
            rawfile TEXT,
            convertedfile TEXT,
            transcribe TEXT,
            summazried TEXT,
            status TEXT,
            created TIMESTAMP
        )
        ''')
        self.conn.commit()
        print("Table 'transcriptions' created successfully.")

    def insert_record(self, url, rawfile, status, convertedfile=None, transcribe=None):
        created = datetime.now()
        self.cursor.execute('''
        INSERT INTO transcriptions (url, rawfile, convertedfile, transcribe, status, created)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (url, rawfile, convertedfile, transcribe, status, created))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_record_by_id(self, id):
        self.cursor.execute('SELECT * FROM transcriptions WHERE id = ?', (id,))
        return self.cursor.fetchone()

    def get_all_records(self):
        self.cursor.execute('SELECT * FROM transcriptions')
        return self.cursor.fetchall()
    
    def get_record_by_status(self, status):
        self.cursor.execute('SELECT * FROM transcriptions where status = ?',(status,))
        return self.cursor.fetchall()
    
    def url_is_exist(self,url):
        url = url.strip()
        pattern = f'%{url}%'
        print(pattern)
        self.cursor.execute('SELECT 1 FROM transcriptions where url like ?',(pattern,))
        return self.cursor.fetchone() is not None

    def update_record(self, id, status, url=None, rawfile=None, convertedfile=None, transcribe=None):
        update_fields = []
        values = []
        if url is not None:
            update_fields.append('url = ?')
            values.append(url)
        if rawfile is not None:
            update_fields.append('rawfile = ?')
            values.append(rawfile)
        if convertedfile is not None:
            update_fields.append('convertedfile = ?')
            values.append(convertedfile)
        if transcribe is not None:
            update_fields.append('transcribe = ?')
            values.append(transcribe)
        if status is not None:
            update_fields.append('status = ?')
            values.append(status)
        
        if not update_fields:
            return False

        query = f"UPDATE transcriptions SET {', '.join(update_fields)} WHERE id = ?"
        values.append(id)
        self.cursor.execute(query, tuple(values))
        self.conn.commit()
        return True
    
    def update_transcribe_text_by_id(self,id,transcribe):
        query = f"UPDATE transcriptions SET transcribe=?,status='TRANSCRIBED' WHERE id = ?"
        self.cursor.execute(query, ( transcribe,id,))
        self.conn.commit()
        return True
    
    def update_summarize_by_id(self, id, summarize):
        query = f"UPDATE transcriptions SET summarized=?,status='DONE' WHERE id = ?"
        self.cursor.execute(query, ( summarize,id,))
        self.conn.commit()
        return True
    
    def delete_record(self, id):
        self.cursor.execute('DELETE FROM transcriptions WHERE id = ?', (id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def __del__(self):
        if self.conn:
            self.conn.close()

# 使用示例
if __name__ == "__main__":
    db = DatabaseManager("transcriptions.db")

    # 插入记录
    # new_id = db.insert_record("http://example.com", "raw.mp3", "converted.wav", "Transcript text", "completed")
    # print(f"Inserted new record with ID: {new_id}")

    # 读取记录
    # record = db.get_record_by_id(1)
    # print(f"Retrieved record: {record}")

    # 更新记录
    # db.update_record(new_id, status="processing")
    # updated_record = db.get_record_by_id(new_id)
    # print(f"Updated record: {updated_record}")

    # 获取所有记录
    # all_records = db.get_all_records()
    # print(f"All records: {all_records}")

    # 删除记录
    # db.delete_record(new_id)
    # print(f"Deleted record with ID: {new_id}")
    
    
    # # 获取status为DOWNLOADED的一条数据
    # record = db.get_record_by_status('DOWNLOADED')
    # id,url = record[0:2]
    # print(f"{id}")
    
    # db.update_transcribe_text_by_id(2,transcribe="test db dao")
    # print(db.url_is_exist('https://www.youtube.com/watch?v=iuO2D5nz_AE'))
    