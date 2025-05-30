# 🗃️ Flask Inventory Management API

A secure, modular, role-based inventory management API built with **Flask**, **SQLAlchemy**, and **MongoDB (MongoEngine)**. Designed for internal dashboards with JWT session auth, RBAC (admin/staff), and scalable product metadata management.

---

## 🚀 Features

* ✅ **User Authentication**

  * JWT-based session system (access + refresh tokens)
  * `httpOnly` cookie storage
  * Password hashing with Bcrypt
  * Token blacklisting with Redis

* 🔐 **Role-Based Access Control**

  * Admin: Full CRUD access
  * Staff: Read-only access
  * Secure route protection with decorators

* 📦 **Inventory Management**

  * Products, Categories, Suppliers (CRUD)
  * MySQL via SQLAlchemy ORM

* 🧠 **Product Metadata in MongoDB**

  * Extended specs (SEO, tags, care instructions)
  * Synced on product create/update/delete

* 🌐 **Frontend Dashboard Ready**

  * Sidebar layout with Alpine.js
  * User dropdown with logout
  * Dark mode toggle

* 🛡️ **Security Features**

  * Brute-force login protection via Flask-Limiter
  * HTTPS-ready session design
  * CSRF-safe logout

---

## 📁 Project Structure

```
/package
│
├── backend/
│   ├── auth/                  # Signup, login, logout logic
│   ├── databases/
│   │   ├── Inventory/         # SQLAlchemy models
│   │   ├── product_log/       # MongoDB metadata services
│
├── frontend/                  # HTML templates, static files
│
├── routes/                    # Route definitions
│
├── services/                  # Business logic
│
├── utils/                     # Helper functions, decorators
│
└── __init__.py                # App factory, middleware, JWT setup
```

---

## ⚙️ Tech Stack

* **Flask** + **Blueprints** (modular API)
* **SQLAlchemy** (MySQL)
* **MongoEngine** (MongoDB for product metadata)
* **Redis** (JWT blacklist)
* **Flask-JWT-Extended** (secure session management)
* **Flask-Limiter** (rate limiting)
* **Pydantic v2** (request validation)

---

## 🔒 Authentication Flow

```text
1. POST /signup         → Create user
2. POST /login          → Returns JWTs (stored in cookies)
3. GET  /refresh        → Refresh token endpoint
4. POST /logout         → Revokes tokens (blacklist in Redis)
```

---

## 🧪 How to Run Locally

```bash
git clone https://github.com/yourusername/inventory-api.git
cd inventory-api

# Create virtualenv & activate
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure .env (JWT_SECRET, DB creds, etc.)
cp .env.example .env

# Run app
flask run --port 8080
```

---

## 📝 Environment Variables

```
JWT_SECRET_KEY=super-secret
MYSQL_URI=mysql://user:pass@localhost/inventory
MONGODB_URI=mongodb://localhost:27017/Catalog
REDIS_URL=redis://localhost:6379/0
```

---

## 👨‍💻 API Endpoints

| Method | Route                | Role        | Description       |
| ------ | -------------------- | ----------- | ----------------- |
| GET    | `/api/products`      | Admin/Staff | List all products |
| POST   | `/api/products`      | Admin       | Add new product   |
| PUT    | `/api/products/<id>` | Admin       | Update product    |
| DELETE | `/api/products/<id>` | Admin       | Delete product    |
| GET    | `/api/categories`    | Admin/Staff | List categories   |
| ...    |                      |             |                   |

---

## 📦 Metadata Handling (MongoDB)

Each product in MySQL is synced with an extended metadata document in MongoDB:

```json
{
  "product_id": 42,
  "name": "Smartwatch Pro",
  "tags": ["wearable", "electronics"],
  "seo_title": "Smartwatch Pro | Brand X",
  "care_instructions": "Keep away from water.",
  ...
}
```

---

## 📸 Screenshots

> *Coming soon...*

---

## 🙋‍♂️ Author

**\[Your Name]**
📧 [sikandaraidev@gmail.com](mailto:your.email@example.com)
🔗 [LinkedIn](https://linkedin.com/in/sikandaraidev) • [GitHub](https://github.com/sikandaraidev)

