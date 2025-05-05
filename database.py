import sqlite3
from contextlib import contextmanager
from datetime import datetime, time, timedelta

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect('hospital.db')
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def initialize_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Patients table with creation timestamp
        cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            age INTEGER CHECK(age > 0),
                            gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
                            diagnosis TEXT,
                            admission_date TEXT DEFAULT CURRENT_DATE,
                            created_at TEXT DEFAULT (datetime('now','localtime')))''')
        
        # Doctors table
        cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            specialization TEXT NOT NULL,
                            experience INTEGER CHECK(experience >= 0),
                            gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')))''')
        
        # Appointments table with time slots
        cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            patient_id INTEGER NOT NULL,
                            doctor_id INTEGER NOT NULL,
                            appointment_date TEXT NOT NULL,
                            start_time TEXT NOT NULL,
                            end_time TEXT NOT NULL,
                            notes TEXT,
                            created_at TEXT DEFAULT (datetime('now','localtime')),
                            FOREIGN KEY (patient_id) REFERENCES patients(id),
                            FOREIGN KEY (doctor_id) REFERENCES doctors(id))''')
        
        conn.commit()

# Patient Functions
def insert_patient(name, age, gender, diagnosis=""):
    """Insert a new patient record with validation"""
    if not name or not isinstance(age, int) or age <= 0:
        raise ValueError("Invalid patient data")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO patients (name, age, gender, diagnosis) 
                          VALUES (?, ?, ?, ?)''',
                      (name.strip(), age, gender.strip(), diagnosis.strip()))
        conn.commit()
        return cursor.lastrowid

def get_patients(search_term=None, search_by_id=False):
    """Get all patients or search by name/diagnosis/ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if search_term:
            if search_by_id:
                try:
                    patient_id = int(search_term)
                    cursor.execute('''SELECT * FROM patients 
                                     WHERE id = ? 
                                     ORDER BY name''', (patient_id,))
                except ValueError:
                    return []
            else:
                cursor.execute('''SELECT * FROM patients 
                                 WHERE name LIKE ? OR diagnosis LIKE ? 
                                 ORDER BY name''',
                             (f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM patients ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]

def update_patient(patient_id, name, age, gender, diagnosis):
    """Update patient record with validation"""
    if not name or not isinstance(age, int) or age <= 0:
        raise ValueError("Invalid patient data")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE patients 
                          SET name = ?, age = ?, gender = ?, diagnosis = ? 
                          WHERE id = ?''',
                      (name.strip(), age, gender.strip(), diagnosis.strip(), patient_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_patient(patient_id):
    """Delete a patient record"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        conn.commit()
        return cursor.rowcount > 0

