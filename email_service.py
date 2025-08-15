from flask_mail import Message
from templates import TEMPLATE_MAP, get_template_by_type, is_valid_email_type
from utils import render_template, create_success_response, create_error_response

class EmailService:
    def __init__(self, mail):
        self.mail = mail
    
    def send_email(self, receiver_email, email_type, variables, sender_name=None, sender_email=None):
        """Send email using specified email type and variables"""
        try:
            if not is_valid_email_type(email_type):
                return create_error_response(f"Email type '{email_type}' is not valid")
            
            template = get_template_by_type(email_type)
            if not template:
                return create_error_response(f"Template not found for email type '{email_type}'")
            
            subject = render_template(template['subject'], variables)
            body = render_template(template['body'], variables)
            
            # Set sender with name and email
            if sender_name and sender_email:
                sender = f"{sender_name} <{sender_email}>"
            elif sender_email:
                sender = sender_email
            else:
                return create_error_response("Sender email is required")
            
            msg = Message(
                subject=subject,
                recipients=[receiver_email],
                html=body,
                sender=sender
            )
            
            self.mail.send(msg)
            
            return create_success_response(
                f"Email sent successfully to {receiver_email}",
                email_type,
                subject
            )
            
        except Exception as e:
            return create_error_response(f"Failed to send email: {str(e)}", 500)
    
    def send_welcome_email(self, receiver_email, name, email, login_url, sender_name, sender_email):
        """Send welcome email to new users"""
        variables = {
            'name': name,
            'email': email,
            'login_url': login_url
        }
        return self.send_email(receiver_email, 'welcome_email', variables, sender_name, sender_email)
    
    def send_account_confirmation_email(self, receiver_email, name, verification_url, sender_name, sender_email, expiry_hours=1):
        """Send account confirmation email"""
        variables = {
            'name': name,
            'verification_url': verification_url,
            'expiry_hours': expiry_hours
        }
        return self.send_email(receiver_email, 'account_confirmation_email', variables, sender_name, sender_email)
    
    def send_password_reset_email(self, receiver_email, name, reset_link, sender_name, sender_email, expiry_hours=24):
        """Send password reset email"""
        variables = {
            'name': name,
            'reset_link': reset_link,
            'expiry_hours': expiry_hours
        }
        return self.send_email(receiver_email, 'password_reset_email', variables, sender_name, sender_email)
    
    def send_access_key_email(self, receiver_email, name, service_name, access_key, 
                            generated_date, expiry_date, sender_name, sender_email, expiry_hours=72):
        """Send access key email"""
        variables = {
            'name': name,
            'service_name': service_name,
            'access_key': access_key,
            'generated_date': generated_date,
            'expiry_date': expiry_date,
            'expiry_hours': expiry_hours
        }
        return self.send_email(receiver_email, 'access_key_email', variables, sender_name, sender_email)
    
    def send_invoice_email(self, receiver_email, customer_name, customer_email, invoice_number,
                          invoice_date, due_date, total_amount, company_name, payment_link,
                          payment_terms, notes, sender_name, sender_email):
        """Send invoice email"""
        variables = {
            'customer_name': customer_name,
            'customer_email': customer_email,
            'invoice_number': invoice_number,
            'invoice_date': invoice_date,
            'due_date': due_date,
            'total_amount': total_amount,
            'company_name': company_name,
            'payment_link': payment_link,
            'payment_terms': payment_terms,
            'notes': notes
        }
        return self.send_email(receiver_email, 'invoice_email', variables, sender_name, sender_email)
