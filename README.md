# Python Email Server

A Flask-based web server that provides email sending functionality using Google SMTP with customizable email templates, modular architecture, and API key protection.

## Features

- **Single Endpoint Design** - One endpoint handles all email types with validation
- **Email Type Validation** - Comprehensive validation of email types and required variables
- **Professional Email Templates** - Beautiful HTML templates with CSS styling
- **API Key Protection** - Secure endpoints with authentication
- **Google SMTP Integration** - Reliable email delivery via Gmail
- **Multiple Email Types** - Welcome, confirmation, password reset, access key, and invoice emails
- **Environment Variable Configuration** - Secure credential management
- **Rate Limiting** - Configurable rate limiting to prevent API abuse
- **Comprehensive Validation** - Input validation and error handling

## Project Structure

```
python-mail-server/
├── app.py                    # Main Flask application with Redis rate limiting
├── config.py                 # Configuration management with Redis support
├── templates.py              # Email templates and type mappings
├── utils.py                  # Utility functions and validation
├── email_service.py          # Email service business logic
├── requirements.txt          # Python dependencies including Flask-Limiter & Redis
├── test_email.py             # Comprehensive testing script
├── test_email_short.py      # Quick testing script
├── test_rate_limiting.py    # Rate limiting & Redis test script
├── run.py                    # Enhanced startup script
├── docker-compose.yml        # Docker setup with Redis service
├── rate_limit_examples.env  # Example rate limiting configurations
├── GMAIL_DOMAIN_EMAIL_SETUP.md # Complete domain email setup guide
├── API_DOCUMENTATION.md      # API endpoints and usage with Redis rate limiting
├── CUSTOM_TEMPLATES.md       # How to create and add custom email templates
├── ENVIRONMENT_SETUP.md      # Detailed environment configuration and Redis setup
└── README.md                 # This file
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the root directory:

```env
MAIL_USERNAME=your-gmail-account@gmail.com
MAIL_PASSWORD=base64-encoded-app-password
API_KEY=your-api-key-here
```

**Important Notes:**
- For Gmail, you need to use an App Password, not your regular password
- Enable 2-factor authentication and generate an App Password in your Google Account settings
- The MAIL_PASSWORD must be base64 encoded
- The API_KEY is required for all protected endpoints
- **Domain Email Setup**: If you want to send emails from a custom domain (e.g., contact@yourdomain.com), you still need to use your Gmail account as MAIL_USERNAME. The domain email will be used as sender_email in your API requests. See `GMAIL_DOMAIN_EMAIL_SETUP.md` for a complete step-by-step guide using Cloudflare Email Routing.

### 2.1 Setting Up Your .env File

1. **Create a `.env` file** in your project root directory
2. **Encode your app password** using base64 encoding
3. **Fill in your `.env` file** with your Gmail account, encoded password, and API key

**Basic .env structure:**
```env
MAIL_USERNAME=yourname@gmail.com
MAIL_PASSWORD=base64-encoded-app-password
API_KEY=your-secure-api-key // This is a random string of password that you can use to authenticate req
```

**Important:** Use your Gmail account (not domain email) as `MAIL_USERNAME`.

### 2.2 Rate Limiting Configuration
The server includes configurable rate limiting to prevent abuse. You can control rate limits through environment variables:

```env
# Rate Limiting Configuration
RATE_LIMIT=10

# Redis Configuration for Rate Limiting (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

**Rate Limit Options:**
- `RATE_LIMIT`: Number of requests per second (default: 10)

**Redis Options (Optional):**
- `REDIS_HOST`: Redis server hostname (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)
- `REDIS_PASSWORD`: Redis password (optional)

**Note:** All rate limit values are requests per second. Redis is automatically detected and used if available, providing persistent rate limiting across server restarts. If Redis is not available, the system automatically falls back to in-memory storage. **For production environments, always use Redis for reliable and persistent rate limiting.**

For detailed setup instructions and troubleshooting, see **[Environment Setup Guide](ENVIRONMENT_SETUP.md)**.

### 3. Run the Server
```bash
python run.py
```

The server will start on `http://localhost:5000`

### 4. Domain Email Setup (Optional)
If you want to send emails from a custom domain address (e.g., `contact@yourdomain.com`):

1. **Follow the complete guide**: `GMAIL_DOMAIN_EMAIL_SETUP.md`
2. **Use Cloudflare Email Routing** for easy domain email setup
3. **Configure Gmail** to send emails from your domain
4. **Run Docker componse with** `docker compose up -d` 
5. **Test with**: `python test_email_short.py`
6. **For all endpoints and complete test with**: `python test_email.py`

**Key Point**: You still use your Gmail account credentials in the `.env` file, but specify your domain email as `sender_email` in API requests.

## Documentation

- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference with request/response examples
- **[Custom Templates](CUSTOM_TEMPLATES.md)** - How to create and add custom email templates
- **[Domain Email Setup](GMAIL_DOMAIN_EMAIL_SETUP.md)** - Complete guide for custom domain emails
- **[Environment Setup](ENVIRONMENT_SETUP.md)** - Detailed environment configuration and troubleshooting

## Testing

```bash
# Quick test
python test_email_short.py

# Comprehensive test
python test_email.py

# Rate limiting test
python test_rate_limiting.py
```

### Rate Limiting Testing
The `test_rate_limiting.py` script tests the rate limiting functionality by making multiple rapid requests to trigger rate limits. This helps verify that your rate limiting configuration is working correctly.

## License

This project is open source and available under the [MIT License](LICENSE).
