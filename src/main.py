from settings import APPOINTMENTS_FILE
from utils import read_db, transform_data, set_columns, set_file, sftp_upload, remove_files

def main():
    conn, cursor, rows = read_db()
    columns = set_columns(cursor)

    df = transform_data(columns, rows)

    set_file(df)

    sftp_upload(APPOINTMENTS_FILE)

    cursor.close()
    conn.close()

    remove_files(APPOINTMENTS_FILE)
if __name__ == "__main__":
    main()
