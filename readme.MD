# 🔗 URL Shortener

A simple URL Shortener web application built with **Python, Flask, and SQLite**. The application converts long URLs into shorter, unique URLs and redirects users to the original URL when the shortened link is accessed.

It also stores URL mappings in a SQLite database and keeps track of how many times each shortened URL has been accessed.

## 🚀 Features

* 🔗 Convert long URLs into short URLs
* 🔄 Redirect short URLs to their original URLs
* 💾 Store URL mappings in a SQLite database
* ♻️ Return the existing short URL if the same long URL is submitted again
* 🔐 Generate unique short URL hashes
* 📊 Track the number of times each shortened URL is accessed
* ⚠️ Handle invalid URLs and unavailable short URLs
* ⚙️ Automatically create the required database table on application startup

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **SQLite**
* **HTML**
* **SQL**
* **os** – Environment and file path handling

## 📂 Project Structure

```text
URL-Shortener/
│
├── url_shorten.py
├── url_hash.py
├── url_shortener.db
│
├── templates/
│   └── index.html
│
└── README.md
```

> `url_shortener.db` is created automatically when the application starts if it does not already exist.

## ⚙️ How It Works

The application provides two main operations:

### 1. Shorten a URL

The user enters a long URL through the web interface.

The application:

1. Receives the URL from the form.
2. Adds `https://` if a protocol is not provided.
3. Checks whether the URL already exists in the database.
4. If it exists, the previously generated short URL is returned.
5. Otherwise, a short hash is generated using `generate_short_url_hash()`.
6. The application checks whether the generated hash already exists.
7. If there is a collision, another hash is generated.
8. The long URL and short URL are stored in the database.

### 2. Redirect to the Original URL

When a user opens a shortened URL:

```text
http://localhost:5000/<short_url>
```

the application:

1. Searches for the short URL in the database.
2. Retrieves the corresponding long URL.
3. Increases the `access_count` by 1.
4. Redirects the user to the original URL.

If the short URL does not exist, the application returns:

```text
URL not found
```

with HTTP status code `404`.

## 🗄️ Database Design

The application uses SQLite with a table named `url_mapping`.

| Column         | Type    | Description                                |
| -------------- | ------- | ------------------------------------------ |
| `id`           | INTEGER | Unique record ID                           |
| `long_url`     | TEXT    | Original URL                               |
| `short_url`    | TEXT    | Generated shortened URL                    |
| `access_count` | INTEGER | Number of times the short URL was accessed |

The `short_url` column has a `UNIQUE` constraint to prevent duplicate short URLs.

## 🔌 Application Routes

### `GET /`

Displays the URL shortening web page.

### `POST /shorten`

Accepts a long URL and generates a shortened URL.

Example form request:

```text
POST /shorten
long_url=https://www.example.com
```

### `GET /<short_url>`

Redirects the user to the original URL associated with the provided short URL.

Example:

```text
GET /a8F3kL
```

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repository-name.git
```

### 2. Navigate to the project directory

```bash
cd URL-Shortener
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 5. Install Flask

```bash
pip install flask
```

## ▶️ Running the Application

Run the Flask application using:

```bash
python url_shorten.py
```

The application will start on:

```text
http://127.0.0.1:5000
```

Open the URL in your web browser and enter a long URL to generate a shortened URL.

## 💡 Example

Suppose the user enters:

```text
https://www.example.com/products/software
```

The application generates a shortened URL similar to:

```text
http://127.0.0.1:5000/a8F3kL
```

When the shortened URL is opened, the application redirects the user to:

```text
https://www.example.com/products/software
```

The database also increments the `access_count` for that shortened URL.

## 🔐 Database Configuration

By default, the SQLite database is created in the project directory:

```text
url_shortener.db
```

The database location can also be configured using the environment variable:

```text
URL_SHORTENER_DB_PATH
```

For example, on Windows:

```powershell
$env:URL_SHORTENER_DB_PATH="C:\path\to\url_shortener.db"
```

Then run:

```bash
python url_shorten.py
```

## 🧠 Key Concepts Demonstrated

This project demonstrates practical knowledge of:

* Python application development
* Flask web application development
* HTTP GET and POST requests
* URL routing
* HTTP redirects
* HTML form handling
* SQLite database connectivity
* SQL queries
* Database CRUD operations
* Unique constraints
* Hash-based identifier generation
* Collision handling
* Environment variables
* Error handling with HTTP status codes

## 🔮 Future Improvements

Possible improvements for future versions include:

* Add URL validation
* Create a REST API for URL shortening
* Add a dashboard for URL analytics
* Display access statistics
* Add URL expiration
* Add custom short URLs
* Add user authentication
* Improve error pages
* Deploy the application to a cloud platform
* Add automated tests
* Use a production WSGI server instead of Flask's development server

## 👨‍💻 Author

**Tamilselvan P**

Aspiring Software Engineer | Python developer

Interested in **Python Development, Software Engineering, Data Analytics, and Backend Development**.

---

⭐ If you find this project useful, feel free to star the repository!
