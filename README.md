# 🖼️ Image Caption Generator (LLaVA)

An AI-powered image captioning app using the **LLaVA vision-language model** via Ollama, with a FastAPI backend and a Streamlit frontend. Upload any image and receive a natural-language description instantly — all running locally.
![IMAGE CAPTION GENERATOR](https://github.com/WisteriaM7/IMAGE-CAPTION-GENERATOR/blob/main/Screenshot%202026-04-25%20203731.png)

---

## 🧠 Tech Stack

| Layer        | Technology              |
|--------------|-------------------------|
| Vision LLM   | LLaVA (via Ollama)      |
| Backend      | FastAPI + Uvicorn       |
| Frontend     | Streamlit               |
| Image Handle | Pillow                  |
| Language     | Python 3.10+            |

---

## 📁 Project Structure

```
image-caption-llava/
│
├── backend/
│   ├── __init__.py
│   └── main.py          # FastAPI app with /caption/ endpoint
│
├── frontend/
│   └── app.py           # Streamlit UI with image upload & preview
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/image-caption-llava.git
cd image-caption-llava
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama & Pull the LLaVA Model

- Download Ollama from: https://ollama.com
- Pull the model:

```bash
ollama pull llava
```

> ⚠️ LLaVA is a larger model (~4GB). Ensure you have sufficient disk space and RAM.

---

## 🚀 Running the App

Open **two separate terminals**:

**Terminal 1 — Start the Backend:**

```bash
uvicorn backend.main:app --reload
```

Backend runs at: `http://localhost:8000`

**Terminal 2 — Start the Frontend:**

```bash
streamlit run frontend/app.py
```

Frontend runs at: `http://localhost:8501`

---

## 📌 API Endpoints

| Method | Endpoint    | Description                        |
|--------|-------------|------------------------------------|
| GET    | `/`         | Health check                       |
| POST   | `/caption/` | Upload image, returns caption text |

### Example Request (curl)

```bash
curl -X POST http://localhost:8000/caption/ \
  -F "file=@your_image.jpg"
```

### Example Response

```json
{
  "caption": "A golden retriever sitting in a sunlit park, looking at the camera with a happy expression."
}
```

---

## ✅ Features

- Upload PNG, JPG, JPEG, or WEBP images
- Image preview with metadata (dimensions, file size, format)
- Copy-friendly caption text box
- CORS-enabled FastAPI backend
- File type validation on the backend
- Graceful error handling for Ollama connection issues and timeouts

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| Backend not connecting | Run `uvicorn backend.main:app --reload` |
| Ollama not responding | Run `ollama serve` and check with `ollama list` |
| Request timeout | LLaVA is slow on CPU — wait and retry, or use a GPU machine |
| Unsupported file type | Use PNG, JPG, JPEG, or WEBP only |
| Empty caption returned | Try a clearer image; very small or blurry images may confuse the model |
