import oracledb
from enum import Enum
from db_conn import user, password, dsn

class Task(Enum):
    CREATE = 1
    READ = 2
    UPDATE = 3
    DELETE = 4

class Request:
  def __init__(self, body: dict = {}, params: dict = {}):
    self.body = body
    self.params = params

class DB:
    def __init__(self, task: Task, req: Request):
        self.task = task
        self.req_params = req.params
        self.body = req.body
        self.conn = oracledb.connect(user=user, password=password, dsn=dsn)
        self.cursor = self.conn.cursor()
        self.oracledb_params = []
        print('db instance init')

    def getQuery(self):
        print(f'getQuery: {self.task}, {self.body if self.body else ""} {self.req_params if self.req_params else ""}')
        if self.task == Task.CREATE:
            columns = ', '.join(list(self.body.keys()))
            placeholders = ', '.join([':' + str(i + 1) for i in range(len(self.body.values()))])
            self.oracledb_params = [self.body[k] for k in self.body.keys()]
            return f"INSERT INTO EMPLOYEES ({columns}) VALUES ({placeholders})"

        elif self.task == Task.READ:
            query = "SELECT * FROM EMPLOYEES"
            if self.req_params:
                where_clauses = []
                for i, key in enumerate(self.req_params.keys()):
                  where_clauses.append(f"{key} = :{i + 1}")
                  self.oracledb_params.append(self.req_params[key])
                query += " WHERE " + " AND ".join(where_clauses)
            return query

        elif self.task == Task.UPDATE:
            body_keys = self.body.keys()
            set_clauses = []
            for i, key in enumerate(body_keys):
              set_clauses.append(f"{key} = :{i + 1}")
              self.oracledb_params.append(self.body[key])
            query = "UPDATE EMPLOYEES SET " + ", ".join(set_clauses)
            if self.req_params:
                where_clauses = []
                offset = len(self.oracledb_params)
                for i, key in enumerate(self.req_params.keys()):
                  where_clauses.append(f"{key} = :{i + offset}")
                  self.oracledb_params.append(self.req_params[key])
                query += " WHERE " + " AND ".join(where_clauses)
            return query

        elif self.task == Task.DELETE:
            query = "DELETE FROM EMPLOYEES"
            if self.req_params:
                where_clauses = []
                for i, key in enumerate(self.req_params.keys()):
                  where_clauses.append(f"{key} = :{i + 1}")
                  self.oracledb_params.append(self.req_params[key])
                query += " WHERE " + " AND ".join(where_clauses)
            return query

    def execute(self):
        try:
            query = self.getQuery()
            print(query)
            self.cursor.execute(query, self.oracledb_params)

            if self.task == Task.READ:
                result = self.cursor.fetchall()
                # Convert rows to JSON-like format
                columns = [col[0] for col in self.cursor.description]
                if result:
                    result_json = [dict(zip(columns, row)) for row in result]
                else:
                    result_json = []
                return {"success": True, "data": result_json}

            else:
                # Commit changes for non-SELECT queries
                self.conn.commit()
                return {"success": True, "message": "Query executed successfully."}

        except Exception as e:
            return {"success": False, "error": str(e)}

        finally:
            self.cursor.close()
            self.conn.close()
