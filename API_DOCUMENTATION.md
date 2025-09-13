# 📚 API Documentation

## Base URL
```
http://localhost:5001
```

## Authentication
All endpoints (except `/register`) require authentication using username and password in the request body.

## Endpoints

### 1. User Registration

**POST** `/register`

Register a new user account.

#### Request Body
```json
{
    "username": "string",
    "password": "string"
}
```

#### Response
```json
{
    "status": 200,
    "message": "You successfully signed up for the API"
}
```

#### Error Responses
```json
{
    "status": 301,
    "message": "Username already exists"
}
```

---

### 2. Classify Image from URL

**POST** `/classify`

Classify an image from a provided URL.

#### Request Body
```json
{
    "username": "string",
    "password": "string",
    "url": "string"
}
```

#### Response
```json
{
    "golden_retriever": 85.67,
    "labrador_retriever": 12.34,
    "chesapeake_bay_retriever": 1.99
}
```

#### Error Responses
```json
{
    "status": 301,
    "message": "Invalid Username"
}
```
```json
{
    "status": 302,
    "message": "Invalid Password"
}
```
```json
{
    "status": 303,
    "message": "You are out of tokens, please refill"
}
```
```json
{
    "error": "No url provided"
}
```

---

### 3. Classify Uploaded Image

**POST** `/classify-image`

Classify an image uploaded as a file.

#### Request Body (multipart/form-data)
```
username: string
password: string
image: file
```

#### Response
```json
{
    "golden_retriever": 85.67,
    "labrador_retriever": 12.34,
    "chesapeake_bay_retriever": 1.99
}
```

#### Error Responses
```json
{
    "status": 301,
    "message": "No image file provided"
}
```
```json
{
    "status": 301,
    "message": "No image file selected"
}
```
```json
{
    "status": 301,
    "message": "Error processing image: [error details]"
}
```

---

### 4. Refill Tokens (Admin Only)

**POST** `/refill`

Refill tokens for a user account (admin function).

#### Request Body
```json
{
    "username": "string",
    "admin_pw": "string",
    "amount": number
}
```

#### Response
```json
{
    "status": 200,
    "message": "Tokens refilled successfully"
}
```

#### Error Responses
```json
{
    "status": 301,
    "message": "Invalid Username"
}
```
```json
{
    "status": 302,
    "message": "Invalid Admin Password"
}
```

---

### 5. Get All Users (Admin Only)

**GET** `/users`

Retrieve all users and their token counts.

#### Response
```json
{
    "status": 200,
    "message": "Users retrieved successfully",
    "users": [
        {
            "username": "user1",
            "tokens": 5
        },
        {
            "username": "user2",
            "tokens": 3
        }
    ],
    "total_users": 2
}
```

#### Error Responses
```json
{
    "status": 301,
    "message": "Error retrieving users: [error details]"
}
```

## Status Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 301  | Invalid Username / File Error |
| 302  | Invalid Password / Admin Password |
| 303  | Insufficient Tokens |
| 400  | Bad Request |

## Rate Limiting

- Each user starts with 6 tokens
- Each classification request consumes 1 token
- Tokens can be refilled by admin users
- Users cannot make requests when tokens = 0

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)

## Image Processing

- Images are automatically resized to 299x299 pixels
- RGB conversion is performed if necessary
- InceptionV3 preprocessing is applied
- Top 3 predictions are returned with confidence scores

## Example Usage

### Python
```python
import requests

# Register user
response = requests.post('http://localhost:5001/register', json={
    'username': 'testuser',
    'password': 'testpass'
})

# Classify image from URL
response = requests.post('http://localhost:5001/classify', json={
    'username': 'testuser',
    'password': 'testpass',
    'url': 'https://example.com/image.jpg'
})

print(response.json())
```

### cURL
```bash
# Register user
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Classify image
curl -X POST http://localhost:5001/classify \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass",
    "url": "https://example.com/image.jpg"
  }'
```

### JavaScript
```javascript
// Register user
const registerResponse = await fetch('http://localhost:5001/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'testuser',
    password: 'testpass'
  })
});

// Classify image
const classifyResponse = await fetch('http://localhost:5001/classify', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'testuser',
    password: 'testpass',
    url: 'https://example.com/image.jpg'
  })
});

const result = await classifyResponse.json();
console.log(result);
```
