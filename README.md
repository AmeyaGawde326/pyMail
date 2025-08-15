# Python Email Server - Single Endpoint Version

A Flask-based web server that provides email sending functionality using Google SMTP with customizable email templates, modular architecture, and API key protection. Uses a single endpoint with email type validation for all email operations.

## Features

- **Single Endpoint Design** - One endpoint handles all email types with validation
- **Email Type Validation** - Comprehensive validation of email types and required variables
- **Professional Email Templates** - Beautiful HTML templates with CSS styling
- **API Key Protection** - Secure endpoints with authentication
- **Google SMTP Integration** - Reliable email delivery via Gmail
- **Multiple Email Types** - Welcome, confirmation, password reset, access key, and invoice emails
- **Environment Variable Configuration** - Secure credential management
- **Comprehensive Validation** - Input validation and error handling

## Project Structure

```
python-mail-server/
├── app.py              # Main Flask application with single endpoint
├── config.py           # Configuration management
├── templates.py        # Email templates and type mappings
├── utils.py            # Utility functions and validation
├── email_service.py    # Email service business logic
├── requirements.txt    # Python dependencies
├── test_email.py       # Comprehensive testing script
├── run.py              # Enhanced startup script
├── start_server.bat    # Windows startup script
└── README.md           # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Google SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=base64-encoded-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# API Security
API_KEY=your-api-key-here
```

**Important:** 
- For Gmail, you need to use an App Password, not your regular password
- Enable 2-factor authentication and generate an App Password in your Google Account settings
- The MAIL_PASSWORD must be base64 encoded (see instructions below)
- The API_KEY is required for all protected endpoints

### Password Encoding

The MAIL_PASSWORD must be base64 encoded for security. To encode your password:

**Linux/macOS:**
```bash
echo -n "your-actual-app-password" | base64
```

**Windows (PowerShell):**
```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your-actual-app-password"))
```

**Python:**
```python
import base64
password = "your-actual-app-password"
encoded = base64.b64encode(password.encode('utf-8')).decode('utf-8')
print(encoded)
```

Copy the encoded output and use it as your MAIL_PASSWORD value.

### 3. Run the Server

```bash
python run.py
```

Or on Windows:
```bash
start_server.bat
```

The server will start on `http://localhost:5000`

## API Endpoints

### Public Endpoints

#### Health Check
**GET** `/health`
- No authentication required
- Check if the service is running
- Returns email types count

### Protected Endpoints (Require API Key)

All protected endpoints require the `X-API-Key` header with your API key.

#### Send Email
**POST** `/send-email`
- Single endpoint for all email types
- Send any type of email using email_type parameter

#### Get Email Types
**GET** `/email-types`
- Get list of available email types with descriptions

## Email Types

### 1. Welcome Email (`welcome_email`)
- **Required Variables:** `name`, `email`, `login_url`
- **Use Case:** New user registration

### 2. Account Confirmation Email (`account_confirmation_email`)
- **Required Variables:** `name`, `verification_url`, `expiry_hours`
- **Use Case:** Email verification for new accounts

### 3. Password Reset Email (`password_reset_email`)
- **Required Variables:** `name`, `reset_link`, `expiry_hours`
- **Use Case:** Password reset requests

### 4. Access Key Email (`access_key_email`)
- **Required Variables:** `name`, `service_name`, `access_key`, `generated_date`, `expiry_date`, `expiry_hours`
- **Use Case:** API access key generation

### 5. Invoice Email (`invoice_email`)
- **Required Variables:** `customer_name`, `customer_email`, `invoice_number`, `invoice_date`, `due_date`, `total_amount`, `company_name`, `payment_link`, `payment_terms`, `notes`
- **Use Case:** Business invoice emails

## Usage Examples

### Send Welcome Email
```bash
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "receiver_email": "user@example.com",
    "email_type": "welcome_email",
    "variables": {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "login_url": "https://example.com/login"
    }
  }'
```

### Send Account Confirmation
```bash
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "receiver_email": "user@example.com",
    "email_type": "account_confirmation_email",
    "variables": {
        "name": "Bob Johnson",
        "verification_url": "https://example.com/verify?token=abc123",
        "expiry_hours": 1
    }
  }'
```

### Send Password Reset
```bash
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "receiver_email": "user@example.com",
    "email_type": "password_reset_email",
    "variables": {
        "name": "Carol Davis",
        "reset_link": "https://example.com/reset?token=xyz789",
        "expiry_hours": 24
    }
  }'
```