# Doctor Functions
def insert_doctor(name, specialization, experience, gender):
    """Insert a new doctor record with validation"""
    if not name or not specialization or not isinstance(experience, int):
        raise ValueError("Invalid doctor data")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO doctors (name, specialization, experience, gender) 
                          VALUES (?, ?, ?, ?)''',
                      (name.strip(), specialization.strip(), experience, gender.strip()))
        conn.commit()
        return cursor.lastrowid

def get_doctors(search_term=None, search_by_id=False):
    """Get all doctors or search by name/specialization/ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if search_term:
            if search_by_id:
                try:
                    doctor_id = int(search_term)
                    cursor.execute('''SELECT * FROM doctors 
                                     WHERE id = ? 
                                     ORDER BY name''', (doctor_id,))
                except ValueError:
                    return []
            else:
                cursor.execute('''SELECT * FROM doctors 
                                 WHERE name LIKE ? OR specialization LIKE ? 
                                 ORDER BY name''',
                             (f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM doctors ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]

def update_doctor(doctor_id, name, specialization, experience, gender):
    """Update doctor record with validation"""
    if not name or not specialization or not isinstance(experience, int):
        raise ValueError("Invalid doctor data")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE doctors 
                          SET name = ?, specialization = ?, experience = ?, gender = ? 
                          WHERE id = ?''',
                      (name.strip(), specialization.strip(), experience, gender.strip(), doctor_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_doctor(doctor_id):
    """Delete a doctor record"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM doctors WHERE id = ?', (doctor_id,))
        conn.commit()
        return cursor.rowcount > 0

# Appointment Functions
def schedule_appointment(patient_id, doctor_id, appointment_date, start_time, end_time, notes=""):
    """Schedule a new appointment with time validation"""
    try:
        # Validate date and time format
        datetime.strptime(appointment_date, '%Y-%m-%d')
        time.fromisoformat(start_time)
        time.fromisoformat(end_time)
        
        # Check if time slot is available
        if not is_time_slot_available(doctor_id, appointment_date, start_time, end_time):
            raise ValueError("This time slot is already booked or invalid")
            
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO appointments 
                            (patient_id, doctor_id, appointment_date, start_time, end_time, notes) 
                            VALUES (?, ?, ?, ?, ?, ?)''',
                        (patient_id, doctor_id, appointment_date, start_time, end_time, notes))
            conn.commit()
            return cursor.lastrowid
    except ValueError as e:
        raise ValueError(str(e))

def is_time_slot_available(doctor_id, date, start_time, end_time):
    """Check if a time slot is available for a doctor"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM appointments 
                          WHERE doctor_id = ? AND appointment_date = ? 
                          AND (
                              (start_time < ? AND end_time > ?) OR
                              (start_time >= ? AND start_time < ?) OR
                              (end_time > ? AND end_time <= ?)
                          )''',
                     (doctor_id, date, end_time, start_time, 
                      start_time, end_time, start_time, end_time))
        return cursor.fetchone() is None

def get_available_time_slots(doctor_id, date, duration_minutes=30):
    """Get available time slots for a doctor on a specific date"""
    try:
        datetime.strptime(date, '%Y-%m-%d')  # Validate date format
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get doctor's working hours (default 9AM-5PM)
        work_start = time(9, 0)
        work_end = time(17, 0)
        
        # Get booked appointments
        cursor.execute('''SELECT start_time, end_time FROM appointments 
                          WHERE doctor_id = ? AND appointment_date = ?
                          ORDER BY start_time''',
                     (doctor_id, date))
        appointments = [(time.fromisoformat(row['start_time']), 
                        time.fromisoformat(row['end_time'])) 
                       for row in cursor.fetchall()]
        
        # Generate available slots
        available_slots = []
        current_time = work_start
        
        while current_time < work_end:
            slot_end = (datetime.combine(datetime.today(), current_time) + 
                       timedelta(minutes=duration_minutes)).time()
            
            if slot_end > work_end:
                break
                
            # Check if this slot is available
            slot_available = True
            for appt_start, appt_end in appointments:
                if not (current_time >= appt_end or slot_end <= appt_start):
                    slot_available = False
                    break
                    
            if slot_available:
                available_slots.append((
                    current_time.strftime('%H:%M'),
                    slot_end.strftime('%H:%M')
                ))
            
            current_time = slot_end
            
        return available_slots

def get_appointments(patient_id=None, doctor_id=None, date=None, search_term=None, search_by_id=False):
    """Get appointments with optional filters"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = '''SELECT a.*, p.name as patient_name, d.name as doctor_name 
                   FROM appointments a
                   JOIN patients p ON a.patient_id = p.id
                   JOIN doctors d ON a.doctor_id = d.id'''
        
        conditions = []
        params = []
        
        if patient_id:
            conditions.append("a.patient_id = ?")
            params.append(patient_id)
        if doctor_id:
            conditions.append("a.doctor_id = ?")
            params.append(doctor_id)
        if date:
            conditions.append("a.appointment_date = ?")
            params.append(date)
        if search_term:
            if search_by_id:
                try:
                    appointment_id = int(search_term)
                    conditions.append("a.id = ?")
                    params.append(appointment_id)
                except ValueError:
                    return []
            else:
                conditions.append("(p.name LIKE ? OR d.name LIKE ? OR a.notes LIKE ?)")
                params.extend([f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY a.appointment_date, a.start_time"
        cursor.execute(query, tuple(params))
        return [dict(row) for row in cursor.fetchall()]

def delete_appointment(appointment_id):
    """Delete an appointment"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_recent_activity(limit=5):
    """Get recent system activity"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get recent patients
        cursor.execute('''SELECT 'Patient' as type, name, created_at 
                          FROM patients 
                          ORDER BY created_at DESC 
                          LIMIT ?''', (limit,))
        patients = cursor.fetchall()
        
        # Get recent appointments
        cursor.execute('''SELECT 'Appointment' as type, 
                          p.name || ' with ' || d.name as description, 
                          a.created_at 
                          FROM appointments a
                          JOIN patients p ON a.patient_id = p.id
                          JOIN doctors d ON a.doctor_id = d.id
                          ORDER BY a.created_at DESC 
                          LIMIT ?''', (limit,))
        appointments = cursor.fetchall()
        
        # Combine and sort
        activity = patients + appointments
        activity.sort(key=lambda x: x['created_at'], reverse=True)
        return [dict(row) for row in activity[:limit]]

def get_patient_by_id(patient_id):
    """Get a single patient by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        result = cursor.fetchone()
        return dict(result) if result else None

def get_doctor_by_id(doctor_id):
    """Get a single doctor by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        result = cursor.fetchone()
        return dict(result) if result else None

def get_appointment_by_id(appointment_id):
    """Get a single appointment by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT a.*, p.name as patient_name, d.name as doctor_name 
                       FROM appointments a
                       JOIN patients p ON a.patient_id = p.id
                       JOIN doctors d ON a.doctor_id = d.id
                       WHERE a.id = ?''', (appointment_id,))
        result = cursor.fetchone()
        return dict(result) if result else None

def get_patient_appointments(patient_id):
    """Get all appointments for a specific patient"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT a.*, d.name as doctor_name, d.specialization 
                       FROM appointments a
                       JOIN doctors d ON a.doctor_id = d.id
                       WHERE a.patient_id = ?
                       ORDER BY a.appointment_date, a.start_time''', (patient_id,))
        return [dict(row) for row in cursor.fetchall()]
    
# Initialize the database
initialize_database()