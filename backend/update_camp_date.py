import psycopg2
import os

def get_db_url():
    paths = ["backend/.env", ".env", "backend/backend/.env"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    if "DATABASE_URL" in line:
                        val = line.split("=")[1].strip()
                        return val.strip("'").strip('"')
    return None

def update_camp_table():
    db_url = get_db_url()
    if not db_url:
        print("DATABASE_URL not found")
        return

    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        print("Updating camp table structure...")
        
        # Check if event_date column exists
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='camp' AND column_name='event_date';")
        if not cur.fetchone():
            print("Adding 'event_date' column to camp table...")
            # We use a default value to avoid errors with existing rows
            cur.execute("ALTER TABLE camp ADD COLUMN event_date VARCHAR DEFAULT '2025-01-01' NOT NULL;")
        
        print("Successfully updated camp table schema with dates!")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_camp_table()