### Send Access Key
```bash
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "receiver_email": "user@example.com",
    "email_type": "access_key_email",
    "variables": {
        "name": "David Wilson",
        "service_name": "API Service",
        "access_key": "ak_1234567890abcdef",
        "generated_date": "2024-01-15 10:30:00",
        "expiry_date": "2024-01-18 10:30:00",
        "expiry_hours": 72
    }
  }'
```

### Send Invoice
```bash
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "receiver_email": "customer@example.com",
    "email_type": "invoice_email",
    "variables": {
        "customer_name": "John Doe",
        "customer_email": "customer@example.com",
        "invoice_number": "INV-2024-001",
        "invoice_date": "2024-01-15",
        "due_date": "2024-02-15",
        "total_amount": "299.99",
        "company_name": "Example Corp",
        "payment_link": "https://example.com/pay/inv-2024-001",
        "payment_terms": "Net 30",
        "notes": "Thank you for your business!"
    }
  }'
```

### Get Available Email Types
```bash
curl -X GET http://localhost:5000/email-types \
  -H "X-API-Key: your-api-key"
```

## Request Format

All email requests use the same format:

```json
{
    "receiver_email": "recipient@example.com",
    "email_type": "email_type_key",
    "variables": {
        "variable1": "value1",
        "variable2": "value2"
    }
}
```

## Testing

Run the comprehensive test suite:

```bash
python test_email.py
```

The test script will:
- Test the single endpoint with all email types
- Verify API key protection
- Test error handling and validation
- Validate email sending functionality

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **200 OK:** Successful email sent
- **400 Bad Request:** Missing required fields or invalid email type
- **401 Unauthorized:** Missing or invalid API key
- **500 Internal Server Error:** Email sending failures or server errors

## Security Features

- **API Key Authentication** - All sensitive endpoints require valid API key
- **Email Type Validation** - Comprehensive validation of email types
- **Variable Validation** - Required variables are validated for each email type
- **Environment Variables** - Sensitive data stored securely
- **Input Validation** - Comprehensive validation of all inputs
- **Error Handling** - Secure error messages without information leakage

## Production Deployment

For production use:

1. **Change Default Keys** - Update API_KEY in production
2. **Environment Variables** - Use proper environment management
3. **HTTPS** - Enable SSL/TLS for all communications
4. **Rate Limiting** - Implement rate limiting for API endpoints
5. **Monitoring** - Add logging and monitoring
6. **Database** - Store API keys in secure database instead of environment

## Troubleshooting

### Common Issues

1. **Authentication Failed:** Check your Gmail App Password
2. **API Key Required:** Ensure X-API-Key header is included
3. **Invalid Email Type:** Check the email_type parameter
4. **Missing Variables:** Ensure all required variables are provided
5. **Connection Refused:** Verify SMTP settings and firewall rules

### Gmail Setup

1. Enable 2-Factor Authentication in your Google Account
2. Generate an App Password for "Mail"
3. Use the App Password in your `.env` file
4. Ensure "Less secure app access" is disabled (App Passwords are more secure)

## Architecture Benefits

- **Single Endpoint** - Simplified API with one endpoint for all email types
- **Type Validation** - Comprehensive validation of email types and variables
- **Maintainability** - Easy to modify and extend functionality
- **Testability** - Components can be tested in isolation
- **Scalability** - Modular design allows for easy scaling
- **Security** - Centralized authentication and validation
- **Professional** - Production-ready code structure

## Template Structure

The email templates use a clear mapping structure:

```python
# Email template type keys
WELCOME_EMAIL_KEY = "welcome_email"
ACCOUNT_CONFIRMATION_KEY = "account_confirmation_email"
PASSWORD_RESET_KEY = "password_reset_email"
ACCESS_KEY_KEY = "access_key_email"
INVOICE_KEY = "invoice_email"

# Main template mapping
TEMPLATE_MAP = {
    WELCOME_EMAIL_KEY: welcome_email,
    ACCOUNT_CONFIRMATION_KEY: account_confirmation_email,
    PASSWORD_RESET_KEY: password_reset_email,
    ACCESS_KEY_KEY: access_key_email,
    INVOICE_KEY: invoice_email
}

# Valid email types list
VALID_EMAIL_TYPES = list(TEMPLATE_MAP.keys())
```

This structure makes it easy to:
- Add new email types
- Validate email type parameters
- Maintain template consistency
- Generate documentation automatically
