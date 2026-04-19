# CivicConnect — Civic Issue Tracking System
## Flask + MySQL + Python

---

## SETUP STEPS

### 1. Install VS Code
Download from: https://code.visualstudio.com/

### 2. Open the Project in VS Code
File → Open Folder → select the `civic_system` folder

### 3. Open Terminal in VS Code
Press: Ctrl + ` (backtick key)

### 4. Install Dependencies
```
pip install flask mysql-connector-python
```

### 5. Set Up MySQL Database
- Open MySQL Workbench or phpMyAdmin
- Run your table creation SQL (civic_system schema)
- Then run: sample_data.sql

### 6. Update DB Password
Open db.py → change "your_password" to your MySQL root password

### 7. Run the App
```
python app.py
```

### 8. Open in Browser
Go to: http://127.0.0.1:5000

---

## LOGIN CREDENTIALS (for testing)
- Citizen:  amit@gmail.com / amit123
- Admin:    admin / admin123

---

## PROJECT STRUCTURE
```
civic_system/
├── app.py              ← All Flask routes
├── db.py               ← MySQL connection
├── sample_data.sql     ← Test data
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── report_complaint.html
│   ├── complaint_detail.html
│   └── admin/
│       ├── admin_login.html
│       ├── manage_complaints.html
│       └── update_status.html
└── static/
    └── css/
```

## HOW THE SYSTEM WORKS
1. Citizen registers / logs in
2. Reports an issue → selects Category → selects Option → fills details
3. Admin logs in → sees all complaints → assigns dept + employee → updates status
4. Citizen tracks progress via timeline
5. After resolved → citizen submits 1-5 star feedback
