# Gmail Domain Email Setup Guide

## Overview
This guide will help you set up a custom domain email address (e.g., `contact@yourdomain.com`) using Cloudflare Email Routing and Gmail, then configure your Flask email server to send emails from that domain address.

## Prerequisites
- A Gmail account
- A Cloudflare account (free)
- A custom domain name from any registrar (GoDaddy, Namecheap, etc.)

## Step-by-Step Setup

### Step 1: Domain Setup in Cloudflare

#### 1.1 Add Your Domain to Cloudflare
1. Log in to your Cloudflare account
2. Click **Add a Site**
3. Enter your domain name and click **Add Site**
4. Choose the **Free** plan
5. Cloudflare will provide you with two nameservers

#### 1.2 Update Your Domain Registrar
1. Go to your domain registrar's DNS settings
2. Replace the existing nameservers with Cloudflare's nameservers
3. Wait for DNS propagation (can take up to 24 hours)

#### 1.3 Verify Domain Activation
1. Return to Cloudflare dashboard
2. Wait for the orange cloud icon to appear (indicating Cloudflare is active)
3. Ensure all DNS records are properly configured

### Step 2: Email Routing Setup in Cloudflare

#### 2.1 Access Email Routing
1. In your Cloudflare dashboard, click **Email** in the left sidebar
2. Click on the **Email Routing** tab
3. Click **Create address**

#### 2.2 Create Custom Email Address
1. **Custom address**: Enter your desired email (e.g., `contact@yourdomain.com`)
2. **Destination address**: Enter your Gmail address where you want to receive emails
3. Click **Save**

#### 2.3 Verify Email Address
1. Check your Gmail inbox for a verification email from Cloudflare
2. Click the verification link to confirm your email address
3. Wait for verification to complete

### Step 3: Gmail Configuration

#### 3.1 Enable 2-Factor Authentication
1. Go to your [Google Account settings](https://myaccount.google.com/)
2. Click **Security** in the left sidebar
3. Under "Signing in to Google," click **2-Step Verification**
4. Follow the steps to enable 2FA

#### 3.2 Generate App Password
1. Return to **Security** page
2. Click **App passwords** (under 2-Step Verification)
3. Select **Mail** from the "Select app" dropdown
4. Select **Other (Custom name)** from the "Select device" dropdown
5. Enter a name (e.g., "Flask Email Server")
6. Click **Generate**
7. **Copy the generated password** and save it securely

#### 3.3 Configure "Send Mail As" in Gmail
1. Go to [Gmail settings](https://mail.google.com/mail/u/0/#settings/general)
2. Click **Accounts and Import** tab
3. Under "Send mail as," click **Add another email address**
4. Enter your custom domain email (e.g., `contact@yourdomain.com`)
5. Click **Next Step**
6. **SMTP Server**: `smtp.gmail.com`
7. **Port**: `587`
8. **Username**: Your Gmail address
9. **Password**: The app password you generated in step 3.2
10. **Security**: Select "TLS"
11. Click **Add Account**
12. Check your Gmail inbox for a verification email and click the verification link

### Step 4: Flask Server Configuration

#### 4.1 Update Your .env File
```bash
# Google SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=yourname@gmail.com
MAIL_PASSWORD=base64-encoded-app-password
API_KEY=your-api-key-here
```

**Important Notes:**
- `MAIL_USERNAME` must be your **Gmail account**, not the domain email
- `MAIL_PASSWORD` must be the **app password** you generated, not your regular Gmail password
- The domain email will be used as `sender_email` in your API requests

#### 4.2 Encode Your App Password
```bash
# Windows PowerShell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your-app-password"))

# Linux/macOS
echo -n "your-app-password" | base64

# Python
import base64
password = "your-app-password"
encoded = base64.b64encode(password.encode('utf-8')).decode('utf-8')
print(encoded)
```

### Step 5: Testing Your Setup

#### 5.1 Test Basic Email Functionality
```bash
python test_email_short.py
```

#### 5.2 Test Domain Email Functionality
```bash
python test_domain_email.py
```

#### 5.3 Verify Email Sending
1. Check that emails are sent successfully
2. Verify the "From" field shows your domain email
3. Check that emails are delivered to recipients

## API Usage Examples

### Send Email Using Domain Address
```json
POST /send-email
{
  "receiver_email": "recipient@example.com",
  "email_type": "welcome_email",
  "variables": {
    "name": "John Doe",
    "email": "john@example.com",
    "login_url": "https://yourdomain.com/login"
  },
  "sender_name": "Your Company",
  "sender_email": "contact@yourdomain.com"
}
```

### Available Email Types
- `welcome_email` - Welcome emails for new users
- `account_confirmation_email` - Account verification emails
- `password_reset_email` - Password reset emails
- `access_key_email` - Access key generation emails
- `invoice_email` - Invoice emails

## Troubleshooting

### Common Issues

#### "Username and Password not accepted"
- Ensure `MAIL_USERNAME` is your Gmail account, not domain email
- Verify you're using the app password, not your regular Gmail password
- Check that 2FA is enabled and app password is generated

#### "Domain not verified"
- Wait for DNS propagation (up to 24 hours)
- Verify Cloudflare is active (orange cloud icon)
- Check that nameservers are correctly updated at your registrar

#### "Email not sending"
- Verify SMTP settings in your .env file
- Check that the domain email is properly set up in Gmail
- Ensure the app password is correctly encoded

### Verification Checklist
- [ ] Domain is active in Cloudflare
- [ ] Email routing is configured
- [ ] Gmail 2FA is enabled
- [ ] App password is generated
- [ ] "Send mail as" is configured in Gmail
- [ ] .env file has correct Gmail credentials
- [ ] App password is base64 encoded
- [ ] Flask server starts without errors
- [ ] Test emails are sent successfully
- [ ] Domain email appears in "From" field

## Security Best Practices

1. **Never share your app password**
2. **Use environment variables** for sensitive data
3. **Enable 2FA** on your Google account
4. **Regularly rotate app passwords**
5. **Monitor email sending logs**
6. **Use HTTPS** for API endpoints in production

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all steps in the verification checklist
3. Check Cloudflare and Gmail status pages
4. Review your .env file configuration
5. Test with the provided test scripts

## Next Steps

After successful setup:
1. Integrate the email API into your applications
2. Set up monitoring and logging
3. Configure rate limiting if needed
4. Set up backup email providers for production use
5. Implement email templates for your specific use cases
