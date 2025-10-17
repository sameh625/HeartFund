## HeartFund – Crowdfunding Platform 💛

Bring ideas to life. HeartFund lets users launch campaigns, donate securely, and track progress in real time.

### Highlights
- Custom user model (email login + Egyptian phone validator)
- Campaign media uploads (cover image)
- Donations with live progress and ownership/target rules
- Search by date range + multiple ordering options
- Clean REST API consumed by a lightweight JS frontend

---

## Features

### Authentication
- Register, login, logout
- Email as username; strong validation for Egyptian mobile numbers
- Only authenticated users can create/edit/delete their projects

### Campaigns
- Create campaigns with title, details, target, start/end dates
- Upload an optional cover image
- View all campaigns, or your own in “My Campaigns”
- Update or delete your campaigns (owner-only)
- Search by date range
- Order by latest, target, raised amount, or ending soon/last

### Donations
- Contribute to any campaign (except your own)
- Blocked once target is reached
- Prevent over-target contributions with hint for remaining amount
- Live progress bar and raised amount

### UI/UX
- Responsive, modern styling (custom CSS)
- JS-driven pages for listing, search, detail, add/edit

---

## Tech Stack
- Backend: Django, Django REST Framework
- Frontend: HTML, CSS, JS (Fetch API)
- Database: PostgreSQL (default in settings)

---

## Setup

### 1) Clone & env
```bash
git clone https://github.com/sameh625/HeartFund.git
cd heartFund
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 2) Install deps
```bash
pip install -r requirements.txt
```

### 3) Configure DB (PostgreSQL)
Update `heartfund/settings.py` to match your local DB (default is `crowd_fund`):
- NAME, USER, PASSWORD, HOST, PORT

### 4) Migrate & run
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open `http://127.0.0.1:8000`.

### Media
- Uploaded images are served from `MEDIA_URL` (`/media/`) in development.

---

## API (Quick Reference)

### Campaigns
- GET `/projects/api/?order=latest` – list campaigns
  - `order`: `latest`, `target_asc`, `target_desc`, `raised_asc`, `raised_desc`, `end_asc`, `end_desc`
- POST `/projects/api/` – create (auth required)
- GET `/projects/api/<id>/` – retrieve
- PUT `/projects/api/<id>/` – update (owner only)
- DELETE `/projects/api/<id>/` – delete (owner only)
- GET `/projects/api/mine/` – list current user’s campaigns (auth)
- GET `/projects/api/search/?start=YYYY-MM-DD&end=YYYY-MM-DD&order=latest` – search by date range

- ### Contributions
- GET `/projects/api/<id>/contributions/` – list contributions for a campaign
- POST `/projects/api/<id>/contributions/` – create contribution (auth)
  - Rules: cannot donate to your own project; blocked when fully funded; cannot exceed target
---

## Project Structure (core)
```text
apps/
  accounts/   # auth (custom user, register/login)
  home/       # landing page
  projects/   # model, API, and pages (add/mine)
static/
  css/        # styles
  js/         # frontend logic
templates/
  base.html + partials (navbar/footer)
```

---

## Demo
[Heartfund.webm](https://github.com/user-attachments/assets/0414f3de-abc0-4c58-bb28-b2fc4eb23f6c)
---

## Notes
- Ensure Pillow is installed for image uploads.
- If you deploy, configure media/static serving and database credentials appropriately.

