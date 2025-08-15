# Custom Email Templates Guide

## Overview
This guide explains how to create and add custom email templates to your Flask email server. The system uses a modular template structure that makes it easy to add new email types.

## Template Structure

### Current Template System
The email server uses a centralized template management system in `templates.py`:

```python
# Template mapping structure
TEMPLATE_MAP = {
    "welcome_email": welcome_email,
    "account_confirmation_email": account_confirmation_email,
    "password_reset_email": password_reset_email,
    "access_key_email": access_key_email,
    "invoice_email": invoice_email
}

# Valid email types list
VALID_EMAIL_TYPES = list(TEMPLATE_MAP.keys())
```

## Adding a New Email Template

### Step 1: Create the Template Function

Add a new template function in `templates.py`:

```python
def newsletter_email():
    """Newsletter email template"""
    return {
        "subject": "{{subject}} - Newsletter",
        "body": """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Newsletter</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .header { background: #007bff; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; }
                .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; }
                .button { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{{company_name}} Newsletter</h1>
            </div>
            
            <div class="content">
                <h2>Hello {{name}},</h2>
                
                <p>{{newsletter_content}}</p>
                
                {% if call_to_action_url %}
                <p style="text-align: center;">
                    <a href="{{call_to_action_url}}" class="button">{{call_to_action_text}}</a>
                </p>
                {% endif %}
                
                <p>Best regards,<br>{{company_name}} Team</p>
            </div>
            
            <div class="footer">
                <p>You're receiving this email because you subscribed to our newsletter.</p>
                <p><a href="{{unsubscribe_url}}">Unsubscribe</a> | <a href="{{company_website}}">Visit our website</a></p>
            </div>
        </body>
        </html>
        """
    }
```

### Step 2: Add Template to Mapping

Update the `TEMPLATE_MAP` in `templates.py`:

```python
# Add your new template to the mapping
TEMPLATE_MAP = {
    "welcome_email": welcome_email,
    "account_confirmation_email": account_confirmation_email,
    "password_reset_email": password_reset_email,
    "access_key_email": access_key_email,
    "invoice_email": invoice_email,
    "newsletter_email": newsletter_email  # Add this line
}
```

### Step 3: Update Valid Email Types

The `VALID_EMAIL_TYPES` list is automatically updated when you modify `TEMPLATE_MAP`, but you can also add it explicitly:

```python
# This is automatically generated, but you can add it explicitly if needed
VALID_EMAIL_TYPES = [
    "welcome_email",
    "account_confirmation_email", 
    "password_reset_email",
    "access_key_email",
    "invoice_email",
    "newsletter_email"  # Add this line
]
```

### Step 4: Add Template Description

Update the `get_template_description` function to include your new template:

```python
def get_template_description(email_type):
    """Get description for email type"""
    descriptions = {
        "welcome_email": "Welcome email for new users with name, email, and login URL placeholders",
        "account_confirmation_email": "Email confirmation with name, verification URL, and expiry time placeholders",
        "password_reset_email": "Password reset email with name, reset link, and expiry time placeholders",
        "access_key_email": "Access key generation email with service details and expiry information",
        "invoice_email": "Invoice email with customer details, invoice information, and payment details",
        "newsletter_email": "Newsletter email with company branding and customizable content"  # Add this line
    }
    return descriptions.get(email_type, "No description available")
```

## Template Variables

### Understanding Template Variables
Templates use Jinja2 syntax with double curly braces `{{variable_name}}` for variable substitution.

### Required vs Optional Variables
- **Required variables**: Must be provided in the API request
- **Optional variables**: Can be omitted (use `{% if variable %}` for conditional rendering)

### Example Template with Variables
```python
def order_confirmation_email():
    """Order confirmation email template"""
    return {
        "subject": "Order Confirmation - {{order_number}}",
        "body": """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Order Confirmation</title>
            <style>
                body { font-family: Arial, sans-serif; }
                .order-details { background: #f8f9fa; padding: 15px; margin: 20px 0; }
                .total { font-weight: bold; font-size: 18px; color: #007bff; }
            </style>
        </head>
        <body>
            <h1>Thank you for your order!</h1>
            
            <p>Hello {{customer_name}},</p>
            
            <p>Your order has been confirmed and is being processed.</p>
            
            <div class="order-details">
                <h3>Order Details:</h3>
                <p><strong>Order Number:</strong> {{order_number}}</p>
                <p><strong>Order Date:</strong> {{order_date}}</p>
                <p><strong>Total Amount:</strong> <span class="total">{{total_amount}}</span></p>
                
                {% if estimated_delivery %}
                <p><strong>Estimated Delivery:</strong> {{estimated_delivery}}</p>
                {% endif %}
            </div>
            
            {% if tracking_number %}
            <p><strong>Tracking Number:</strong> {{tracking_number}}</p>
            {% endif %}
            
            <p>You can track your order at: <a href="{{tracking_url}}">{{tracking_url}}</a></p>
            
            <p>Best regards,<br>{{company_name}} Team</p>
        </body>
        </html>
        """
    }
```

## Template Best Practices

