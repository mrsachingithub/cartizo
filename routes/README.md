# 🛒 Cartizo – Smart E-Commerce Platform with RefundGuard

Cartizo is an advanced **full-stack e-commerce platform** built using **Python & Flask**, featuring an intelligent **RefundGuard system** to detect and prevent return & refund abuse.

The platform simulates a real-world product company environment by combining **shopping workflows**, **user role management**, and **behavior-based risk analytics**.

---

## 🚀 Key Highlights

- Real-world **product-focused architecture**
- Intelligent **refund abuse detection**
- Admin-level **risk monitoring dashboard**
- Clean & modular Flask backend design

---

## 🎯 Core Features

### 🔐 RefundGuard – Abuse Detection System
- Automated **risk scoring (0–100)** for each user
- Detects:
  - High return frequency
  - Wardrobing patterns (use & return)
  - New account abuse
- Flags suspicious users for admin review
- Supports **future ML integration**

---

### 🛍️ Shopping & E-Commerce Features
- Product listing & browsing
- Search & filtering
- Cart management
- Checkout simulation (no real payment gateway)

---

### 👥 User Roles
- **Customer**
  - Browse products
  - Place orders
  - Request returns
- **Admin**
  - Monitor refund abuse
  - View user risk scores
  - Restrict abusive accounts

---

## 🧠 Risk Engine (RefundGuard Logic)

RefundGuard evaluates users based on:

- Return rate vs total orders
- Account age
- Time between purchase & return
- Repeated refund patterns
- Historical behavior trends

Each user receives a **Risk Score (0–100)**:
- **0–30** → Low Risk  
- **31–70** → Medium Risk  
- **71–100** → High Risk (Flagged)

---

## 🧰 Technology Stack

### Backend
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- Flask-Migrate (optional)

### Frontend
- HTML
- CSS
- JavaScript

### Architecture
- REST APIs
- Modular Flask application
- MVC-style structure

---

## 📂 Project Structure (Simplified)

