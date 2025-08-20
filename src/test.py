import oracledb

conn = oracledb.connect(
    user="sysmiddle",
    password="sysmiddle@opty",
    dsn="10.102.0.21:1521/desen"
)

print("connection stablished")
conn.close()