# 🛡️ Image Moderation API

A full-stack image moderation service built with FastAPI, MongoDB, and Sightengine. It detects and blocks harmful content such as nudity, gore, weapons, and more. Includes token-based authentication, usage tracking, a Dockerized backend, and a minimal JavaScript frontend UI.

---

## 🚀 Features

- ✅ FastAPI-based REST API
- 🔒 Bearer token authentication (admin + regular users)
- 🧠 Real-time image analysis via Sightengine API
- 📊 MongoDB logs for tokens and API usage
- 🖼️ Minimal HTML + JavaScript frontend
- 🐳 Docker + Docker Compose setup

---

## 📦 Technologies Used

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** MongoDB Atlas
- **External API:** [Sightengine](https://sightengine.com/)
- **Frontend:** HTML + JavaScript
- **Containerization:** Docker, Docker Compose

---

## ⚙️ Setup & Installation

### 🔧 1. Clone the repository

```bash
git clone https://github.com/your-username/image-moderation-api.git
cd image-moderation-api
```

### 🔧 2. Create Environment File

Copy `.env.example` to `.env` and fill in your keys:

```env
MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/moderation
SIGHTENGINE_USER=your_sightengine_user
SIGHTENGINE_SECRET=your_sightengine_secret
SECRET_KEY=your_fastapi_secret_key
```

---

### 🔧 3. Run with Docker (Recommended)

```bash
docker-compose up --build
```

- API + Frontend hosted at: http://localhost:7000
- Health check: http://localhost:7000/health

---

## 💻 API Endpoints

| Method | Endpoint             | Auth       | Description                        |
|--------|----------------------|------------|------------------------------------|
| GET    | `/health`            | ❌ Public  | Health check                       |
| POST   | `/auth/tokens`       | ✅ Admin   | Create new token                   |
| GET    | `/auth/tokens`       | ✅ Admin   | List all tokens                    |
| DELETE | `/auth/tokens/{tok}` | ✅ Admin   | Delete a token                     |
| POST   | `/moderate`          | ✅ Regular | Upload image for moderation        |
| GET    | `/usage`             | ✅ Admin   | List usage logs                    |

---

## 🖼️ Frontend UI

- Navigate to `http://localhost:7000`
- Enter a valid token
- Upload an image
- Results display real-time:
  - `Safe: ✅ Yes` or `❌ No`
  - Detected categories and confidence scores

---

## 📂 Folder Structure

```
app/
├── api/            # Route handlers (auth, moderate, usage)
├── core/           # Configuration, database
├── static/         # Frontend files (HTML, JS)
├── main.py         # App entry point
├── Dockerfile
├── .env.example
```

---

## 🧪 Running Tests

```bash
pip install -r requirements.txt
pip install pytest
pytest
```

Sample test included for `/health` endpoint.

---

## 📊 MongoDB Collections

- `tokens`: Stores API tokens and admin flags
- `usages`: Stores usage logs per token and endpoint

---

## 🙌 Author

Made by Areej Zeb 
https://github.com/Areej-zeb

---

## 🧼 License
use freely, but give credit.