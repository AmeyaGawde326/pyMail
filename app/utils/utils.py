from flask import jsonify
from ..templates.templates import TEMPLATE_MAP, TEMPLATE_VARIABLES, VALID_EMAIL_TYPES, is_valid_email_type

def validate_email_request(data):
    """Validate email request data and return errors if any"""
    errors = []
    
    if not data:
        errors.append("No data provided")
        return errors
    
    receiver_email = data.get('receiver_email')
    email_type = data.get('email_type')
    variables = data.get('variables', {})
    sender_email = data.get('sender_email')
    
    if not receiver_email:
        errors.append("Receiver email is required")
    
    if not sender_email:
        errors.append("Sender email is required")
    
    if not email_type:
        errors.append("Email type is required")
    elif not is_valid_email_type(email_type):
        errors.append(f"Email type '{email_type}' is not valid. Valid types: {VALID_EMAIL_TYPES}")
    
    if email_type in TEMPLATE_VARIABLES:
        required_vars = TEMPLATE_VARIABLES[email_type]
        missing_vars = []
        for var in required_vars:
            if var not in variables:
                missing_vars.append(var)
        
        if missing_vars:
            errors.append(f"Missing required variables for email type '{email_type}': {missing_vars}")
    
    return errors

def render_template(template_body, variables):
    """Render email template with placeholder variables"""
    rendered = template_body
    
    for key, value in variables.items():
        if isinstance(value, str):
            rendered = rendered.replace(f'{{{{{key}}}}}', value)
        elif isinstance(value, (int, float)):
            rendered = rendered.replace(f'{{{{{key}}}}}', str(value))
        elif isinstance(value, list):
            if key == 'items':
                items_html = ''
                for item in value:
                    items_html += f'<li>{item.get("name", "")} - ${item.get("price", "")}</li>'
                rendered = rendered.replace('{% for item in items %}\n                <li>{{item.name}} - ${{item.price}}</li>\n                {% endfor %}', items_html)
    
    return rendered

def create_success_response(message, email_type, subject):
    """Create standardized success response"""
    return jsonify({
        'success': True,
        'message': message,
        'email_type': email_type,
        'subject': subject
    }), 200

def create_error_response(message, status_code=400):
    """Create standardized error response"""
    return jsonify({'error': message}), status_code

def validate_api_key(request):
    """Validate API key from request headers"""
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return False, "API key is required"
    
    import os
    expected_key = os.getenv('API_KEY')
    
    if not expected_key:
        return False, "API key not configured on server"
    
    if api_key != expected_key:
        return False, "Invalid API key"
    
    return True, None
