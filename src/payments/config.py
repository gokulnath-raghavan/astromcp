"""
Payment configuration settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Stripe API Keys
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Payment Plans
PAYMENT_PLANS = {
    'basic': {
        'name': 'Basic Reading',
        'price': 29.99,
        'description': 'Basic astrological reading with general insights',
        'features': [
            'Basic birth chart analysis',
            'General horoscope',
            'Basic transit predictions',
            'Email support'
        ]
    },
    'premium': {
        'name': 'Premium Reading',
        'price': 59.99,
        'description': 'Detailed astrological reading with personalized insights',
        'features': [
            'Detailed birth chart analysis',
            'Personalized horoscope',
            'Advanced transit predictions',
            'Relationship compatibility',
            'Priority email support',
            '30-minute consultation'
        ]
    },
    'enterprise': {
        'name': 'Enterprise Reading',
        'price': 99.99,
        'description': 'Comprehensive astrological reading with full consultation',
        'features': [
            'Comprehensive birth chart analysis',
            'Detailed personalized horoscope',
            'Advanced transit predictions',
            'Relationship compatibility',
            'Career guidance',
            '24/7 priority support',
            '1-hour consultation',
            'Follow-up session'
        ]
    }
}

# Currency settings
CURRENCY = 'usd'

# Payment success/failure URLs
PAYMENT_SUCCESS_URL = '/payment/success'
PAYMENT_CANCEL_URL = '/payment/cancel'

# Webhook endpoint
WEBHOOK_ENDPOINT = '/webhook/stripe' 