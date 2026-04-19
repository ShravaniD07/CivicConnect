from flask import Flask, render_template, request, redirect, session
from flask_mail import Mail, Message
from db import get_connection
from datetime import date

app = Flask(__name__)
app.secret_key = "civic_secret_key_2024"

# EMAIL CONFIGURATION
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'civicconnect.people@gmail.com'
app.config['MAIL_PASSWORD'] = 'czutginuscrdpnml'
app.config['MAIL_DEFAULT_SENDER'] = 'civicconnect.people@gmail.com'

mail = Mail(app)


# ─────────────────────────────────────────
# EMAIL HELPERS
# ─────────────────────────────────────────
def send_welcome_email(to_email, name):
    try:
        print(f"Trying welcome email to: {to_email}")
        msg = Message(
            subject='Welcome to CivicConnect',
            recipients=[to_email]
        )
        msg.body = f"""
Hello {name},

Welcome to CivicConnect.

Your citizen account has been successfully registered.
You can now log in and report civic issues such as potholes, water leakage, electricity complaints, sanitation issues, and park maintenance problems.

Thank you,
CivicConnect Team
"""
        mail.send(msg)
        print("Welcome email sent successfully.")
    except Exception as e:
        print("Welcome email failed:", repr(e))


def send_complaint_registered_email(to_email, name, complaint_id, title, status):
    try:
        print(f"Trying complaint registration email to: {to_email}")
        msg = Message(
            subject=f'Complaint #{complaint_id} Registered Successfully',
            recipients=[to_email]
        )
        msg.body = f"""
Hello {name},

Your complaint has been registered successfully.

Complaint ID: {complaint_id}
Title: {title}
Current Status: {status}

You can log in to CivicConnect and track the progress of your complaint.

Thank you,
CivicConnect Team
"""
        mail.send(msg)
        print("Complaint registration email sent successfully.")
    except Exception as e:
        print("Complaint registration email failed:", repr(e))


def send_status_update_email(to_email, name, complaint_id, status, message):
    try:
        print(f"Trying status update email to: {to_email}")
        msg = Message(
            subject=f'Complaint #{complaint_id} Status Updated',
            recipients=[to_email]
        )
        msg.body = f"""
Hello {name},

Your complaint status has been updated.

Complaint ID: {complaint_id}
New Status: {status}
Update Message: {message}

Please log in to CivicConnect to view more details.

Thank you,
CivicConnect Team
"""
        mail.send(msg)
        print("Status update email sent successfully.")
    except Exception as e:
        print("Status update email failed:", repr(e))


# ─────────────────────────────────────────
# HOME
# ─────────────────────────────────────────
@app.route('/')
def home():
    return redirect('/login')


