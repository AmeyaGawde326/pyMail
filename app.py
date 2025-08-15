from flask import Flask, request, jsonify
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from config import Config
from templates import VALID_EMAIL_TYPES, get_template_description
from utils import validate_email_request, validate_api_key, create_error_response
from email_service import EmailService

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
email_service = EmailService(mail)

# Initialize rate limiter with Redis or fallback to memory
def get_storage_uri():
    """Get storage URI for rate limiting - Redis if available, memory as fallback"""
    try:
        import redis
        # Test Redis connection
        r = redis.Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            db=app.config['REDIS_DB'],
            password=app.config['REDIS_PASSWORD'],
            socket_connect_timeout=2,
            socket_timeout=2
        )
        r.ping()
        print("✅ Redis connected successfully for rate limiting")
        if app.config['REDIS_PASSWORD']:
            return f"redis://:{app.config['REDIS_PASSWORD']}@{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}/{app.config['REDIS_DB']}"
        else:
            return f"redis://{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}/{app.config['REDIS_DB']}"
    except Exception as e:
        print(f"⚠️ Redis connection failed, falling back to in-memory storage: {e}")
        return "memory://"

# Get storage URI and determine storage type
storage_uri = get_storage_uri()
storage_type = 'redis' if 'redis://' in storage_uri else 'memory'

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=storage_uri
)

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
@limiter.limit(f"{app.config['RATE_LIMIT']} per second")
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
    sender_name = data.get('sender_name')
    sender_email = data.get('sender_email')
    
    # Send email using email service
    return email_service.send_email(receiver_email, email_type, variables, sender_name, sender_email)

@app.route('/email-types', methods=['GET'])
@limiter.limit(f"{app.config['RATE_LIMIT']} per second")
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
        'email_types_count': len(VALID_EMAIL_TYPES),
        'rate_limiting': {
            'limit': f"{app.config['RATE_LIMIT']} per second",
            'storage': storage_type
        }
    })

# Error handler for rate limit exceeded
@app.errorhandler(429)
def ratelimit_handler(e):
    return create_error_response("Rate limit exceeded. Please try again later.", 429)

if __name__ == '__main__':
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("Warning: MAIL_USERNAME or MAIL_PASSWORD not set in environment variables")
        print("Please check your .env file configuration")
    
    app.run(host='0.0.0.0', port=5000)
