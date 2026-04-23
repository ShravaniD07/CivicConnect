
create database civic_system;
USE civic_system;

CREATE TABLE Citizen (
    Citizen_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Email VARCHAR(50) UNIQUE,
    Phone VARCHAR(15),
    Address VARCHAR(100),
    Password VARCHAR(50)
);


CREATE TABLE Category (
    Category_ID INT PRIMARY KEY AUTO_INCREMENT,
    Category_Name VARCHAR(50) NOT NULL,
    Description VARCHAR(100)
);

-- 3️⃣ Complaint_Option (Priority stored here)
CREATE TABLE Complaint_Option (
    Option_ID INT PRIMARY KEY AUTO_INCREMENT,
    Category_ID INT,
    Option_Name VARCHAR(50) NOT NULL,
    Priority VARCHAR(10) DEFAULT 'Medium',
    FOREIGN KEY (Category_ID) REFERENCES Category(Category_ID)
        ON DELETE CASCADE
);

-- 4️⃣ Department
CREATE TABLE Department (
    Department_ID INT PRIMARY KEY AUTO_INCREMENT,
    Department_Name VARCHAR(50) NOT NULL,
    Manager_Name VARCHAR(50),
    Manager_Email VARCHAR(50),
    Manager_Phone VARCHAR(15),
    Contact_Email VARCHAR(50),
    Phone VARCHAR(15)
);

-- 5️⃣ Employee
CREATE TABLE Employee (
    Employee_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Email VARCHAR(50),
    Phone VARCHAR(15),
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
        ON DELETE SET NULL
);

-- 6️⃣ Complaint
CREATE TABLE Complaint (
    Complaint_ID INT PRIMARY KEY AUTO_INCREMENT,
    Citizen_ID INT,
    Option_ID INT,
    Department_ID INT,
    Employee_ID INT,
    Title VARCHAR(100),
    Description VARCHAR(200),
    Location VARCHAR(100),
    Date_Submitted DATE,
    Status VARCHAR(20) DEFAULT 'Pending',
    Parent_Complaint_ID INT,
    
    FOREIGN KEY (Citizen_ID) REFERENCES Citizen(Citizen_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (Option_ID) REFERENCES Complaint_Option(Option_ID)
        ON DELETE SET NULL,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
        ON DELETE SET NULL,
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
        ON DELETE SET NULL,
    FOREIGN KEY (Parent_Complaint_ID) REFERENCES Complaint(Complaint_ID)
        ON DELETE SET NULL
);

-- 7️⃣ Complaint_Update
CREATE TABLE Complaint_Update (
    Update_ID INT PRIMARY KEY AUTO_INCREMENT,
    Complaint_ID INT,
    Update_Message VARCHAR(200),
    Update_Date DATE,
    Status VARCHAR(20),
    
    FOREIGN KEY (Complaint_ID) REFERENCES Complaint(Complaint_ID)
        ON DELETE CASCADE
);

-- 8️⃣ Feedback
CREATE TABLE Feedback (
    Feedback_ID INT PRIMARY KEY AUTO_INCREMENT,
    Complaint_ID INT,
    Citizen_ID INT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comments VARCHAR(200),
    Feedback_Date DATE,
    
    FOREIGN KEY (Complaint_ID) REFERENCES Complaint(Complaint_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (Citizen_ID) REFERENCES Citizen(Citizen_ID)
        ON DELETE CASCADE
);



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


select * from Complaint;

select * from Feedback;
select * from Citizen;

select * from complaint_update;

ALTER TABLE Complaint
ADD Photo_Path VARCHAR(255),
ADD Latitude DECIMAL(10,7) NULL,
ADD Longitude DECIMAL(10,7) NULL;

