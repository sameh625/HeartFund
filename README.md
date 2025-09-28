#  HeartFund – Crowdfunding Platform

HeartFund is a crowdfunding web application built with **Django** and **JavaScript**, where users can register, create projects, manage their own campaigns, and support others' ideas.  

---

## 🚀 Features


### 🔐 Authentication
- User registration with:
  - First name & last name
  - Email & password
  - Egyptian phone number validation
- Login/Logout system
- Access control: only logged-in users can create/edit projects

### 📂 Projects
- Create new fundraising campaigns with:
  - Title & details
  - Funding target
  - Start & end dates (with validation)
- View all projects
- View single project details
- Edit or delete your own projects
- Search projects by date range
- Display project owner’s info for easy support

### 🎨 Frontend
- Modern responsive UI with **custom CSS**
- Smooth navbar, hero section, and footer
- Interactive project cards with view/edit/delete buttons
- Dynamic JavaScript integration with Django REST API
- Messages (success/error) styled

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**:PostgreSQL
- **Authentication**: Django’s custom user model
- **API**: JSON responses for all CRUD operations

---

## ⚙️ Installation & Setup
```bash
git clone https://github.com/sameh625/HeartFund.git
cd heartfund
Create a virtual environment
python -m venv venv
```
```
source venv/bin/activate  # (Linux)
venv\Scripts\activate     # (Windows)
pip install -r requirements.txt
```
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Visit 👉 http://127.0.0.1:8000
```
---
## API Endpoints
| Method | Endpoint                                                | Description                          |
| ------ | ------------------------------------------------------- | ------------------------------------ |
| GET    | `/projects/api/`                                        | List all projects                    |
| POST   | `/projects/api/`                                        | Create a new project (auth required) |
| GET    | `/projects/api/<id>/`                                   | Get project details                  |
| PUT    | `/projects/api/<id>/`                                   | Update a project                     |
| DELETE | `/projects/api/<id>/`                                   | Delete a project                     |
| GET    | `/projects/api/mine/`                                   | List logged-in user’s projects       |
| GET    | `/projects/api/search/?start=YYYY-MM-DD&end=YYYY-MM-DD` | Search projects by date              |

---
## Video Demo 
[Screencast from 27 سبت, 2025 EEST 06:41:02 م.webm](https://github.com/user-attachments/assets/4447b60a-9ad1-4b9a-9f64-ded944a7955c)