### 1. HTML Structure
- Use semantic HTML5 elements
- Include proper DOCTYPE and meta tags
- Ensure responsive design with CSS

### 2. CSS Styling
- Use inline CSS for email client compatibility
- Keep styles simple and widely supported
- Test across different email clients

### 3. Variable Naming
- Use descriptive, lowercase variable names
- Separate words with underscores
- Be consistent with existing templates

### 4. Conditional Rendering
- Use `{% if variable %}` for optional content
- Provide fallbacks for missing variables
- Handle edge cases gracefully

### 5. Accessibility
- Use proper heading hierarchy
- Include alt text for images
- Ensure sufficient color contrast
- Use readable font sizes

## Testing Your New Template

### 1. Test the Template Function
```python
# In Python console or test script
from templates import get_template_by_type
template = get_template_by_type("newsletter_email")
print(template["subject"])
print(template["body"])
```

### 2. Test Variable Substitution
```python
from utils import render_template

# Test variables
variables = {
    "name": "John Doe",
    "company_name": "Example Corp",
    "newsletter_content": "This is our monthly newsletter content.",
    "call_to_action_url": "https://example.com/newsletter",
    "call_to_action_text": "Read More"
}

# Render template
subject = render_template(template["subject"], variables)
body = render_template(template["body"], variables)

print("Subject:", subject)
print("Body:", body)
```

### 3. Test API Endpoint
```bash
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "receiver_email": "test@example.com",
    "email_type": "newsletter_email",
    "sender_name": "Example Corp",
    "sender_email": "newsletter@example.com",
    "variables": {
        "name": "John Doe",
        "company_name": "Example Corp",
        "newsletter_content": "This is our monthly newsletter content.",
        "call_to_action_url": "https://example.com/newsletter",
        "call_to_action_text": "Read More"
    }
  }'
```

## Advanced Template Features

### 1. Loops
```python
# In your template
{% for item in order_items %}
<div class="item">
    <h4>{{item.name}}</h4>
    <p>Quantity: {{item.quantity}}</p>
    <p>Price: {{item.price}}</p>
</div>
{% endfor %}
```

### 2. Filters
```python
# Format dates, numbers, etc.
{{order_date|strftime('%B %d, %Y')}}
{{total_amount|round(2)}}
{{customer_name|title}}
```

### 3. Macros
```python
{# Define reusable components #}
{% macro button(text, url, style="primary") %}
<a href="{{url}}" class="btn btn-{{style}}">{{text}}</a>
{% endmacro %}

{# Use the macro #}
{{ button("View Order", order_url, "success") }}
```

## Template Examples

### Simple Notification Email
```python
def notification_email():
    """Simple notification email"""
    return {
        "subject": "{{notification_title}}",
        "body": """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{notification_title}}</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                .notification { background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; }
            </style>
        </head>
        <body>
            <div class="notification">
                <h2>{{notification_title}}</h2>
                <p>{{notification_message}}</p>
                
                {% if action_url %}
                <p><a href="{{action_url}}">{{action_text}}</a></p>
                {% endif %}
            </div>
        </body>
        </html>
        """
    }
```

### Marketing Email
```python
def marketing_email():
    """Marketing/promotional email"""
    return {
        "subject": "{{promotion_title}} - Limited Time Offer!",
        "body": """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{promotion_title}}</title>
            <style>
                body { font-family: Arial, sans-serif; }
                .hero { background: linear-gradient(45deg, #ff6b6b, #4ecdc4); color: white; padding: 40px; text-align: center; }
                .cta-button { background: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-size: 18px; }
            </style>
        </head>
        <body>
            <div class="hero">
                <h1>{{promotion_title}}</h1>
                <p>{{promotion_description}}</p>
                <a href="{{cta_url}}" class="cta-button">{{cta_text}}</a>
            </div>
            
            <div style="padding: 20px;">
                <h2>Offer Details:</h2>
                <ul>
                    {% for detail in offer_details %}
                    <li>{{detail}}</li>
                    {% endfor %}
                </ul>
                
                <p><strong>Expires:</strong> {{expiry_date}}</p>
            </div>
        </body>
        </html>
        """
    }
```

## Troubleshooting

### Common Issues

1. **Template not found**: Ensure the template is added to `TEMPLATE_MAP`
2. **Variable errors**: Check variable names and required variables
3. **Rendering issues**: Test template rendering separately
4. **Email client compatibility**: Test across different email clients

### Debug Tips

1. **Print template content**: Use `print(template["body"])` to see raw template
2. **Test variables**: Create a simple test with minimal variables
3. **Check syntax**: Ensure proper Jinja2 syntax
4. **Validate HTML**: Use HTML validators for complex templates

## Next Steps

After creating your custom template:

1. **Test thoroughly** with various variable combinations
2. **Update documentation** to include your new email type
3. **Add validation** for required variables in your application
4. **Monitor usage** to ensure the template works as expected
5. **Iterate and improve** based on user feedback

## Resources

- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [Email HTML Best Practices](https://www.emailonacid.com/blog/)
- [CSS Email Client Support](https://www.campaignmonitor.com/css/)
- [HTML Email Templates](https://github.com/mailgun/transactional-email-templates)
