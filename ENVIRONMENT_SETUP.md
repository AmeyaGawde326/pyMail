# Environment Setup Guide

## Overview
This guide provides detailed instructions for setting up your environment variables and troubleshooting common issues with the Flask Email Server.

## Prerequisites
- A Gmail account
- Access to your project directory
- Basic command line knowledge
- Redis (recommended for production, optional for development)

## Step-by-Step Setup

### Step 1: Create the .env File

#### Windows
```cmd
# Command Prompt
echo. > .env

# PowerShell
New-Item -Path ".env" -ItemType File
```

#### macOS/Linux
```bash
touch .env
```

### Step 2: Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click "2-Step Verification" under "Signing in to Google"
3. Follow the setup process to enable 2FA
4. **Important**: You must complete 2FA setup before generating app passwords

### Step 3: Generate Gmail App Password

1. Return to [Google Account Security](https://myaccount.google.com/security)
2. Click "App passwords" under "2-Step Verification"
3. Select "Mail" from the "Select app" dropdown
4. Select "Other (Custom name)" from the "Select device" dropdown
5. Enter a descriptive name (e.g., "Flask Email Server")
6. Click "Generate"
7. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)
8. Click "Done"

**Note**: The password will only be shown once. If you lose it, you'll need to generate a new one.

### Step 4: Encode Your App Password

#### Windows PowerShell
```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your-16-char-app-password"))
```

**Example:**
```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("abcd efgh ijkl mnop"))
# Output: YWJjZCBmZ2ggaWprbCBtbm9w
```

#### macOS/Linux Terminal
```bash
echo -n "your-16-char-app-password" | base64
```

**Example:**
```bash
echo -n "abcd efgh ijkl mnop" | base64
# Output: YWJjZCBmZ2ggaWprbCBtbm9w
```

#### Python (Cross-platform)
```python
import base64
password = "your-16-char-app-password"
encoded = base64.b64encode(password.encode('utf-8')).decode('utf-8')
print(encoded)
```

**Example:**
```python
import base64
password = "abcd efgh ijkl mnop"
encoded = base64.b64encode(password.encode('utf-8')).decode('utf-8')
print(encoded)
# Output: YWJjZCBmZ2ggaWprbCBtbm9w
```

### Step 5: Configure Your .env File

Open the `.env` file in your text editor and add the following:

```env
# Your Gmail account (not domain email)
MAIL_USERNAME=yourname@gmail.com

# Base64 encoded app password
MAIL_PASSWORD=YWJjZCBmZ2ggaWprbCBtbm9w==

# Your custom API key (change from default)
API_KEY=your-secure-api-key-here

# Rate Limiting Configuration
RATE_LIMIT=10

# Redis Configuration for Rate Limiting (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

**Example completed .env file:**
```env
MAIL_USERNAME=john.doe@gmail.com
MAIL_PASSWORD=YWJjZCBmZ2ggaWprbCBtbm9w==
API_KEY=my-super-secure-api-key-123
RATE_LIMIT=10
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

### Step 6: Redis Setup (Recommended for Production)

Redis provides persistent rate limiting across server restarts. **For production environments, Redis is strongly recommended.**