# ─────────────────────────────────────────
# CITIZEN AUTH
# ─────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']

        con = get_connection()
        cur = con.cursor()

        try:
            cur.execute("""
                INSERT INTO Citizen (Name, Email, Phone, Address, Password)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, phone, address, password))
            con.commit()
            con.close()

            print("User registered successfully in DB.")
            send_welcome_email(email, name)

            return redirect('/login')
        except Exception as e:
            con.close()
            print("Register failed:", repr(e))
            return render_template('register.html', error="Email already registered.")

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        con = get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM Citizen WHERE Email=%s AND Password=%s",
            (email, password)
        )
        user = cur.fetchone()
        con.close()

        if user:
            session['citizen_id'] = user['Citizen_ID']
            session['citizen_name'] = user['Name']
            return redirect('/dashboard')

        return render_template('login.html', error="Invalid email or password.")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ─────────────────────────────────────────
# CITIZEN DASHBOARD
# ─────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'citizen_id' not in session:
        return redirect('/login')

    con = get_connection()
    cur = con.cursor(dictionary=True)

    status = request.args.get('status', '').strip()
    category = request.args.get('category', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    query = """
        SELECT c.Complaint_ID, c.Title, c.Location, c.Status, c.Date_Submitted,
               co.Option_Name, co.Priority, cat.Category_Name,
               d.Department_Name
        FROM Complaint c
        LEFT JOIN Complaint_Option co ON c.Option_ID = co.Option_ID
        LEFT JOIN Category cat ON co.Category_ID = cat.Category_ID
        LEFT JOIN Department d ON c.Department_ID = d.Department_ID
        WHERE c.Citizen_ID = %s
    """
    params = [session['citizen_id']]

    if status:
        query += " AND c.Status = %s"
        params.append(status)

    if category:
        query += " AND cat.Category_Name = %s"
        params.append(category)

    if date_from:
        query += " AND c.Date_Submitted >= %s"
        params.append(date_from)

    if date_to:
        query += " AND c.Date_Submitted <= %s"
        params.append(date_to)

    query += " ORDER BY c.Date_Submitted DESC"

    cur.execute(query, tuple(params))
    complaints = cur.fetchall()

    total = len(complaints)
    pending = sum(1 for c in complaints if c['Status'] == 'Pending')
    progress = sum(1 for c in complaints if c['Status'] == 'In Progress')
    resolved = sum(1 for c in complaints if c['Status'] == 'Resolved')

    cur.execute("SELECT Category_Name FROM Category ORDER BY Category_Name")
    categories = cur.fetchall()

    con.close()

    return render_template(
        'dashboard.html',
        complaints=complaints,
        total=total,
        pending=pending,
        progress=progress,
        resolved=resolved,
        categories=categories,
        selected_status=status,
        selected_category=category,
        selected_date_from=date_from,
        selected_date_to=date_to
    )


# ─────────────────────────────────────────
# REPORT COMPLAINT
# ─────────────────────────────────────────
@app.route('/report', methods=['GET', 'POST'])
def report_complaint():
    if 'citizen_id' not in session:
        return redirect('/login')

    con = get_connection()
    cur = con.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        option_id = request.form['option_id']

        cur.execute("""
            INSERT INTO Complaint
            (Citizen_ID, Option_ID, Title, Description, Location, Date_Submitted, Status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
        """, (
            session['citizen_id'],
            option_id,
            title,
            description,
            location,
            date.today()
        ))

        complaint_id = cur.lastrowid

        cur.execute("""
            INSERT INTO Complaint_Update
            (Complaint_ID, Update_Message, Update_Date, Status)
            VALUES (%s, %s, %s, %s)
        """, (
            complaint_id,
            'Complaint submitted by citizen.',
            date.today(),
            'Pending'
        ))

        cur.execute("""
            SELECT Name, Email
            FROM Citizen
            WHERE Citizen_ID = %s
        """, (session['citizen_id'],))
        citizen = cur.fetchone()

        con.commit()
        con.close()

        if citizen and citizen.get('Email'):
            send_complaint_registered_email(
                citizen['Email'],
                citizen['Name'],
                complaint_id,
                title,
                'Pending'
            )

        return redirect('/dashboard')

    cur.execute("SELECT * FROM Category ORDER BY Category_Name")
    categories = cur.fetchall()

    cur.execute("""
        SELECT co.Option_ID,
               co.Option_Name,
               co.Priority,
               co.Category_ID,
               cat.Category_Name
        FROM Complaint_Option co
        JOIN Category cat ON co.Category_ID = cat.Category_ID
        ORDER BY co.Option_Name
    """)
    options = cur.fetchall()

    con.close()

    return render_template(
        'report_complaint.html',
        categories=categories,
        options=options
    )


# ─────────────────────────────────────────
# COMPLAINT DETAIL + TIMELINE
# ─────────────────────────────────────────
@app.route('/complaint/<int:complaint_id>')
def complaint_detail(complaint_id):
    if 'citizen_id' not in session:
        return redirect('/login')

    con = get_connection()
    cur = con.cursor(dictionary=True)

    cur.execute("""
        SELECT c.*, co.Option_Name, co.Priority, cat.Category_Name,
               d.Department_Name, e.Name AS Employee_Name
        FROM Complaint c
        LEFT JOIN Complaint_Option co ON c.Option_ID = co.Option_ID
        LEFT JOIN Category cat ON co.Category_ID = cat.Category_ID
        LEFT JOIN Department d ON c.Department_ID = d.Department_ID
        LEFT JOIN Employee e ON c.Employee_ID = e.Employee_ID
        WHERE c.Complaint_ID = %s AND c.Citizen_ID = %s
    """, (complaint_id, session['citizen_id']))
    complaint = cur.fetchone()

    cur.execute("""
        SELECT * FROM Complaint_Update
        WHERE Complaint_ID = %s
        ORDER BY Update_Date ASC
    """, (complaint_id,))
    updates = cur.fetchall()

    cur.execute("""
        SELECT * FROM Feedback
        WHERE Complaint_ID = %s AND Citizen_ID = %s
    """, (complaint_id, session['citizen_id']))
    feedback = cur.fetchone()

    con.close()

    if not complaint:
        return redirect('/dashboard')

    return render_template(
        'complaint_detail.html',
        complaint=complaint,
        updates=updates,
        feedback=feedback
    )


@app.route('/feedback/<int:complaint_id>', methods=['POST'])
def submit_feedback(complaint_id):
    if 'citizen_id' not in session:
        return redirect('/login')

    rating = request.form['rating']
    comments = request.form['comments']

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO Feedback (Complaint_ID, Citizen_ID, Rating, Comments, Feedback_Date)
        VALUES (%s, %s, %s, %s, %s)
    """, (complaint_id, session['citizen_id'], rating, comments, date.today()))

    con.commit()
    con.close()

    return redirect(f'/complaint/{complaint_id}')


# ─────────────────────────────────────────
# ADMIN AUTH
# ─────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect('/admin/dashboard')
        return render_template('admin/admin_login.html', error="Invalid credentials.")

    return render_template('admin/admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin/login')


# ─────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin/login')

    con = get_connection()
    cur = con.cursor(dictionary=True)

    status = request.args.get('status', '').strip()
    category = request.args.get('category', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    department = request.args.get('department', '').strip()

    query = """
        SELECT c.Complaint_ID, c.Title, c.Status, c.Date_Submitted,
               ci.Name AS Citizen_Name, co.Priority,
               cat.Category_Name, d.Department_Name
        FROM Complaint c
        LEFT JOIN Citizen ci ON c.Citizen_ID = ci.Citizen_ID
        LEFT JOIN Complaint_Option co ON c.Option_ID = co.Option_ID
        LEFT JOIN Category cat ON co.Category_ID = cat.Category_ID
        LEFT JOIN Department d ON c.Department_ID = d.Department_ID
        WHERE 1=1
    """
    params = []

    if status:
        query += " AND c.Status = %s"
        params.append(status)

    if category:
        query += " AND cat.Category_Name = %s"
        params.append(category)

    if department:
        query += " AND d.Department_Name = %s"
        params.append(department)

    if date_from:
        query += " AND c.Date_Submitted >= %s"
        params.append(date_from)

    if date_to:
        query += " AND c.Date_Submitted <= %s"
        params.append(date_to)

    query += " ORDER BY c.Date_Submitted DESC"

    cur.execute(query, tuple(params))
    complaints = cur.fetchall()

    total = len(complaints)
    pending = sum(1 for c in complaints if c['Status'] == 'Pending')
    progress = sum(1 for c in complaints if c['Status'] == 'In Progress')
    resolved = sum(1 for c in complaints if c['Status'] == 'Resolved')

    cur.execute("SELECT Category_Name FROM Category ORDER BY Category_Name")
    categories = cur.fetchall()

    cur.execute("SELECT Department_Name FROM Department ORDER BY Department_Name")
    departments = cur.fetchall()

    con.close()

    return render_template(
        'admin/manage_complaints.html',
        complaints=complaints,
        total=total,
        pending=pending,
        progress=progress,
        resolved=resolved,
        categories=categories,
        departments=departments,
        selected_status=status,
        selected_category=category,
        selected_department=department,
        selected_date_from=date_from,
        selected_date_to=date_to
    )


# ─────────────────────────────────────────
# ADMIN UPDATE COMPLAINT
# ─────────────────────────────────────────
@app.route('/admin/update/<int:complaint_id>', methods=['GET', 'POST'])
def update_complaint(complaint_id):
    if not session.get('admin'):
        return redirect('/admin/login')

    con = get_connection()
    cur = con.cursor(dictionary=True)

    if request.method == 'POST':
        dept_id = request.form['dept_id']
        emp_id = request.form['emp_id']
        status = request.form['status']
        message = request.form['message']

        cur.execute("""
            UPDATE Complaint
            SET Department_ID = %s, Employee_ID = %s, Status = %s
            WHERE Complaint_ID = %s
        """, (dept_id, emp_id, status, complaint_id))

        cur.execute("""
            INSERT INTO Complaint_Update (Complaint_ID, Update_Message, Update_Date, Status)
            VALUES (%s, %s, %s, %s)
        """, (complaint_id, message, date.today(), status))

        cur.execute("""
            SELECT ci.Name, ci.Email, c.Title
            FROM Complaint c
            JOIN Citizen ci ON c.Citizen_ID = ci.Citizen_ID
            WHERE c.Complaint_ID = %s
        """, (complaint_id,))
        citizen = cur.fetchone()

        con.commit()
        con.close()

        if citizen and citizen.get('Email'):
            send_status_update_email(
                citizen['Email'],
                citizen['Name'],
                complaint_id,
                status,
                message
            )

        return redirect('/admin/dashboard')

    cur.execute("""
        SELECT c.*, co.Option_Name, ci.Name AS Citizen_Name, cat.Category_Name
        FROM Complaint c
        LEFT JOIN Complaint_Option co ON c.Option_ID = co.Option_ID
        LEFT JOIN Citizen ci ON c.Citizen_ID = ci.Citizen_ID
        LEFT JOIN Category cat ON co.Category_ID = cat.Category_ID
        WHERE c.Complaint_ID = %s
    """, (complaint_id,))
    complaint = cur.fetchone()

    cur.execute("SELECT * FROM Department")
    departments = cur.fetchall()

    cur.execute("""
        SELECT e.*, d.Department_Name
        FROM Employee e
        JOIN Department d ON e.Department_ID = d.Department_ID
    """)
    employees = cur.fetchall()

    cur.execute("""
        SELECT * FROM Complaint_Update
        WHERE Complaint_ID = %s
        ORDER BY Update_Date
    """, (complaint_id,))
    updates = cur.fetchall()

    con.close()

    return render_template(
        'admin/update_status.html',
        complaint=complaint,
        departments=departments,
        employees=employees,
        updates=updates
    )


if __name__ == '__main__':
    app.run(debug=True)