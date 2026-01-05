# Mini Document Validator 🚢

A production-grade FastAPI microservice that validates insurance documents using Google Gemini AI. Built for **Genoshi Technologies LLP** assignment.

## 🎯 Features

- **AI-Powered Extraction**: Uses Google Gemini 1.5 Flash to extract structured data from unstructured insurance documents
- **Business Rule Validation**: Validates extracted data against 4 critical business rules
- **Robust Error Handling**: Comprehensive error handling for AI failures, invalid data, and edge cases
- **Production Ready**: Includes Docker support, logging, health checks, and comprehensive tests
- **Type Safe**: Full type annotations with Pydantic models

## 📋 Prerequisites

- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mini_doc_validator
```

### 2. Set Up Environment

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_actual_gemini_api_key_here
APP_ENV=development
LOG_LEVEL=INFO
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

The API will be available at `http://localhost:8080`

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Endpoints

#### `POST /validate`

Validates an insurance document and extracts key fields.

**Request Body:**
```json
{
  "text": "This Marine Hull Insurance Policy confirms that the vessel MV Neptune is covered under policy number HM-2025-10-A4B for the period from 1st November 2025 to 31st October 2026. The total insured value is INR 5,000,000."
}
```

**Response:**
```json
{
  "extracted_data": {
    "policy_number": "HM-2025-10-A4B",
    "vessel_name": "MV Neptune",
    "policy_start_date": "2025-11-01",
    "policy_end_date": "2026-10-31",
    "insured_value": 5000000
  },
  "validation_results": [
    {
      "rule": "Date Consistency",
      "status": "PASS",
      "message": "Policy end date is after start date."
    },
    {
      "rule": "Value Check",
      "status": "PASS",
      "message": "Insured value is valid."
    },
    {
      "rule": "Vessel Name Match",
      "status": "PASS",
      "message": "Vessel 'MV Neptune' is on the approved list."
    },
    {
      "rule": "Completeness Check",
      "status": "PASS",
      "message": "Policy number is present."
    }
  ]
}
```

#### `GET /health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "ai_extractor": "initialized",
  "validator": "initialized"
}
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_validation.py

# Run with verbose output
pytest -v
```

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t mini-doc-validator:latest .
```

### Run the Container

```bash
docker run -d \
  --name doc-validator \
  -p 8080:8080 \
  -e GEMINI_API_KEY=your_gemini_api_key \
  mini-doc-validator:latest
```

### Check Container Health

```bash
docker ps
docker logs doc-validator
```

### Stop the Container

```bash
docker stop doc-validator
docker rm doc-validator
```

## 📁 Project Structure

```
mini_doc_validator/
│
├── main.py                 # FastAPI application entry point
├── ai_extractor.py        # Gemini AI integration
├── validation.py          # Business rule validation logic
├── models.py              # Pydantic models
├── utils.py               # Utility functions
├── valid_vessels.json     # Approved vessel names list
│
├── tests/
│   └── test_validation.py # Unit tests for validation
│
├── .env                   # Environment variables (create this)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `APP_ENV` | Application environment | No | development |
| `LOG_LEVEL` | Logging level | No | INFO |

### Valid Vessels

Edit `valid_vessels.json` to add or remove approved vessel names:

```json
[
  "MV Neptune",
  "SS Voyager",
  "Ocean Star",
  "Sea Breeze",
  "The Horizon"
]
```

## 📊 Validation Rules

The system validates extracted data against 4 business rules:

1. **Date Consistency**: Policy end date must be after start date
2. **Value Check**: Insured value must be greater than 0
3. **Vessel Name Match**: Vessel must be in the approved list (case-insensitive)
4. **Completeness Check**: Policy number must not be null or empty

## 🔍 Example Use Cases

### Valid Document

```bash
curl -X POST "http://localhost:8080/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Marine Hull Insurance Policy HM-2025-10-A4B covers vessel MV Neptune from 1st November 2025 to 31st October 2026 for INR 5,000,000."
  }'
```

### Document with Validation Failures

```bash
curl -X POST "http://localhost:8080/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Insurance policy covers vessel Unknown Ship from 2026-10-31 to 2025-11-01 for INR 0."
  }'
```

## 🛠️ Development

### Running in Development Mode

```bash
uvicorn main:app --reload --log-level debug
```

### Code Quality

The codebase follows:
- **PEP 8** style guidelines
- **Type hints** for all functions
- **Comprehensive error handling**
- **Structured logging**
- **Modular architecture**

### Adding New Validation Rules

1. Add the rule logic to `validation.py`
2. Update the `validate()` method to include your rule
3. Add tests in `tests/test_validation.py`
4. Update this README

## 🐛 Troubleshooting

### API Key Issues

**Error:** `GEMINI_API_KEY not found in environment variables`

**Solution:** Ensure your `.env` file exists and contains a valid API key.

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'google.generativeai'`

**Solution:** Install dependencies: `pip install -r requirements.txt`

### Port Already in Use

**Error:** `Address already in use`

**Solution:** Change the port or kill the process:
```bash
lsof -ti:8080 | xargs kill -9
uvicorn main:app --port 8081
```

### Docker Build Fails

**Solution:** Ensure Docker daemon is running and you have sufficient disk space.

## 📝 API Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid input or validation failure) |
| 500 | Internal Server Error (AI failure or system error) |

## 🤝 Contributing

This is an assignment project, but improvements are welcome:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request
