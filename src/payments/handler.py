"""
Payment handler for processing payments using Stripe
"""

import stripe
from flask import jsonify, request, current_app
from .config import (
    STRIPE_PUBLIC_KEY,
    STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET,
    PAYMENT_PLANS,
    CURRENCY,
    PAYMENT_SUCCESS_URL,
    PAYMENT_CANCEL_URL
)

stripe.api_key = STRIPE_SECRET_KEY

def create_checkout_session(plan_id):
    """
    Create a Stripe checkout session for the specified plan
    """
    try:
        if plan_id not in PAYMENT_PLANS:
            return jsonify({'error': 'Invalid plan selected'}), 400

        plan = PAYMENT_PLANS[plan_id]
        
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': CURRENCY,
                    'product_data': {
                        'name': plan['name'],
                        'description': plan['description'],
                    },
                    'unit_amount': int(plan['price'] * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.host_url + PAYMENT_SUCCESS_URL,
            cancel_url=request.host_url + PAYMENT_CANCEL_URL,
            metadata={
                'plan_id': plan_id,
                'user_id': request.user.id if hasattr(request, 'user') else None
            }
        )
        
        return jsonify({'sessionId': session.id})
    
    except Exception as e:
        current_app.logger.error(f"Error creating checkout session: {str(e)}")
        return jsonify({'error': 'Error creating checkout session'}), 500

def handle_webhook():
    """
    Handle Stripe webhook events
    """
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)
    elif event['type'] == 'payment_intent.payment_failed':
        session = event['data']['object']
        handle_failed_payment(session)
    
    return jsonify({'status': 'success'})

def handle_successful_payment(session):
    """
    Handle successful payment completion
    """
    try:
        # Get payment details
        plan_id = session['metadata']['plan_id']
        user_id = session['metadata']['user_id']
        
        # Update user's subscription status in database
        # TODO: Implement database update
        
        # Send confirmation email
        # TODO: Implement email sending
        
        current_app.logger.info(f"Payment successful for user {user_id}, plan {plan_id}")
        
    except Exception as e:
        current_app.logger.error(f"Error handling successful payment: {str(e)}")

def handle_failed_payment(session):
    """
    Handle failed payment
    """
    try:
        # Get payment details
        plan_id = session['metadata']['plan_id']
        user_id = session['metadata']['user_id']
        
        # Update payment status in database
        # TODO: Implement database update
        
        # Send failure notification
        # TODO: Implement notification sending
        
        current_app.logger.warning(f"Payment failed for user {user_id}, plan {plan_id}")
        
    except Exception as e:
        current_app.logger.error(f"Error handling failed payment: {str(e)}") 