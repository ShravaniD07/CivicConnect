-- Run this AFTER creating your tables
USE civic_system;

INSERT INTO Category (Category_Name, Description) VALUES
('Roads & Transport', 'Potholes, broken lights, road damage'),
('Water Supply',      'Leakage, no water, contamination'),
('Electricity',       'Outages, damaged poles, billing'),
('Sanitation',        'Garbage collection, drainage, sewage'),
('Parks & Gardens',   'Maintenance, damaged equipment');

INSERT INTO Complaint_Option (Category_ID, Option_Name, Priority) VALUES
(1, 'Pothole on Road',         'High'),
(1, 'Broken Street Light',     'Medium'),
(1, 'Damaged Road Divider',    'Medium'),
(1, 'Encroachment on Road',    'Low'),
(2, 'Water Pipe Leakage',      'High'),
(2, 'No Water Supply',         'High'),
(2, 'Water Contamination',     'High'),
(2, 'Low Water Pressure',      'Medium'),
(3, 'Power Outage',            'High'),
(3, 'Damaged Electric Pole',   'High'),
(3, 'Street Light Not Working','Medium'),
(3, 'Illegal Connection',      'Low'),
(4, 'Garbage Not Collected',   'High'),
(4, 'Blocked Drain',           'High'),
(4, 'Sewage Overflow',         'High'),
(4, 'Illegal Dumping',         'Medium'),
(5, 'Damaged Park Equipment',  'Medium'),
(5, 'Overgrown Grass',         'Low'),
(5, 'Broken Park Bench',       'Low');

INSERT INTO Department (Department_Name, Manager_Name, Manager_Email, Manager_Phone, Contact_Email, Phone) VALUES
('Roads Department',        'Suresh Patil',  'suresh@civic.gov',  '9876540001', 'roads@civic.gov',  '0202340001'),
('Water Supply Department', 'Priya Sharma',  'priya@civic.gov',   '9876540002', 'water@civic.gov',  '0202340002'),
('Electricity Department',  'Rahul Joshi',   'rahul@civic.gov',   '9876540003', 'elec@civic.gov',   '0202340003'),
('Sanitation Department',   'Meena Kulkarni','meena@civic.gov',   '9876540004', 'sanit@civic.gov',  '0202340004'),
('Parks Department',        'Arjun Desai',   'arjun@civic.gov',   '9876540005', 'parks@civic.gov',  '0202340005');

INSERT INTO Employee (Name, Email, Phone, Department_ID) VALUES
('Raj Kumar',    'raj@civic.gov',    '9800000001', 1),
('Sonal Mehta',  'sonal@civic.gov',  '9800000002', 1),
('Anjali Desai', 'anjali@civic.gov', '9800000003', 2),
('Vivek Naik',   'vivek@civic.gov',  '9800000004', 2),
('Vikram More',  'vikram@civic.gov', '9800000005', 3),
('Pooja Shah',   'pooja@civic.gov',  '9800000006', 4),
('Ravi Deshpande','ravi@civic.gov',  '9800000007', 5);

INSERT INTO Citizen (Name, Email, Phone, Address, Password) VALUES
('Amit Shah',   'amit@gmail.com',   '9000000001', '123 MG Road, Camp, Pune',        'amit123'),
('Priya Joshi', 'priya@gmail.com',  '9000000002', '45 Shivajinagar, Pune',           'priya123'),
('Rohan Verma', 'rohan@gmail.com',  '9000000003', '12 Kothrud Colony, Pune',         'rohan123');