#### Option A: Local Redis Installation

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Windows:**
Download and install from [Redis for Windows](https://github.com/microsoftarchive/redis/releases)

#### Option B: Docker Redis (Recommended)

```bash
# Start Redis container
docker run -d --name redis -p 6379:6379 redis:7-alpine

# Or use docker-compose (includes Redis)
docker-compose up -d
```

#### Option C: Cloud Redis Services

- **Redis Cloud**: [redis.com](https://redis.com/)
- **AWS ElastiCache**: Redis-compatible
- **Google Cloud Memorystore**: Redis-compatible
- **Azure Cache for Redis**

### Step 7: Verify Configuration

1. **Check file location**: Ensure `.env` is in your project root directory
2. **Check file format**: No extra spaces, quotes, or special characters
3. **Check encoding**: Ensure the file is saved as UTF-8
4. **Test Redis connection** (if configured): Ensure Redis is accessible
5. **Restart server**: Restart your Flask server after making changes

## Common Issues and Solutions

### Issue: "Username and Password not accepted"

**Symptoms:**
- Error: `(535, b'5.7.8 Username and Password not accepted')`
- Authentication fails when starting server

**Solutions:**
1. **Verify MAIL_USERNAME**: Use your Gmail account, not domain email
2. **Check app password**: Ensure you're using the app password, not regular password
3. **Verify 2FA**: 2FA must be enabled before generating app passwords
4. **Regenerate password**: Create a new app password if issues persist

**Example fix:**
```env
# ❌ Wrong - using domain email
MAIL_USERNAME=contact@yourdomain.com

# ✅ Correct - using Gmail account
MAIL_USERNAME=yourname@gmail.com
```

### Issue: "App password not working"

**Symptoms:**
- App password is rejected
- Authentication fails immediately

**Solutions:**
1. **Copy full password**: Ensure you copied all 16 characters
2. **Remove spaces**: App passwords may have spaces that need to be included
3. **Wait for activation**: Wait 2-5 minutes after generating before using
4. **Regenerate**: Create a new app password if problems continue

**Example:**
```env
# ❌ Wrong - missing characters
MAIL_PASSWORD=YWJjZCBmZ2ggaWprbCBtbm9w

# ✅ Correct - full encoded password
MAIL_PASSWORD=YWJjZCBmZ2ggaWprbCBtbm9w==
```

### Issue: "Base64 encoding problems"

**Symptoms:**
- Invalid base64 string errors
- Encoding/decoding failures

**Solutions:**
1. **Use exact commands**: Follow the platform-specific commands above
2. **No extra characters**: Don't add quotes, spaces, or line breaks
3. **Test simple password**: Try with a simple password first
4. **Verify output**: Ensure the output is a clean string without extra characters

**Troubleshooting:**
```bash
# Test if your encoding worked
echo "YWJjZCBmZ2ggaWprbCBtbm9w" | base64 -d
# Should output: abcd efgh ijkl mnop
```

### Issue: "API key not working"

**Symptoms:**
- 401 Unauthorized errors
- API key validation fails

**Solutions:**
1. **Check .env file**: Ensure API_KEY is correctly set
2. **Restart server**: Server must be restarted after .env changes
3. **Check request headers**: Use `X-API-Key` header in requests
4. **Verify format**: No extra spaces or quotes around the API key

**Example:**
```env
# ❌ Wrong - extra quotes
API_KEY="my-api-key"

# ✅ Correct - no quotes
API_KEY=my-api-key
```

### Issue: "Redis connection failed"

**Symptoms:**
- Redis connection errors in logs
- Rate limiting falls back to in-memory storage

**Solutions:**
1. **Check Redis service**: Ensure Redis is running
2. **Verify connection details**: Check host, port, and password
3. **Test connection**: Use `redis-cli ping` to test Redis
4. **Check firewall**: Ensure port 6379 is accessible
5. **Fallback works**: In-memory storage will be used automatically

**Troubleshooting:**
```bash
# Test Redis connection
redis-cli ping
# Should return: PONG

# Test with specific host/port
redis-cli -h localhost -p 6379 ping
```

### Issue: "File not found or not loading"

**Symptoms:**
- Environment variables not loaded
- Configuration errors

**Solutions:**
1. **Check file location**: `.env` must be in project root
2. **Check file name**: Must be exactly `.env` (not `.env.txt`)
3. **Check file permissions**: Ensure file is readable
4. **Restart application**: Restart after creating/modifying .env

## Security Best Practices

### 1. Never Commit .env Files
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
```

### 2. Use Strong API Keys
```env
# ❌ Weak - too simple
API_KEY=123456

# ✅ Strong - complex and unique
API_KEY=flask-email-server-2024-secure-key-abc123def456
```

### 3. Regular Password Rotation
- Rotate app passwords every 3-6 months
- Rotate API keys when team members change
- Monitor for unauthorized access

### 4. Environment Separation
```env
# Development
MAIL_USERNAME=dev@gmail.com
API_KEY=dev-api-key
REDIS_HOST=localhost

# Production (use different file or environment)
MAIL_USERNAME=prod@gmail.com
API_KEY=prod-api-key
REDIS_HOST=redis-prod.example.com
```

### 5. Redis Security (if using Redis)
```env
# Use strong Redis passwords
REDIS_PASSWORD=strong-redis-password-123

# Restrict Redis access
REDIS_HOST=127.0.0.1  # Only local access
# Or use Redis ACLs for more granular control
```

## Testing Your Configuration

### 1. Basic Test
```bash
# Test if .env is loaded
python -c "from config import Config; print('MAIL_USERNAME:', Config.MAIL_USERNAME)"
```

### 2. Email Test
```bash
# Test email functionality
python test_email_short.py
```

### 3. Configuration Test
```bash
# Test configuration loading
python -c "from config import Config; print('Config loaded successfully')"
```

### 4. Redis Test (if configured)
```bash
# Test Redis connection
python -c "from config import Config; print('Redis host:', Config.REDIS_HOST)"
```

## Advanced Configuration

### Custom SMTP Settings
```env
# Override default SMTP settings if needed
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
```

### Multiple Environment Files
```bash
# Development
cp .env .env.development

# Production
cp .env .env.production

# Load specific environment
export ENV_FILE=.env.production
```

### Redis Cluster Configuration
```env
# For Redis Cluster or Sentinel
REDIS_HOST=redis-cluster.example.com
REDIS_PORT=7000
REDIS_DB=0
REDIS_PASSWORD=cluster-password
```

## Production Recommendations

### 1. Always Use Redis
- **Redis is strongly recommended for production**
- Provides persistent rate limiting across server restarts
- Handles high-traffic scenarios better
- More reliable than in-memory storage

### 2. Production Environment Variables
```env
FLASK_ENV=production
FLASK_DEBUG=False
REDIS_HOST=redis-prod.example.com
REDIS_PASSWORD=strong-production-password
```

### 3. Docker Production Setup
```bash
# Use docker-compose for production
docker-compose -f docker-compose.yml up -d

# Or deploy with Redis separately
docker run -d --name redis-prod -p 6379:6379 redis:7-alpine
```

## Troubleshooting Checklist

- [ ] 2-Factor Authentication enabled
- [ ] App password generated for "Mail"
- [ ] App password copied completely (16 characters)
- [ ] App password base64 encoded correctly
- [ ] .env file created in project root
- [ ] .env file contains correct values
- [ ] No extra spaces or quotes in .env
- [ ] Flask server restarted after changes
- [ ] Gmail account (not domain email) used as MAIL_USERNAME
- [ ] API key matches between .env and requests
- [ ] Redis service running (if configured)
- [ ] Redis connection details correct
- [ ] Rate limiting configuration set

## Getting Help

If you're still experiencing issues:

1. **Check the logs**: Look for specific error messages
2. **Verify each step**: Go through the setup process again
3. **Test with simple values**: Use basic passwords/keys first
4. **Check Gmail status**: Ensure Gmail services are working
5. **Review security settings**: Verify Google Account security configuration
6. **Test Redis separately**: Verify Redis connection independently
7. **Check fallback behavior**: In-memory storage should work if Redis fails

## Resources

- [Google Account Security](https://myaccount.google.com/security)
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)
- [Base64 Encoding Tools](https://www.base64encode.org/)
- [Environment Variables Best Practices](https://12factor.net/config)
- [Redis Documentation](https://redis.io/documentation)
- [Redis Installation Guide](https://redis.io/download)
- [Docker Redis](https://hub.docker.com/_/redis)
