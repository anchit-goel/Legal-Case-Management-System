from db import test_connection

if __name__ == "__main__":
    ok, ver = test_connection()
    if ok:
        print(f"SQLite OK (version: {ver})")
    else:
        print("SQLite connection failed")
