# Email template type keys
WELCOME_EMAIL_KEY = "welcome_email"
ACCOUNT_CONFIRMATION_KEY = "account_confirmation_email"
PASSWORD_RESET_KEY = "password_reset_email"
ACCESS_KEY_KEY = "access_key_email"
INVOICE_KEY = "invoice_email"

# Individual email templates
welcome_email = {
    'subject': 'Welcome to Our Service!',
    'body': '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Welcome to Our Service</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background: linear-gradient(135deg, #E4405F 0%, #833AB4 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }
            .content {
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }
            .button {
                display: inline-block;
                background: linear-gradient(135deg, #E4405F 0%, #833AB4 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 20px 0;
            }
            .footer {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Welcome to Our Service</h1>
            <p>Your Account Has Been Created</p>
        </div>
        <div class="content">
            <h2>Welcome {{name}}!</h2>
            <p>Thank you for joining our service. We're excited to have you on board!</p>
            
            <p>Your account has been successfully created with email: <strong>{{email}}</strong></p>
            
            <div style="text-align: center;">
                <a href="{{login_url}}" class="button">Get Started</a>
            </div>
            
            <p>If you have any questions, feel free to reach out to our support team.</p>
            
            <p>We look forward to helping you succeed!</p>
        </div>
        <div class="footer">
            <p>This email was sent by Our Service. Please do not reply to this email.</p>
            <p>If you have any questions, please contact our support team.</p>
        </div>
    </body>
    </html>
    '''
}

account_confirmation_email = {
    'subject': 'Confirm Your Email Address',
    'body': '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Confirm Your Email</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background: linear-gradient(135deg, #E4405F 0%, #833AB4 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }
            .content {
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }
            .button {
                display: inline-block;
                background: linear-gradient(135deg, #E4405F 0%, #833AB4 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 20px 0;
            }
            .footer {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Confirm Your Email</h1>
            <p>Complete Your Registration</p>
        </div>
        <div class="content">
            <h2>Welcome {{name}}!</h2>
            <p>Thank you for registering with our service. To complete your registration and start using our platform, please confirm your email address by clicking the button below:</p>
            
            <div style="text-align: center;">
                <a href="{{verification_url}}" class="button">Confirm Email Address</a>
            </div>
            
            <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
            <p style="word-break: break-all; background: #f0f0f0; padding: 10px; border-radius: 5px;">
                {{verification_url}}
            </p>
            
            <p><strong>Important:</strong> This link will expire in {{expiry_hours}} hour(s) for security reasons.</p>
            
            <p>If you didn't create an account with us, you can safely ignore this email.</p>
        </div>
        <div class="footer">
            <p>This email was sent by Our Service. Please do not reply to this email.</p>
            <p>If you have any questions, please contact our support team.</p>
        </div>
    </body>
    </html>
    '''
}

password_reset_email = {
    'subject': 'Password Reset Request',
    'body': '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Password Reset Request</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background: linear-gradient(135deg, #E4405F 0%, #833AB4 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }
            .content {
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }
            .button {
                display: inline-block;
                background: linear-gradient(135deg, #E4405F 0%, #833AB4 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 20px 0;
            }
            .warning {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .footer {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Password Reset Request</h1>
            <p>Secure Your Account</p>
        </div>
        <div class="content">
            <h2>Hello {{name}},</h2>
            <p>We received a request to reset your password. Click the button below to proceed:</p>
            
            <div style="text-align: center;">
                <a href="{{reset_link}}" class="button">Reset Password</a>
            </div>
            
            <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
            <p style="word-break: break-all; background: #f0f0f0; padding: 10px; border-radius: 5px;">
                {{reset_link}}
            </p>
            
            <div class="warning">
                <strong>Security Notice:</strong> This link will expire in {{expiry_hours}} hour(s). If you didn't request this password reset, please ignore this email and ensure your account is secure.
            </div>
        </div>
        <div class="footer">
            <p>This email was sent by Our Service. Please do not reply to this email.</p>
            <p>If you have any questions, please contact our support team.</p>
        </div>
    </body>
    </html>
    '''
}

access_key_email = {
    'subject': 'Your Access Key - {{service_name}}',
    'body': '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Access Key Generated</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background: linear-gradient(135deg, #E4405F 0%, #833AB4 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }
            .content {
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }
            .key-box {
                background: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
                font-family: 'Courier New', monospace;
                font-size: 18px;
                font-weight: bold;
                color: #495057;
            }
            .warning {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .footer {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Access Key Generated</h1>
            <p>{{service_name}}</p>
        </div>
        <div class="content">
            <h2>Hello {{name}},</h2>
            <p>Your access key for <strong>{{service_name}}</strong> has been generated successfully.</p>
            
            <div class="key-box">
                {{access_key}}
            </div>
            
            <p><strong>Service Details:</strong></p>
            <ul>
                <li><strong>Service:</strong> {{service_name}}</li>
                <li><strong>Generated:</strong> {{generated_date}}</li>
                <li><strong>Expires:</strong> {{expiry_date}}</li>
            </ul>
            
            <div class="warning">
                <strong>Important:</strong> Keep this access key secure and do not share it with anyone. This key will expire in {{expiry_hours}} hour(s).
            </div>
            
            <p>Use this key to authenticate with our API or access the service.</p>
        </div>
        <div class="footer">
            <p>This email was sent by Our Service. Please do not reply to this email.</p>
            <p>If you have any questions, please contact our support team.</p>
        </div>
    </body>
    </html>
    '''
}

invoice_email = {
    'subject': 'Invoice #{{invoice_number}} - {{company_name}}',
    'body': '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Invoice #{{invoice_number}}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background: linear-gradient(135deg, #E4405F 0%, #833AB4 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }
            .content {
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }
            .invoice-details {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }
            .total-box {
                background: #e3f2fd;
                border: 2px solid #2196f3;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
            }
            .button {
                display: inline-block;
                background: linear-gradient(135deg, #E4405F 0%, #833AB4 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 20px 0;
            }
            .footer {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Invoice</h1>
            <p>{{company_name}}</p>
        </div>
        <div class="content">
            <h2>Invoice #{{invoice_number}}</h2>
            <p>Hello {{customer_name}},</p>
            <p>Thank you for your business. Please find your invoice attached below.</p>
            
            <div class="invoice-details">
                <h3>Invoice Details</h3>
                <p><strong>Invoice Date:</strong> {{invoice_date}}</p>
                <p><strong>Due Date:</strong> {{due_date}}</p>
                <p><strong>Customer:</strong> {{customer_name}}</p>
                <p><strong>Email:</strong> {{customer_email}}</p>
            </div>
            
            <div class="total-box">
                <h3>Total Amount Due</h3>
                <h2 style="color: #2196f3; margin: 10px 0;">${{total_amount}}</h2>
            </div>
            
            <div style="text-align: center;">
                <a href="{{payment_link}}" class="button">Pay Now</a>
            </div>
            
            <p><strong>Payment Terms:</strong> {{payment_terms}}</p>
            <p><strong>Notes:</strong> {{notes}}</p>
        </div>
        <div class="footer">
            <p>This email was sent by {{company_name}}. Please do not reply to this email.</p>
            <p>If you have any questions, please contact our billing team.</p>
        </div>
    </body>
    </html>
    '''
}

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

# Template variable mappings
TEMPLATE_VARIABLES = {
    WELCOME_EMAIL_KEY: ['name', 'email', 'login_url'],
    ACCOUNT_CONFIRMATION_KEY: ['name', 'verification_url', 'expiry_hours'],
    PASSWORD_RESET_KEY: ['name', 'reset_link', 'expiry_hours'],
    ACCESS_KEY_KEY: ['name', 'service_name', 'access_key', 'generated_date', 'expiry_date', 'expiry_hours'],
    INVOICE_KEY: ['customer_name', 'customer_email', 'invoice_number', 'invoice_date', 'due_date', 'total_amount', 'company_name', 'payment_link', 'payment_terms', 'notes']
}

def get_template_description(email_type):
    """Get description for each email type"""
    descriptions = {
        WELCOME_EMAIL_KEY: 'Welcome email for new users with name, email, and login URL placeholders',
        ACCOUNT_CONFIRMATION_KEY: 'Email confirmation with name, verification URL, and expiry time placeholders',
        PASSWORD_RESET_KEY: 'Password reset email with name, reset link, and expiry time placeholders',
        ACCESS_KEY_KEY: 'Access key generation email with service details and expiry information',
        INVOICE_KEY: 'Invoice email with customer details, invoice information, and payment details'
    }
    return descriptions.get(email_type, 'No description available')

def get_template_by_type(email_type):
    """Get template by email type"""
    return TEMPLATE_MAP.get(email_type)

def is_valid_email_type(email_type):
    """Check if email type is valid"""
    return email_type in VALID_EMAIL_TYPES
