
import cryptocode
import pandas as pd
from sqlalchemy import create_engine, text
from logger import log
from sqlalchemy import text
import winreg

# A rendszerváltozók registry kulcsa


class cl_DataBase_main:
    def __init__(self,  sid):
        key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        try:
            # HKEY_LOCAL_MACHINE gyökérkulcs megnyitása
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                # DB_NAME változó lekérése
                database, reg_type = winreg.QueryValueEx(key, "DB_DATABASE")
                driver, reg_type = winreg.QueryValueEx(key, "DB_DRIVER")
                pwd, reg_type = winreg.QueryValueEx(key, "DB_PWD")
                user, reg_type = winreg.QueryValueEx(key, "DB_USER")
                print(database,driver,pwd,user)
        except Exception as e:
            pass
        self.sid = sid
        self.db_local = database
        self.db_driver=driver
        self.db_pwd=pwd
        self.db_user=user
        self.engine = None
        self.connection = None
        log.info(f"Initializing database    -    PY[{__name__}] SID[{self.sid}] {self} {database}")

    def __enter__(self):
        try:
            connstr =  f"mssql+pyodbc://{self.db_user}:{cryptocode.decrypt(self.db_pwd,'fika?')}@{self.db_local}/procy_obk?driver={self.db_driver}"
            self.engine = create_engine(connstr)
            self.connection = self.engine.connect()
            log.info(f"Entered database -   PY[{__name__}] SID[{self.sid}] {self.engine} {self.db_local}")
        except Exception as e:
            log.error(f"Entered database    -   PY[{__name__}] SID[{self.sid}] MSG[{str(e)}]")
        return self

    def __exit__(self, exception_type, exception_val, trace):
        try:
            if self.connection:
                self.connection.close()
            if self.engine:
                self.engine.dispose()
            log.info(f"Exit database    -   PY[{__name__}] SID[{self.sid}]")
        except Exception as e:
            log.error(f"Exit database   -   PY[{__name__}] SID[{self.sid}] MSG[{str(e)}]")


    def execute_query(self, query, params=None):
        """Biztonságos SQL lekérdezés végrehajtása paraméterezett lekérdezéssel."""
        try:
            if params:
                result = self.connection.execute(text(query), params)
            else:
                result = self.connection.execute(text(query))
            
            # INSERT/UPDATE/DELETE esetén commit és visszatérünk a sorok számával
            if query.strip().lower().startswith(("insert", "update", "delete")):
                self.connection.commit()
                return result.rowcount
            # SELECT esetén visszatérünk az eredménnyel
            else:
                return result.fetchall()
        except Exception as e:
            log.error(f"Query execution error   -   SID[{self.sid}] MSG[{str(e)}]")
            self.connection.rollback()
            raise

    def insert_data(self, table_name, data):
       """Adatok beszúrása egy táblába."""
       try:
           # Mezők és értékek kinyerése
           columns = ", ".join(data.keys())
           placeholders = ", ".join([f":{key}" for key in data.keys()])
           # SQL lekérdezés összeállítása
           query = text(f"INSERT INTO [{table_name}] ({columns}) VALUES ({placeholders})")
           # Lekérdezés végrehajtása paraméterekkel
           result = self.connection.execute(query, data)
           self.connection.commit()
           return result.rowcount
       except Exception as e:
           log.error(f"Insert error   -   SID[{self.sid}] MSG[{str(e)}]")
           self.connection.rollback()
           raise           
    