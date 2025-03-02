import sqlite3
import hashlib
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name='dashboard.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            is_validated BOOLEAN NOT NULL DEFAULT 0
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            location TEXT NOT NULL,
            installation_date TEXT NOT NULL,
            maintenance_frequency INTEGER NOT NULL,
            last_maintenance_date TEXT,
            status TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_history (
            id INTEGER PRIMARY KEY,
            machine_id INTEGER,
            maintenance_date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines (id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            description TEXT,
            event_type TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY,
            machine_id INTEGER,
            inspection_date TEXT NOT NULL,
            inspector TEXT NOT NULL,
            result TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines (id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            status TEXT NOT NULL,
            location TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_orders (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            assigned_to INTEGER,
            due_date TEXT,
            FOREIGN KEY (assigned_to) REFERENCES users (id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit TEXT NOT NULL,
            reorder_level INTEGER NOT NULL
        )
        ''')

        self.conn.commit()

    def add_user(self, username, password, role):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                (username, hashed_password, role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_user(self, user_id):
        self.cursor.execute("UPDATE users SET is_validated = 1 WHERE id = ?", (user_id,))
        self.conn.commit()

    def authenticate_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = self.cursor.fetchone()
        if user and user[4]:  # Check if user exists and is validated
            return user
        return None

    def get_users(self):
        self.cursor.execute("SELECT id, username, role, is_validated FROM users")
        return self.cursor.fetchall()

    def add_machine(self, name, machine_type, location, installation_date, maintenance_frequency):
        self.cursor.execute('''
        INSERT INTO machines (name, type, location, installation_date, maintenance_frequency, status)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, machine_type, location, installation_date, maintenance_frequency, 'Healthy'))
        self.conn.commit()

    def get_machines(self):
        self.cursor.execute("SELECT * FROM machines")
        return self.cursor.fetchall()

    def update_machine_status(self, machine_id, status):
        self.cursor.execute("UPDATE machines SET status = ? WHERE id = ?", (status, machine_id))
        self.conn.commit()

    def add_maintenance(self, machine_id, description):
        current_date = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('''
        INSERT INTO maintenance_history (machine_id, maintenance_date, description)
        VALUES (?, ?, ?)
        ''', (machine_id, current_date, description))
        self.cursor.execute("UPDATE machines SET last_maintenance_date = ? WHERE id = ?", (current_date, machine_id))
        self.conn.commit()

    def get_maintenance_history(self, machine_id):
        self.cursor.execute("SELECT * FROM maintenance_history WHERE machine_id = ?", (machine_id,))
        return self.cursor.fetchall()

    def add_calendar_event(self, title, start_date, end_date, description, event_type):
        self.cursor.execute('''
        INSERT INTO calendar_events (title, start_date, end_date, description, event_type)
        VALUES (?, ?, ?, ?, ?)
        ''', (title, start_date, end_date, description, event_type))
        self.conn.commit()

    def get_calendar_events(self, start_date, end_date):
        self.cursor.execute('''
        SELECT * FROM calendar_events
        WHERE start_date >= ? AND end_date <= ?
        ''', (start_date, end_date))
        return self.cursor.fetchall()

    def add_inspection(self, machine_id, inspection_date, inspector, result, notes):
        self.cursor.execute('''
        INSERT INTO inspections (machine_id, inspection_date, inspector, result, notes)
        VALUES (?, ?, ?, ?, ?)
        ''', (machine_id, inspection_date, inspector, result, notes))
        self.conn.commit()

    def get_inspections(self, machine_id=None):
        if machine_id:
            self.cursor.execute('SELECT * FROM inspections WHERE machine_id = ?', (machine_id,))
        else:
            self.cursor.execute('SELECT * FROM inspections')
        return self.cursor.fetchall()

    def add_resource(self, name, type, status, location):
        self.cursor.execute('''
        INSERT INTO resources (name, type, status, location)
        VALUES (?, ?, ?, ?)
        ''', (name, type, status, location))
        self.conn.commit()

    def get_resources(self):
        self.cursor.execute('SELECT * FROM resources')
        return self.cursor.fetchall()

    def add_work_order(self, title, description, status, priority, assigned_to, due_date):
        self.cursor.execute('''
        INSERT INTO work_orders (title, description, status, priority, assigned_to, due_date)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, status, priority, assigned_to, due_date))
        self.conn.commit()

    def get_work_orders(self):
        self.cursor.execute('SELECT * FROM work_orders')
        return self.cursor.fetchall()

    def add_inventory_item(self, item_name, quantity, unit, reorder_level):
        self.cursor.execute('''
        INSERT INTO inventory (item_name, quantity, unit, reorder_level)
        VALUES (?, ?, ?, ?)
        ''', (item_name, quantity, unit, reorder_level))
        self.conn.commit()

    def get_inventory(self):
        self.cursor.execute('SELECT * FROM inventory')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

