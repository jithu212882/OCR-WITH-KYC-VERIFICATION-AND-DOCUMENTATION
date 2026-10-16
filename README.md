KYC Document Verification and OCR PoC
A lightweight, automated Proof-of-Concept (PoC) web application for verifying identity documents (PAN Card, Aadhaar Card, Passport) and extracting structured KYC entities.
🚀 Tech Stack
Backend: FastAPI (Python 3.12) & Uvicorn
Vision & Pre-check: OpenCV (Laplacian variance focus measure, `< 100` blur threshold)
OCR Engine: EasyOCR (CRAFT detector & deep recognition model with confidence scoring)
Entity Parser: Regex patterns for DOB (`DD/MM/YYYY`), PAN (`[A-Z]{5}[0-9]{4}[A-Z]`), Aadhaar (`\d{4}\s?\d{4}\s?\d{4}`), and Passport (`[A-Z][0-9]{7}`)
Frontend: Single-Page Dashboard (HTML5, Tailwind CSS via CDN, vanilla JavaScript) served directly by FastAPI.
---
🛠️ Key Features
File Upload & Live Preview:
Drag-and-drop or file selector supporting PNG, JPEG, JPG, and WEBP documents.
OpenCV Blur & Quality Guard:
Calculates Laplacian variance (`cv2.Laplacian(gray, cv2.CV_64F).var()`).
Flags blurry images (`variance < 100.0`) with a warning overlay badge and advisory recommendation.
Highlights sharp images (`variance >= 100.0`) with a green verification badge.
EasyOCR Text & Confidence Extraction:
Extracts all detected lines with per-line confidence percentages and bounding box coordinates.
Calculates overall mean document confidence score.
Structured KYC Entity Extraction:
Date of Birth: Formats `DD/MM/YYYY` (or labeled variations).
PAN Card: Format `[A-Z]{5}[0-9]{4}[A-Z]` with 4th-character entity type detection (Individual, Company, Firm, etc.).
Aadhaar Card: Format `\d{4}\s?\d{4}\s?\d{4}` with automated masked format (`XXXX XXXX 1234`).
Passport: Format `[A-Z][0-9]{7}`.
Document Classification: Automatically identifies document type (PAN Card, Aadhaar Card, Passport).
Interactive Single-Page Dashboard:
Left Column: Upload drop-zone, document preview with dynamic Quality Overlay Badge (`✓ Sharp` vs `⚠ Blurry`), toggleable bounding box layer, and document dimensions.
Right Column: Identified Document header, Overall OCR Confidence score gauge, clean card grid for parsed KYC entities with 1-click clipboard copy, and collapsible Raw OCR Text Stream with line-by-line confidence badges and real-time text filter.
1-Click Test Samples: Top bar contains instant test buttons for mock PAN, Aadhaar, Passport, and Blurry cards.
---
📂 Project Structure
```
d:/OCR/
├── app/
│   ├── __init__.py
│   ├── config.py              # Constants, threshold (< 100), paths
│   ├── main.py                # FastAPI endpoints & static routing
│   ├── vision/
│   │   ├── __init__.py
│   │   ├── quality.py         # OpenCV Laplacian blur check
│   │   └── ocr_engine.py      # EasyOCR singleton & text extraction
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── kyc_parser.py      # Regex entity extraction (DOB, PAN, Aadhaar, Passport)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Glassmorphism, animations, bbox overlay styles
│   │   ├── js/
│   │   │   └── app.js         # Frontend controller, drag-drop, DOM rendering
│   │   └── samples/           # Mock sample documents for instant testing
│   └── templates/
│       └── index.html         # Responsive dashboard with Tailwind CSS CDN
├── sample_generator.py        # Generates mock synthetic KYC documents
├── tests/
│   ├── test_samples.py        # Verification test runner
│   └── test_api_upload.py     # Multipart HTTP upload test runner
├── requirements.txt
└── run.py                     # Application runner
```
---
🏃 Running the Application
1. Start Server
```powershell
.\venv\Scripts\python.exe run.py
```
Or with Uvicorn:
```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
2. Access in Browser
Navigate to:
```
http://127.0.0.1:8000
```
Click any of the top 1-Click Test Samples (`PAN Card (Sharp)`, `Aadhaar Card (Sharp)`, `Passport (Sharp)`, or `Blurry Doc (< 100)`) to test instantly.
Or drag-and-drop any PNG/JPEG image from your computer into the upload zone.
