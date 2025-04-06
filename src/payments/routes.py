"""
Payment routes for handling payment-related endpoints
"""

from flask import Blueprint, render_template, jsonify, request
from .handler import create_checkout_session, handle_webhook
from .config import PAYMENT_PLANS, PAYMENT_SUCCESS_URL, PAYMENT_CANCEL_URL

bp = Blueprint('payments', __name__)

@bp.route('/pricing')
def pricing():
    """
    Display pricing page with available plans
    """
    return render_template('pricing.html', plans=PAYMENT_PLANS)

@bp.route('/create-checkout-session', methods=['POST'])
def checkout():
    """
    Create a new checkout session
    """
    data = request.get_json()
    plan_id = data.get('plan_id')
    
    if not plan_id:
        return jsonify({'error': 'Plan ID is required'}), 400
        
    return create_checkout_session(plan_id)

@bp.route('/webhook/stripe', methods=['POST'])
def webhook():
    """
    Handle Stripe webhook events
    """
    return handle_webhook()

@bp.route(PAYMENT_SUCCESS_URL)
def success():
    """
    Handle successful payment
    """
    return render_template('payment_success.html')

@bp.route(PAYMENT_CANCEL_URL)
def cancel():
    """
    Handle cancelled payment
    """
    return render_template('payment_cancel.html') 