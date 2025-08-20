import oracledb
import os
import paramiko
import pandas as pd

from datetime import date, datetime

from settings import DATA_FILE, APPOINTMENTS_FILE, DB_HOST, DB_USER, DB_NAME, DB_PASSWORD, SQL_FILE, SFTP_HOST, SFTP_USER, SFTP_PASSWORD

def database_connect():
    conn = oracledb.connect(
        user = DB_USER,
        password = DB_PASSWORD,
        dsn = f"{DB_HOST}:1521/{DB_NAME}"
    )
    return conn

def read_sql_file(filepath:str):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def read_db():
    conn = database_connect()
    cursor = conn.cursor()
    sql = read_sql_file(SQL_FILE)
    cursor.execute(sql)
    rows = cursor.fetchall()
    print("data fetch")
    return conn, cursor, rows

def set_columns(cursor):
    return [col[0] for col in cursor.description]

def set_file(df:pd.DataFrame):
    df.to_csv(APPOINTMENTS_FILE, sep=";", index=None)
    return

def add_locale_column(df:pd.DataFrame):
    df["locale"] = "BR"
    return df

def setup_birth_date(date:str):
    if date:
        date_obj = datetime.strptime(date, "%Y-%M-%d")
        return date_obj.strftime("%d-%M-%Y")

    return date

def setup_datetime(date:str, time:str):
    if date and time:
        return f"{date.replace("/", "-")} {time}"
    return date

def concat_region_code(phone:str):
    return f"+55{phone}"

def transform_data(columns, rows):
    df = pd.DataFrame(rows, columns=columns)
    df["DTAGENDA"] = df.apply(
        lambda row: setup_datetime(row["DTAGENDA"], row["HRAGENDA"]), axis=1)
    df.drop("HRAGENDA", axis=1, inplace=True)
    df["DTNASCIMENTO"] = df["DTNASCIMENTO"].apply(setup_birth_date)
    df["TELPACIENTE"] = df["TELPACIENTE"].apply(concat_region_code)
    df = add_locale_column(df)

    return df

def sftp_upload(filepath:str):
    transport = paramiko.Transport((SFTP_HOST, 22))
    transport.connect(None, SFTP_USER, SFTP_PASSWORD)

    with paramiko.SFTPClient.from_transport(transport) as conn:
        print("SFTP connection open")

        if not os.path.isfile(filepath):
            print(f"Local file does not exist:")
            return
        
        remote_filename = f"/Import/{DATA_FILE}".replace(".csv", f"_{str(date.today())}.csv")
        print(remote_filename, filepath)
        try:
            conn.put(filepath, remote_filename)
            print(f"{DATA_FILE} transferred to {remote_filename}")

        except Exception as error:
            print(f"Error transferring {DATA_FILE}: {error}")

def remove_files(filename:str):
    if not os.path.isfile(filename):
        return

    os.remove(filename)
    print('file removed')