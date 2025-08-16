# Python Email Server

A robust, production-ready email server built with Flask that supports multiple email templates, rate limiting, and Redis integration.

## 🚀 Features

- **Multiple Email Templates**: Welcome emails, account confirmations, password resets, and more
- **Rate Limiting**: Configurable rate limiting with Redis persistence or in-memory fallback
- **API Key Authentication**: Secure endpoints with API key validation
- **SMTP Integration**: Gmail SMTP support with TLS encryption
- **Docker Support**: Containerized deployment with Docker Compose
- **Health Monitoring**: Built-in health check endpoint
- **Template Variables**: Dynamic email content with variable substitution

## ⚠️ Important Notice: Email Delivery

**Emails sent through this server may be delivered to recipients' spam/junk folders.** This is a common issue with automated email services, especially when:

- Sending from a new domain or IP address
- Using Gmail SMTP for bulk sending
- Recipients haven't previously engaged with your emails
- Email content triggers spam filters

**Recommendations:**
- Inform your recipients to check their spam/junk folders
- Ask them to mark your emails as "Not Spam" and add your sender address to their contacts
- Consider implementing email authentication (SPF, DKIM, DMARC) for better deliverability
- Monitor your sender reputation and bounce rates
- Start with small email volumes and gradually increase to build trust

## 📁 Project Structure

```
python-mail-server/
├── app/                          # Core application code
│   ├── services/                 # Business logic services
│   │   └── email_service.py     # Email sending service
│   ├── utils/                    # Utility functions
│   │   └── utils.py             # Validation and helper functions
│   ├── templates/                # Email templates
│   │   └── templates.py         # Email template definitions
│   ├── routes/                   # API route definitions
│   ├── app.py                    # Main Flask application
│   └── run.py                    # Application entry point
├── config/                       # Configuration files
│   ├── config.py                 # Application configuration
│   ├── env_example.txt          # Environment variables template
│   └── rate_limit_examples.env  # Rate limiting examples
├── docs/                         # Documentation
│   ├── API_DOCUMENTATION.md     # API reference
│   ├── CUSTOM_TEMPLATES.md      # Template customization guide
│   ├── ENVIRONMENT_SETUP.md     # Environment setup guide
│   └── GMAIL_DOMAIN_EMAIL_SETUP.md # Gmail configuration
├── docker/                       # Docker configuration
│   ├── Dockerfile               # Container definition
│   └── docker-run.sh            # Docker run script
├── scripts/                      # Utility scripts
│   └── encode_password.py       # Password encoding utility
├── tests/                        # Test files
│   ├── test_email.py            # Email functionality tests
│   ├── test_email_short.py      # Quick email tests
│   └── test_rate_limiting.py    # Rate limiting tests
├── docker-compose.yml            # Docker Compose configuration
├── main.py                       # Main entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🛠️ Quick Start

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- Gmail account with App Password

### 1. Clone and Setup
```bash
git clone <repository-url>
cd python-mail-server
```

### 2. Environment Configuration
```bash
# Copy and configure environment variables
cp config/env_example.txt .env
# Edit .env with your Gmail credentials and API key
```

### 3. Run with Docker (Recommended)
```bash
docker-compose up -d
```

### 4. Run Locally
```bash
pip install -r requirements.txt
python main.py
```

## 🔧 Configuration

### Environment Variables
- `MAIL_USERNAME`: Your Gmail address
- `MAIL_PASSWORD`: Base64 encoded Gmail App Password
- `API_KEY`: Secret API key for authentication
- `RATE_LIMIT`: Requests per second (default: 10)
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`: Redis configuration

### Rate Limiting
- **Protected endpoints** (`/send-email`, `/email-types`): Rate limited per second
- **Health endpoint** (`/health`): No rate limiting for monitoring
- **Storage**: Redis for persistence, in-memory fallback

## 📡 API Endpoints

### Send Email
```http
POST /send-email
X-API-Key: your-api-key
Content-Type: application/json

{
  "receiver_email": "user@example.com",
  "email_type": "welcome_email",
  "variables": {
    "name": "John Doe",
    "login_url": "https://example.com/login"
  },
  "sender_name": "Your App",
  "sender_email": "noreply@yourapp.com"
}
```

### Get Email Types
```http
GET /email-types
X-API-Key: your-api-key
```

### Health Check
```http
GET /health
```

## 🧪 Testing

### Rate Limiting Tests
```bash
python tests/test_rate_limiting.py
```

### Email Tests
```bash
python tests/test_email.py
```

## 🔒 Security Features

- **API Key Authentication**: All protected endpoints require valid API key
- **Rate Limiting**: Prevents abuse and ensures fair usage
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Secure error responses without information leakage

## 📊 Monitoring

The health endpoint provides:
- Service status
- Version information
- Email template count
- Rate limiting configuration
- Storage type (Redis/Memory)

## 🐳 Docker Deployment

### Production
```bash
docker-compose -f docker-compose.yml up -d
```

### Development
```bash
docker-compose -f docker-compose.yml up --build
```

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md) - Complete API reference
- [Environment Setup](docs/ENVIRONMENT_SETUP.md) - Detailed setup guide
- [Custom Templates](docs/CUSTOM_TEMPLATES.md) - Template customization
- [Gmail Setup](docs/GMAIL_DOMAIN_EMAIL_SETUP.md) - Gmail configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation in the `docs/` folder
2. Review the test files for usage examples
3. Open an issue on GitHub

---

**Built with ❤️ using Flask, Redis, and Docker**
