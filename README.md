# 🖼️ AI-Powered Image Classification API

A sophisticated REST API service that leverages deep learning to classify images using Google's InceptionV3 model. Built with Flask, MongoDB, and Docker, this application demonstrates modern full-stack development practices with AI/ML integration.

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-5.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)

## 🚀 Features

- **Advanced Image Classification**: Uses Google's pre-trained InceptionV3 model for accurate image recognition
- **User Authentication**: Secure user registration and authentication with bcrypt password hashing
- **Token-Based System**: Implemented usage tracking with token consumption for API calls
- **Multiple Input Methods**: Support for both URL-based and file upload image classification
- **RESTful API Design**: Clean, well-structured REST endpoints following best practices
- **Containerized Deployment**: Fully dockerized application with MongoDB integration
- **Admin Functionality**: Token refill system for user management
- **Error Handling**: Comprehensive error handling and validation
- **Real-time Predictions**: Fast image processing with confidence scores

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │────│   Flask API     │────│   MongoDB       │
│                 │    │                 │    │                 │
│ - Web Browser   │    │ - Authentication│    │ - User Data     │
│ - Mobile App    │    │ - Image Proc.   │    │ - Token Mgmt    │
│ - API Client    │    │ - ML Inference  │    │ - Session Data  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: Python 3.9, Flask, Flask-RESTful
- **Database**: MongoDB with PyMongo
- **Machine Learning**: TensorFlow, Keras, InceptionV3
- **Image Processing**: PIL (Pillow), NumPy
- **Security**: bcrypt for password hashing
- **Containerization**: Docker, Docker Compose
- **Development**: Git version control

## 📋 Prerequisites

- Docker and Docker Compose
- Git
- Python 3.9+ (for local development)

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/image-classification-api.git
   cd image-classification-api
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the API**
   - API Base URL: `http://localhost:5001`
   - MongoDB: `localhost:27017`

### Option 2: Local Development

1. **Install dependencies**
   ```bash
   cd web
   pip install -r requirements.txt
   ```

2. **Start MongoDB** (ensure MongoDB is running locally)

3. **Run the application**
   ```bash
   python app.py
   ```

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /register
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

#### Classify Image from URL
```http
POST /classify
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password",
    "url": "https://example.com/image.jpg"
}
```

#### Classify Uploaded Image
```http
POST /classify-image
Content-Type: multipart/form-data

username: your_username
password: your_password
image: [image_file]
```

#### Refill Tokens (Admin)
```http
POST /refill
Content-Type: application/json

{
    "username": "target_username",
    "admin_pw": "abc123",
    "amount": 10
}
```

#### Get All Users (Admin)
```http
GET /users
```

### Response Format

#### Successful Classification
```json
{
    "golden_retriever": 85.67,
    "labrador_retriever": 12.34,
    "chesapeake_bay_retriever": 1.99
}
```

#### Error Response
```json
{
    "status": 301,
    "message": "Invalid Username"
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
MONGODB_URL=mongodb://db:27017/
ADMIN_PASSWORD=abc123
FLASK_ENV=production
```

### Docker Configuration

The application uses multi-service Docker setup:
- **web**: Flask application (Port 5001)
- **db**: MongoDB database (Port 27017)

## 🧪 Testing the API

### Using cURL

1. **Register a user**
   ```bash
   curl -X POST http://localhost:5001/register \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass"}'
   ```

2. **Classify an image**
   ```bash
   curl -X POST http://localhost:5001/classify \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "testpass",
       "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Dog_face.jpg/256px-Dog_face.jpg"
     }'
   ```

### Using Python Requests

```python
import requests

# Register
response = requests.post('http://localhost:5001/register', json={
    'username': 'testuser',
    'password': 'testpass'
})

# Classify
response = requests.post('http://localhost:5001/classify', json={
    'username': 'testuser',
    'password': 'testpass',
    'url': 'https://example.com/image.jpg'
})

print(response.json())
```

## 📊 Performance Features

- **Pre-trained Model**: Uses Google's InceptionV3 for high accuracy
- **Image Optimization**: Automatic resizing and preprocessing
- **Token Management**: Usage tracking and rate limiting
- **Error Handling**: Graceful error handling with meaningful messages
- **Concurrent Processing**: Flask's threaded request handling

## 🔒 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **Input Validation**: Comprehensive input validation and sanitization
- **Error Messages**: Secure error handling without information leakage
- **Admin Controls**: Separate admin authentication for sensitive operations

## 🚀 Deployment

### Production Deployment

1. **Update environment variables** for production
2. **Use a reverse proxy** (nginx) for production
3. **Set up SSL certificates** for HTTPS
4. **Configure MongoDB** with authentication
5. **Use a container orchestration** platform (Kubernetes, Docker Swarm)

### Cloud Deployment Options

- **AWS**: ECS, EKS, or Elastic Beanstalk
- **Google Cloud**: Cloud Run, GKE, or App Engine
- **Azure**: Container Instances, AKS, or App Service
- **Heroku**: Container deployment with MongoDB Atlas

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Future Enhancements

- [ ] JWT-based authentication
- [ ] API rate limiting
- [ ] Image preprocessing options
- [ ] Batch image processing
- [ ] Custom model training
- [ ] Web interface for testing
- [ ] API documentation with Swagger
- [ ] Logging and monitoring
- [ ] CI/CD pipeline
- [ ] Unit and integration tests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@idanlips1](https://github.com/idanlips1)
- LinkedIn: [Idan Lipschitz](www.linkedin.com/in/idan-lipschitz-b061a8301)
- Email: idanlips@gmail.com

## 🙏 Acknowledgments

- Google Research for the InceptionV3 model
- Flask and TensorFlow communities
- MongoDB for the database solution
- Docker for containerization

---


