# Pakistan Tourism Management System (PKTM)

**A comprehensive web application for managing and exploring tourist destinations, hotels, restaurants, bookings, and reviews across Pakistan.**  
Built using **Flask**, **SQLAlchemy**, and **MySQL**, PKTM offers a seamless experience for tourists and administrators alike.


## 🌟 Features

- 🔐 User and Admin Authentication  
- 🔍 Browse & Search Tourist Destinations, Hotels, and Restaurants  
- 🏨 Book Hotels & Make Restaurant Reservations  
- ⭐ Leave Reviews for Destinations, Hotels, and Restaurants  
- 🛠️ Admin Dashboard for Managing Content  
- 🧑‍💼 User Dashboard for Managing Bookings, Favorites, and Reservations


## 🖥️ System Requirements

### Software:
- **Python** 3.13+
- **MySQL Server**
- **Flask** 3.1.1+
- **pip** for dependency management

### Python Libraries:
Dependencies are listed in `pyproject.toml`, including:
- Flask
- SQLAlchemy
- Flask-WTF
- PyMySQL
- Other relevant Flask extensions

### Hardware:
- Minimum: Dual-core CPU, 2GB RAM
- Recommended: Quad-core CPU, 4GB+ RAM

## ⚙️ Installation Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/pktm.git
   cd pktm
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install .
   ```

4. **Configure Database Connection**
   - Default: `mysql+pymysql://root:password@localhost/DataBaseName`
   - To override, set the `DATABASE_URL` environment variable.

6. **(Optional) Populate Sample Data via Script**
   ```bash
   python populate_database.py
   ```

7. **Run the Application**
   ```bash
   python main.py
   ```
   Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## 🔐 Demo Login Credentials

| Role   | Email                  | Password   |
|--------|------------------------|------------|
| Admin  | admin@tourism.pk       | admin123   |
| User   | user1@example.com      | user123    |

---

## 🗂️ Code Structure Overview

```plaintext
├── app.py / main.py               # Application entry points
├── models.py                      # SQLAlchemy models
├── forms.py                       # WTForms input forms
├── routes.py / views.py           # Routes and view logic
├── populate_database.py           # Script to populate DB with sample data
├── templates/                     # Jinja2 HTML templates
├── static/                        # Static CSS and JS files
└── pyproject.toml                 # Dependency configuration
```

## 🙌 Credits

### 👥 Team Members
- **[Ahmad Hassan]** – Backend Development, Flask API Integration  
- **[Rehan Ali]** – Frontend Design, User Dashboard  
- **[Aqsa Aziz]** – Admin Features, Reviews System
- **[M Ysir]** – Database Design, Data Population Scripts, Deployment Configuration

### 📦 Libraries & Resources
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PyMySQL](https://pypi.org/project/PyMySQL/)
- [WTForms](https://wtforms.readthedocs.io/)
- [Bootstrap 5](https://getbootstrap.com/)
- [FontAwesome](https://fontawesome.com/)


© 2025 Pakistan Tourism Management System  
_Explore Pakistan like never before._ 🇵🇰
