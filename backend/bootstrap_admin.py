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

def bootstrap_admin():
    db_url = get_db_url()
    if not db_url:
        print("DATABASE_URL not found")
        return

    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        print("Step 1: Ensuring admin user 'nara' exists...")
        # Check if 'nara' exists in users
        cur.execute("SELECT id, phone_no FROM users WHERE username='nara';")
        user = cur.fetchone()
        
        if not user:
            print("  Creating 'nara' user record...")
            cur.execute("""
                INSERT INTO users (username, password, phone_no, email) 
                VALUES ('nara', 'nara', '0000000000', 'admin@roottoreuse.com') 
                RETURNING id, phone_no;
            """)
            user = cur.fetchone()
        
        user_id, phone_no = user

        print("Step 2: Ensuring 'nara' is an Approved Volunteer...")
        cur.execute("SELECT id FROM volunteer WHERE username='nara';")
        volunteer = cur.fetchone()
        
        if not volunteer:
            print("  Creating approved volunteer record for 'nara'...")
            cur.execute("""
                INSERT INTO volunteer (full_name, username, user_phone, email, phone_no, skills, age, location, status) 
                VALUES ('Narayanan Admin', 'nara', %s, 'admin@roottoreuse.com', '0000000000', 'Admin, System Management', 30, 'Chennai', 'Approved')
            """, (phone_no,))
            print("  Admin volunteer record created.")
        else:
            print("  Ensuring admin volunteer is Approved...")
            cur.execute("UPDATE volunteer SET status='Approved' WHERE username='nara';")

        print("Successfully bootstrapped admin account 'nara'!")

        print("Step 3: Ensuring admin user 'demoadmin' exists...")
        # Check if 'demoadmin' exists in users
        cur.execute("SELECT id, phone_no FROM users WHERE username='demoadmin';")
        user_demo = cur.fetchone()
        
        if not user_demo:
            print("  Creating 'demoadmin' user record...")
            cur.execute("""
                INSERT INTO users (username, password, phone_no, email) 
                VALUES ('demoadmin', 'demoadmin', '0000000001', 'demo@roottoreuse.com') 
                RETURNING id, phone_no;
            """)
            user_demo = cur.fetchone()
        
        user_id_demo, phone_no_demo = user_demo

        print("Step 4: Ensuring 'demoadmin' is an Approved Volunteer...")
        cur.execute("SELECT id FROM volunteer WHERE username='demoadmin';")
        volunteer_demo = cur.fetchone()
        
        if not volunteer_demo:
            print("  Creating approved volunteer record for 'demoadmin'...")
            cur.execute("""
                INSERT INTO volunteer (full_name, username, user_phone, email, phone_no, skills, age, location, status) 
                VALUES ('Demo Admin', 'demoadmin', %s, 'demo@roottoreuse.com', '0000000001', 'Admin, Demo', 30, 'Chennai', 'Approved')
            """, (phone_no_demo,))
            print("  Demo Admin volunteer record created.")
        else:
            print("  Ensuring demo admin volunteer is Approved...")
            cur.execute("UPDATE volunteer SET status='Approved' WHERE username='demoadmin';")

        print("Successfully bootstrapped admin account 'demoadmin'!")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error during bootstrap: {e}")

if __name__ == "__main__":
    bootstrap_admin()
