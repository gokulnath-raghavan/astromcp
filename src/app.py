"""
Main Flask application
"""

from flask import Flask, render_template
from payments.routes import bp as payments_bp
from payments.config import STRIPE_PUBLIC_KEY

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Register blueprints
app.register_blueprint(payments_bp)

@app.route('/')
def index():
    """
    Home page
    """
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """
    User dashboard
    """
    return render_template('dashboard.html')

@app.route('/contact')
def contact():
    """
    Contact page
    """
    return render_template('contact.html')

# Make Stripe public key available to all templates
@app.context_processor
def inject_stripe_key():
    return dict(stripe_public_key=STRIPE_PUBLIC_KEY)

if __name__ == '__main__':
    app.run(debug=True) 