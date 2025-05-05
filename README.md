# 🏥 Hospital Management System

A modern desktop-based Hospital Management System built with **Python**, **Tkinter**, and **SQLite**. This system provides intuitive interfaces for managing **patients**, **doctors**, and **appointments**, complete with record dashboards and recent activity logs.

## 📌 Features

- 🔐 **Welcome screen with loading animation**
- 👨‍⚕️ **Patient Management** – Add, edit, delete, search, and generate visit receipts
- 👩‍⚕️ **Doctor Management** – Add, update, and delete doctor records
- 📅 **Appointment Scheduling** – Book time slots with conflict checking
- 📊 **All Records Dashboard** – Visual overview of all patients, doctors, and appointments
- 🕓 **Recent Activity Feed** – Track new additions and appointments
- 🗂️ **SQLite3 Database** – Auto-initialized and locally persistent
- 🖼️ **GUI** – Clean, responsive design using Tkinter with ttk widgets

---

## 🧰 Tech Stack

- **Python 3.x**
- **Tkinter** for GUI
- **SQLite3** for database
- **ttk.Treeview** for displaying records
- **ttk.Progressbar** for animated loading screen

---

## 🚀 Getting Started

### 🔧 Prerequisites

Ensure Python 3 is installed on your system.

You can download Python from: https://www.python.org/downloads/

---

### 💾 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Hospital-Management-System.git
cd Hospital-Management-System

```
**Run the app:**
python main.py

The system will auto-generate the hospital.db database on first run.

# 🗂️ Project Structure:

Hospital-Management-System/

├── main.py  
├── database.py           
├── welcome_screen.py     
└── hospital.db           

# 🛠️ Customization:

- Edit the colors and fonts in main.py under the self.colors and self.font_* attributes.

- Modify the working hours and appointment durations in database.py under get_available_time_slots().
- Extend with additional modules like billing, user login, or reporting.

# 📄 License
This project is licensed under the **MIT License**.
Feel free to use, modify, and distribute with attribution.

# 🙋‍♂️ Author
**Muhammad Shahzaib**  
Aspiring AI/ML Engineer & Founder of DreamTechX  
Feel free to connect or contribute!

# ⭐ Support
If you like this project, don't forget to ⭐ the repository!
