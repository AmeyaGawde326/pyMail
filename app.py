from flask import Flask, request, jsonify
from flask_mail import Mail
from functools import wraps
from config import Config
from templates import VALID_EMAIL_TYPES, get_template_description
from utils import validate_email_request, validate_api_key, create_error_response
from email_service import EmailService

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
email_service = EmailService(mail)

def require_api_key(f):
    """Decorator to require API key for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_valid, error_message = validate_api_key(request)
        if not is_valid:
            return create_error_response(error_message, 401)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/send-email', methods=['POST'])
@require_api_key
def send_email():
    """Send email using email type and variables"""
    data = request.get_json()
    
    # Validate request data
    errors = validate_email_request(data)
    if errors:
        return create_error_response("; ".join(errors))
    
    receiver_email = data.get('receiver_email')
    email_type = data.get('email_type')
    variables = data.get('variables', {})
    
    # Send email using email service
    return email_service.send_email(receiver_email, email_type, variables)

@app.route('/email-types', methods=['GET'])
@require_api_key
def get_email_types():
    """Get list of available email types with descriptions"""
    email_types = {}
    for email_type in VALID_EMAIL_TYPES:
        email_types[email_type] = {
            'description': get_template_description(email_type)
        }
    return jsonify(email_types)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint (no API key required)"""
    return jsonify({
        'status': 'healthy',
        'service': 'Email Server',
        'version': '2.1.0',
        'email_types_count': len(VALID_EMAIL_TYPES)
    })

if __name__ == '__main__':
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("Warning: MAIL_USERNAME or MAIL_PASSWORD not set in environment variables")
        print("Please check your .env file configuration")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
