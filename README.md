# 📚 Smart Library System (FastAPI)

A modern library management system built using **`FastAPI`** with authentication, book borrowing, and role-based access control.  
## 🚀 Features - 
- **User Authentication** (JWT-based)
- **Book Management** (CRUD operations)
- **Smart Borrowing System** (borrow, return, track due dates) 
- **Role-Based Access Control** (admin, user, librarian) 
- **Advanced Search & Filtering**  
---  
## ⚙️ Installation & Setup  

### **1️⃣ Clone the Repository** 
```sh 
git clone https://github.com/swayam5342/backend
cd backend
```
### **2️⃣ Install Dependencies**

Ensure you have Python 3.12 installed.

```
pip install uv
uv add pyproject.toml
```
### **3️⃣ Start the Server**

``` sh
uvicorn app.main:app --reload
```

API is now available at **http://127.0.0.1:8000** 🚀

---

## 🔑 Authentication (OAuth2)

This API uses JWT-based authentication with OAuth2.

- **Login URL:** `/auth/login`
- **Token Type:** Bearer Token
- **Example Request (Swagger UI Compatible):** 

```shell
 Authorization: Bearer <your_token>
 ```

#### **Login Request (Form-Data)**

``` json
{"username": "user@example.com",   "password": "securepassword" }
```

#### **Response**

```json
{"access_token": "<JWT_TOKEN>",   "token_type": "bearer" }
```

---

## 📘 API Endpoints

### **1️⃣ Authentication**

|Method|Endpoint|Description|
|---|---|---|
|`POST`|`/auth/register`|Register a new user|
|`POST`|`/auth/login`|Login and get a JWT token|

### **2️⃣ Books Management**

|Method|Endpoint|Description|Auth|
|---|---|---|---|
|`GET`|`/library/books`|Get all books|Public|
|`POST`|`/library/books`|Add a new book|🔒 Admin|
|`GET`|`/library/books/{book_id}`|Get book by ID|Public|
|`PUT`|`/library/books/{book_id}`|Update book details|🔒 Admin|
|`DELETE`|`/library/books/{book_id}`|Delete a book|🔒 Admin|

### **3️⃣ Borrowing System**

|Method|Endpoint|Description|Auth|
|---|---|---|---|
|`POST`|`/borrow/borrow/{book_id}`|Borrow a book|🔒 User|
|`POST`|`/borrow/return/{book_id}`|Return a book|🔒 User|
|`GET`|`/borrow/borrowed`|Get borrowed books|🔒 User|

---

## 📄 Swagger UI & API Documentation

Interactive API Docs are available at:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 🛠 Technologies Used

- **FastAPI** - Backend Framework
- **SQLAlchemy** - ORM for database interactions
- **MySQL** - Database
- **JWT (OAuth2)** - Secure Authentication
- **Alembic** - Database Migrations

---

## 🏗 Future Improvements

- 📌 Implement **email notifications** for overdue books
- 📌 Add **fine calculation** for late returns
- 📌 Develop a **frontend** for better user experience

---

## 👨‍💻 Contributors

- **Swayam** ([@swayam5342](https://github.com/swayam5342))
