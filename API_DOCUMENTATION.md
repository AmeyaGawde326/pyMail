# API Documentation

## Overview
The Python Email Server provides a RESTful API for sending various types of emails. All protected endpoints require API key authentication.

## Base URL
```
http://localhost:5000
```

## Authentication
All protected endpoints require the `X-API-Key` header with your API key.

```bash
X-API-Key: your-api-key-here
```

## Rate Limiting
The API implements configurable rate limiting to prevent abuse. Rate limits can be configured via environment variables:

- **Rate Limit**: Configurable via `RATE_LIMIT` environment variable (default: 10 requests per second)
- **Applies to**: All endpoints uniformly
- **Storage**: Redis (persistent) or in-memory (resets on restart) - automatically detected

**Rate Limit Response (HTTP 429):**
```json
{
  "error": "Rate limit exceeded. Please try again later.",
  "status": "error"
}
```

**Note**: Rate limiting is always enabled and uses requests per second. Redis is automatically detected and used if available, providing persistent rate limiting across server restarts. If Redis is not available, the system automatically falls back to in-memory storage. **For production environments, always use Redis for reliable and persistent rate limiting.**

## Endpoints

### 1. Health Check
**GET** `/health`

No authentication required. Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Email Server",
  "version": "2.1.0",
  "email_types_count": 5,
  "rate_limiting": {
    "limit": "10 per second",
    "storage": "redis"
  }
}
```

### 2. Get Email Types
**GET** `/email-types`

Get list of available email types with descriptions.

**Headers:**
```bash
X-API-Key: your-api-key-here
```

**Response:**
```json
{
  "welcome_email": {
    "description": "Welcome email for new users with name, email, and login URL placeholders"
  },
  "account_confirmation_email": {
    "description": "Email confirmation with name, verification URL, and expiry time placeholders"
  },
  "password_reset_email": {
    "description": "Password reset email with name, reset link, and expiry time placeholders"
  },
  "access_key_email": {
    "description": "Access key generation email with service details and expiry information"
  },
  "invoice_email": {
    "description": "Invoice email with customer details, invoice information, and payment details"
  }
}
```

### 3. Send Email
**POST** `/send-email`

Single endpoint for all email types. Send any type of email using the `email_type` parameter.

**Headers:**
```bash
Content-Type: application/json
X-API-Key: your-api-key-here
```

**Request Body:**
```json
{
  "receiver_email": "recipient@example.com",
  "email_type": "email_type_key",
  "sender_name": "Sender Name",
  "sender_email": "sender@example.com",
  "variables": {
    "variable1": "value1",
    "variable2": "value2"
  }
}
```

**Required Fields:**
- `receiver_email`: Email address of the recipient
- `email_type`: Type of email to send
- `sender_email`: Email address of the sender
- `variables`: Template variables specific to the email type

**Optional Fields:**
- `sender_name`: Name of the sender (will use email if not provided)

## Email Types and Variables

### 1. Welcome Email (`welcome_email`)
**Use Case:** New user registration

**Required Variables:**
- `name`: User's full name
- `email`: User's email address
- `login_url`: URL to the login page

**Example Request:**
```json
{
  "receiver_email": "user@example.com",
  "email_type": "welcome_email",
  "sender_name": "Example App",
  "sender_email": "noreply@example.com",
  "variables": {
    "name": "Alice Smith",
    "email": "alice@example.com",
    "login_url": "https://example.com/login"
  }
}
```

### 2. Account Confirmation Email (`account_confirmation_email`)
**Use Case:** Email verification for new accounts

**Required Variables:**
- `name`: User's full name
- `verification_url`: URL to verify the account
- `expiry_hours`: Hours until the verification link expires

**Example Request:**
```json
{
  "receiver_email": "user@example.com",
  "email_type": "account_confirmation_email",
  "sender_name": "Example App",
  "sender_email": "noreply@example.com",
  "variables": {
    "name": "Bob Johnson",
    "verification_url": "https://example.com/verify?token=abc123",
    "expiry_hours": 1
  }
}
```

### 3. Password Reset Email (`password_reset_email`)
**Use Case:** Password reset requests

**Required Variables:**
- `name`: User's full name
- `reset_link`: URL to reset the password
- `expiry_hours`: Hours until the reset link expires

**Example Request:**
```json
{
  "receiver_email": "user@example.com",
  "email_type": "password_reset_email",
  "sender_name": "Example App",
  "sender_email": "noreply@example.com",
  "variables": {
    "name": "Carol Davis",
    "reset_link": "https://example.com/reset?token=xyz789",
    "expiry_hours": 24
  }
}
```

### 4. Access Key Email (`access_key_email`)
**Use Case:** API access key generation

**Required Variables:**
- `name`: User's full name
- `service_name`: Name of the service
- `access_key`: The generated access key
- `generated_date`: When the key was generated
- `expiry_date`: When the key expires
- `expiry_hours`: Hours until the key expires

**Example Request:**
```json
{
  "receiver_email": "user@example.com",
  "email_type": "access_key_email",
  "sender_name": "Example App",
  "sender_email": "noreply@example.com",
  "variables": {
    "name": "David Wilson",
    "service_name": "API Service",
    "access_key": "ak_1234567890abcdef",
    "generated_date": "2024-01-15 10:30:00",
    "expiry_date": "2024-01-18 10:30:00",
    "expiry_hours": 72
  }
}
```

### 5. Invoice Email (`invoice_email`)
**Use Case:** Business invoice emails

**Required Variables:**
- `customer_name`: Customer's full name
- `customer_email`: Customer's email address
- `invoice_number`: Invoice number
- `invoice_date`: Date of the invoice
- `due_date`: Due date for payment
- `total_amount`: Total amount due
- `company_name`: Your company name
- `payment_link`: URL to make payment
- `payment_terms`: Payment terms (e.g., "Net 30")
- `notes`: Additional notes or message

**Example Request:**
```json
{
  "receiver_email": "customer@example.com",
  "email_type": "invoice_email",
  "sender_name": "Example Corp",
  "sender_email": "billing@example.com",
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
}
```

## Response Format

### Success Response
**Status:** 200 OK

```json
{
  "success": true,
  "message": "Email sent successfully to recipient@example.com",
  "email_type": "welcome_email",
  "subject": "Welcome to Example App!"
}
```

### Error Response
**Status:** 400 Bad Request, 401 Unauthorized, 500 Internal Server Error

```json
{
  "success": false,
  "error": "Error message describing the issue"
}
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Missing fields or invalid data |
| 401 | Unauthorized - Invalid or missing API key |
| 500 | Internal Server Error - Email sending failure |

## cURL Examples

### Send Welcome Email
```bash
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "receiver_email": "user@example.com",
    "email_type": "welcome_email",
    "sender_name": "Example App",
    "sender_email": "noreply@example.com",
    "variables": {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "login_url": "https://example.com/login"
    }
  }'
```

### Get Email Types
```bash
curl -X GET http://localhost:5000/email-types \
  -H "X-API-Key: your-api-key"
```

### Health Check
```bash
curl -X GET http://localhost:5000/health
```

## Testing

Test the API endpoints using the provided test scripts:

```bash
# Quick test
python test_email_short.py

# Comprehensive test
python test_email.py
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## Security

- All sensitive endpoints require API key authentication
- Email type validation prevents unauthorized email types
- Variable validation ensures required data is provided
- Environment variables store sensitive configuration
- Input validation prevents injection attacks
