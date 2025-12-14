# Coursework 2 – Intelligence Platform (Multi-Domain Analytics)

This project is a Streamlit-based intelligence platform built for **Cybersecurity** and **IT Operations**, featuring incident dashboards, database integration, authentication, and a clean UI.  
I have completed the project till  **Tier 2 requirements** of the Coursework.

---

##  MY Details

This project is  developed by **Raahemeen Ahmad Khan**, MSIS **M01051518**, as part of the CST1510 Programming for Data Communication and Networks module at Middlesex University Dubai.

---

##  Overview

This project implements a platform capable of analysing and managing incidents across multiple domains.  
It includes:

- Secure login system  
- Cybersecurity incident dashboard  
- IT operations outage dashboard  
- SQLite database backend  
- Data filtering & visualisation  
- Ability to add new incidents  
- Optional AI assistant feature (OpenAI)

---

##  Features

###  1. Secure Authentication
- Login form with username + password  
- Passwords stored as **bcrypt hashes**  
- Role support (e.g., "user", "admin")  
- Session state management  

---

###  2. Cybersecurity Dashboard
- Loads incidents from `cyber_incidents` table in SQLite  
- Filter by:
  - Severity  
  - Status  
  - Incident type  
  - Date range  
- Metrics:
  - Total incidents  
  - Open/Investigating  
  - High/Critical  
- Charts:
  - Bar chart (severity distribution)  
  - Line chart (incidents over time)  
- Add new cybersecurity incidents  
- (Optional) AI assistant for analytics  

---

###  3. IT Operations – Outage Dashboard
- Pulls from `it_incidents` table  
- Filter by:
  - Service name  
  - Severity  
  - Status  
- Metrics:
  - Total IT incidents  
  - Open/Investigating  
  - Resolved  
- Visualisation:
  - Severity chart  
  - Detected-date trend  
- Add new IT incidents

---

###  4. SQLite Database

Used for persistent storage:

| Table            | Purpose                         |
|------------------|---------------------------------|
| `users`          | Stores login credentials (hashed) |
| `cyber_incidents`| Cyber incident records          |
| `it_incidents`   | IT outage records               |

CSV files are loaded into the database initially.

---

##  Project Structure

```text
project/
│
├── app.py                  # Main Streamlit application
├── db_helper.py            # Database helper functions
├── db_setup.py             # (If used) DB initialisation / migration
├── ai_helper.py            # (Optional) AI assistant integration
├── README.md               # Documentation
│
├── data1/
│   ├── cw2.db              # SQLite database
│   ├── users.txt           # Seed users (username, hash, role)
│   ├── incidents.csv       # Cyber incidents CSV
│   └── it_incidents.csv    # IT incidents CSV (if used)
│
└── pages/
    ├── Login.py                    # Login page
    ├── CybersecurityDashboard.py   # Cybersecurity dashboard
    └── ITDashboard.py              # IT operations dashboard
