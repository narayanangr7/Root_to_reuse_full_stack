import psycopg2
import os

def get_db_url():
    try:
        # Try different paths to find .env
        paths = ["backend/.env", ".env", "backend/backend/.env"]
        for path in paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    for line in f:
                        if "DATABASE_URL" in line:
                            # Handle potential quotes or spaces
                            val = line.split("=")[1].strip()
                            return val.strip("'").strip('"')
    except Exception as e:
        print(f"Error reading .env: {e}")
    return None

def fix_db():
    db_url = get_db_url()
    if not db_url:
        print("DATABASE_URL not found")
        return

    print("Connecting to database...")
    
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        print("Step 1: Dropping old volunteer table...")
        cur.execute("DROP TABLE IF EXISTS volunteer CASCADE;")

        print("Step 2: Altering users table types...")
        cur.execute("ALTER TABLE users ALTER COLUMN phone_no TYPE VARCHAR;")

        # Important: Foreign keys require UNIQUE constraints on referenced columns
        print("Step 3: Ensuring unique constraints on users table...")
        
        # Check for duplicates in phone_no
        cur.execute("SELECT phone_no, COUNT(*) FROM users GROUP BY phone_no HAVING COUNT(*) > 1;")
        dupes = cur.fetchall()
        if dupes:
            print(f"Found duplicate phone numbers: {dupes}. Cleaning up...")
            for phone, count in dupes:
                # Keep only one row for each duplicate phone number (simplistic cleanup)
                cur.execute("DELETE FROM users WHERE id NOT IN (SELECT MIN(id) FROM users GROUP BY phone_no);")

        # Now add the constraints properly
        try:
            cur.execute("ALTER TABLE users ADD CONSTRAINT unique_username UNIQUE (username);")
            print("  Created unique_username constraint.")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("  Unique username constraint already exists.")
            else:
                print(f"  Warning adding username constraint: {e}")

        try:
            cur.execute("ALTER TABLE users ADD CONSTRAINT unique_phone UNIQUE (phone_no);")
            print("  Created unique_phone constraint.")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("  Unique phone constraint already exists.")
            else:
                print(f"  Warning adding phone constraint: {e}")

        print("Step 4: Creating new volunteer table...")
        cur.execute("""
            CREATE TABLE volunteer (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR NOT NULL,
                username VARCHAR NOT NULL REFERENCES users(username) ON DELETE CASCADE,
                user_phone VARCHAR NOT NULL REFERENCES users(phone_no) ON DELETE CASCADE,
                email VARCHAR NOT NULL,
                phone_no VARCHAR NOT NULL,
                skills TEXT,
                age INTEGER NOT NULL,
                location VARCHAR NOT NULL,
                status VARCHAR DEFAULT 'Pending' NOT NULL
            );
        """)

        print("Step 5: Final touchups...")
        print("Successfully synchronized database schema for high-precision links!")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"FATAL ERROR during database sync: {e}")

if __name__ == "__main__":
    fix_db()
