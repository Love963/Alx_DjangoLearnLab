# Social Media API Documentation

## Base URL

http://localhost:8000/

## **Authentication**

All endpoints that modify data require authentication.
We use **token-based authentication**.

* Header example:

```
Authorization: Token <your_token_here>
```

---

## **Accounts (User Authentication)**

### **Register a New User**

* **URL:** `/accounts/register/`
* **Method:** `POST`
* **Body:**

```json
{
  "username": "tame",
  "email": "tame@example.com",
  "password": "password123"
}
```

* **Response:**

```json
{
  "id": 1,
  "username": "tame",
  "email": "tame@example.com",
  "token": "abcd1234token"
}
```

---

### **Login**

* **URL:** `/accounts/login/`
* **Method:** `POST`
* **Body:**

```json
{
  "username": "tame",
  "password": "password123"
}
```

* **Response:**

```json
{
  "token": "abcd1234token"
}
```

---

## **Posts**

### **List All Posts**

* **URL:** `/posts/`
* **Method:** `GET`
* **Query Parameters (optional):**

  * `author=<user_id>` → Filter by author
  * `search=<keyword>` → Search in title/content
  * `ordering=created_at` → Order by creation date
  * `ordering=-created_at` → Descending order
  * `?page=1` → Pagination
* **Response:**

```json
[
  {
    "id": 1,
    "author": "tame",
    "title": "My first post",
    "content": "Hello world",
    "created_at": "2025-08-20T05:19:24Z",
    "updated_at": "2025-08-20T05:19:24Z",
    "comments": [
      {
        "id": 1,
        "post": 1,
        "author": "tame",
        "content": "This is my first comment",
        "created_at": "2025-08-20T05:21:01Z",
        "updated_at": "2025-08-20T05:21:01Z"
      }
    ]
  }
]
```

---

### **Retrieve a Single Post**

* **URL:** `/posts/<post_id>/`
* **Method:** `GET`
* **Response:** Same as list but only for one post.

---

### **Create a Post**

* **URL:** `/posts/`
* **Method:** `POST`
* **Headers:** Authorization token required
* **Body:**

```json
{
  "title": "My first post",
  "content": "Hello world"
}
```

* **Response:**

```json
{
  "id": 1,
  "author": "tame",
  "title": "My first post",
  "content": "Hello world",
  "created_at": "2025-08-20T05:19:24Z",
  "updated_at": "2025-08-20T05:19:24Z",
  "comments": []
}
```

---

### **Update a Post**

* **URL:** `/posts/<post_id>/`
* **Method:** `PUT` or `PATCH`
* **Headers:** Authorization token required
* **Note:** Only the post author can update.
* **Body Example (PATCH):**

```json
{
  "title": "Updated post title"
}
```

---

### **Delete a Post**

* **URL:** `/posts/<post_id>/`
* **Method:** `DELETE`
* **Headers:** Authorization token required
* **Note:** Only the post author can delete.

---

## **Comments**

### **List All Comments**

* **URL:** `/comments/`
* **Method:** `GET`
* **Response:**

```json
[
  {
    "id": 1,
    "post": 1,
    "author": "tame",
    "content": "This is my first comment",
    "created_at": "2025-08-20T05:21:01Z",
    "updated_at": "2025-08-20T05:21:01Z"
  }
]
```

---

### **Create a Comment**

* **URL:** `/comments/`
* **Method:** `POST`
* **Headers:** Authorization token required
* **Body:**

```json
{
  "post": 1,
  "content": "This is my first comment"
}
```

* **Response:**

```json
{
  "id": 1,
  "post": 1,
  "author": "tame",
  "content": "This is my first comment",
  "created_at": "2025-08-20T05:21:01Z",
  "updated_at": "2025-08-20T05:21:01Z"
}
```

---

### **Update a Comment**

* **URL:** `/comments/<comment_id>/`
* **Method:** `PUT` or `PATCH`
* **Headers:** Authorization token required
* **Note:** Only the comment author can update.

---

### **Delete a Comment**

* **URL:** `/comments/<comment_id>/`
* **Method:** `DELETE`
* **Headers:** Authorization token required
* **Note:** Only the comment author can delete.

---

### **Pagination**

* All list endpoints (`/posts/` and `/comments/`) support pagination.
* Default page size: `5` posts/comments per page.
* Use query param `?page=<number>`.

---

### **Filtering & Searching**

* **Posts filtering:**

  * `?author=<user_id>` → filter by author
  * `?search=<keyword>` → search in title or content
  * `?ordering=created_at` → ascending
  * `?ordering=-created_at` → descending

---

**End of API\_DOCS.md**
