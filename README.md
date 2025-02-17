# flask_newcomer

## Overview
The `flask_newcomer` project is designed as a simple educational tool for new employees learning the basics of Flask and database integration. This project is not intended for production use and requires additional security measures if deployed in a real-world environment.

### Prerequisites
Before running the project, ensure that the necessary Python libraries are installed. You can install them using the following command:

```bash
pip install flask flask_cors oracledb
```
#### Additional Notes
If you wish, you can modify db.py and related files to use a different database system instead of OracleDB. Adapt the connection logic and queries to fit your chosen database.

## Instructions

### db_conn.py
Complete the `db_conn.py` file with the necessary information to establish a connection to an Oracle database:
- `user`
- `password`
- `port`
- `service_name`
- `host`
- `dsn`

Make sure to securely manage sensitive information like `user` and `password`.

### db.py
Modify the `db.py` file to ensure that table names are not hardcoded. Currently, all queries use the table name `EMPLOYEES`. Update the logic to dynamically handle table names based on your application’s needs.

### main.py
Make the following updates to `main.py`:

#### Oracle Client Configuration
- The current code uses the thick mode of OracleDB:
  ```python
  oracledb.init_oracle_client()
  ```
  Ensure that the Oracle client is properly installed on your system for this to work.

#### CORS Policy
- The current implementation applies a very loose CORS policy, allowing all origins. This is not secure and should only be used for training purposes. If deploying in a production environment, update the CORS policy to restrict access to trusted origins.

#### Host Configuration
- The current code allows connections from all hosts using `host='0.0.0.0'`. This is also insecure for production use. Update the configuration to restrict access to specific trusted hosts if security is a priority.

### Additional Feature
If desired, you can create `templates/index.html` in the project root folder. The page will serve as a CRUD user interface for employee resources. This repository already includes an example `index.html` that you can use as a reference.
**Note**: The API base in this project is set to `http://host:port/employees`. If you want to use it for practical exercises with the included `index.html`, make sure to update the API base URL in the `index.html` file to match your environment.
## Notes
This project is meant for educational purposes only. Please review all configurations and implement appropriate security measures before using the code in a production environment.

---

Thank you for using `flask_newcomer`!
