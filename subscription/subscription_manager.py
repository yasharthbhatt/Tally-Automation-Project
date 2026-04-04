"""
Subscription Management for StockSense
Handles subscription tiers, feature access, and payment integration
"""
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import json
from pathlib import Path
from loguru import logger

try:
    import razorpay
    RAZORPAY_AVAILABLE = True
except ImportError:
    RAZORPAY_AVAILABLE = False
    logger.warning("Razorpay not installed. Payment features will be limited.")

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    logger.warning("Stripe not installed. Payment features will be limited.")


class SubscriptionManager:
    """Manage subscriptions, payments, and feature access"""

    # Subscription Plans
    PLANS = {
        'essential': {
            'name': 'Essential',
            'price': 18,
            'price_inr': 1499,
            'billing': 'monthly',
            'features': [
                'Dashboard with overview metrics',
                'Basic stock analysis',
                'Product and customer views',
                'Manual insights',
                'Up to 5 products',
                'Up to 10 customers'
            ],
            'limits': {
                'max_products': 5,
                'max_customers': 10,
                'forecasting': False,
                'customer_segmentation': False,
                'ai_assistant': False,
                'smart_reorder': False,
                'automated_insights': False
            }
        },
        'professional': {
            'name': 'Professional',
            'price': 42,  # USD
            'price_inr': 3499,
            'billing': 'monthly',
            'features': [
                'Everything in Essential',
                'Demand forecasting (30 days)',
                'Customer segmentation (RFM)',
                'Automated insights',
                'Risk assessment',
                'Smart reorder recommendations',
                'Up to 200 products',
                'Unlimited customers',
                'Email support'
            ],
            'limits': {
                'max_products': 200,
                'max_customers': -1,  # Unlimited
                'forecasting': True,
                'customer_segmentation': True,
                'ai_assistant': False,
                'smart_reorder': True,
                'automated_insights': True
            },
            'razorpay_plan_id': os.getenv('RAZORPAY_PLAN_PROFESSIONAL'),
            'stripe_price_id': os.getenv('STRIPE_PRICE_PROFESSIONAL')
        },
        'ai_plus': {
            'name': 'AI Plus',
            'price': 84,  # USD
            'price_inr': 6999,
            'billing': 'monthly',
            'features': [
                'Everything in Professional',
                'Natural Language AI Assistant',
                'Conversational queries (Hindi/English)',
                'AI-generated reports',
                'Smart recommendations',
                'Unlimited products',
                'Unlimited customers',
                'Priority support',
                'Early access to new features'
            ],
            'limits': {
                'max_products': -1,  # Unlimited
                'max_customers': -1,  # Unlimited
                'forecasting': True,
                'customer_segmentation': True,
                'ai_assistant': True,
                'smart_reorder': True,
                'automated_insights': True
            },
            'razorpay_plan_id': os.getenv('RAZORPAY_PLAN_AI_PLUS'),
            'stripe_price_id': os.getenv('STRIPE_PRICE_AI_PLUS')
        }
    }

    def __init__(self, storage_path: str = '.stocksense'):
        """
        Initialize subscription manager

        Args:
            storage_path: Directory to store subscription data
        """
        self.storage_path = Path.home() / storage_path
        self.storage_path.mkdir(exist_ok=True)
        self.subscriptions_file = self.storage_path / 'subscriptions.json'

        # Initialize payment gateways
        self._init_payment_gateways()

        # Load existing subscriptions
        self.subscriptions = self._load_subscriptions()

    def _init_payment_gateways(self):
        """Initialize Razorpay and Stripe"""
        # Razorpay (for India)
        if RAZORPAY_AVAILABLE:
            razorpay_key = os.getenv('RAZORPAY_KEY_ID')
            razorpay_secret = os.getenv('RAZORPAY_KEY_SECRET')
            if razorpay_key and razorpay_secret:
                self.razorpay_client = razorpay.Client(auth=(razorpay_key, razorpay_secret))
                logger.info("Razorpay initialized")
            else:
                self.razorpay_client = None
                logger.warning("Razorpay credentials not found")
        else:
            self.razorpay_client = None

        # Stripe (for global)
        if STRIPE_AVAILABLE:
            stripe_key = os.getenv('STRIPE_SECRET_KEY')
            if stripe_key:
                stripe.api_key = stripe_key
                logger.info("Stripe initialized")
            else:
                logger.warning("Stripe credentials not found")

    def _load_subscriptions(self) -> Dict:
        """Load subscriptions from storage"""
        if self.subscriptions_file.exists():
            try:
                with open(self.subscriptions_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading subscriptions: {e}")
                return {}
        return {}

    def _save_subscriptions(self):
        """Save subscriptions to storage"""
        try:
            with open(self.subscriptions_file, 'w') as f:
                json.dump(self.subscriptions, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving subscriptions: {e}")

    def get_subscription(self, user_id: str) -> Dict:
        """
        Get subscription details for a user

        Args:
            user_id: User identifier

        Returns:
            Subscription details
        """
        if user_id not in self.subscriptions:
            # Return trial (7-day Essential trial) by default
            trial_end = (datetime.now() + timedelta(days=7)).isoformat()
            return {
                'user_id': user_id,
                'plan': 'essential',
                'status': 'trial',
                'start_date': datetime.now().isoformat(),
                'end_date': trial_end,
                'payment_method': 'trial',
                'is_trial': True
            }

        sub = self.subscriptions[user_id]

        # Check if subscription is expired
        if sub.get('end_date'):
            end_date = datetime.fromisoformat(sub['end_date'])
            if datetime.now() > end_date:
                sub['status'] = 'expired'
                self._save_subscriptions()

        return sub

    def create_subscription(self, user_id: str, plan: str, payment_method: str = 'manual') -> Dict:
        """
        Create or update a subscription

        Args:
            user_id: User identifier
            plan: Plan name (free, professional, ai_plus)
            payment_method: Payment method used

        Returns:
            Updated subscription details
        """
        if plan not in self.PLANS:
            raise ValueError(f"Invalid plan: {plan}")

        # Calculate end date (30 days from now for all plans)
        end_date = (datetime.now() + timedelta(days=30)).isoformat()

        subscription = {
            'user_id': user_id,
            'plan': plan,
            'status': 'active',
            'start_date': datetime.now().isoformat(),
            'end_date': end_date,
            'payment_method': payment_method,
            'created_at': datetime.now().isoformat()
        }

        self.subscriptions[user_id] = subscription
        self._save_subscriptions()

        logger.info(f"Created subscription for {user_id}: {plan}")
        return subscription

    def cancel_subscription(self, user_id: str) -> bool:
        """
        Cancel a subscription

        Args:
            user_id: User identifier

        Returns:
            Success status
        """
        if user_id in self.subscriptions:
            self.subscriptions[user_id]['status'] = 'cancelled'
            self.subscriptions[user_id]['cancelled_at'] = datetime.now().isoformat()
            # Set end date to end of current billing period
            if not self.subscriptions[user_id].get('end_date'):
                self.subscriptions[user_id]['end_date'] = (datetime.now() + timedelta(days=30)).isoformat()
            self._save_subscriptions()
            logger.info(f"Cancelled subscription for {user_id}")
            return True
        return False

    def has_feature_access(self, user_id: str, feature: str) -> bool:
        """
        Check if user has access to a feature

        Args:
            user_id: User identifier
            feature: Feature name

        Returns:
            True if user has access
        """
        sub = self.get_subscription(user_id)

        # If subscription expired, mark as expired (trial ends, needs renewal)
        if sub['status'] == 'expired':
            pass  # Keep plan but mark expired

        plan = self.PLANS.get(sub['plan'], self.PLANS['essential'])
        return plan['limits'].get(feature, False)

    def get_plan_limits(self, user_id: str) -> Dict:
        """Get plan limits for a user"""
        sub = self.get_subscription(user_id)
        plan = self.PLANS.get(sub['plan'], self.PLANS['free'])
        return plan['limits']

    def check_limit(self, user_id: str, limit_type: str, current_count: int) -> tuple[bool, Optional[int]]:
        """
        Check if user is within plan limits

        Args:
            user_id: User identifier
            limit_type: Type of limit (max_products, max_customers)
            current_count: Current count

        Returns:
            (is_within_limit, max_allowed)
        """
        limits = self.get_plan_limits(user_id)
        max_allowed = limits.get(limit_type, 0)

        # -1 means unlimited
        if max_allowed == -1:
            return True, None

        is_within_limit = current_count <= max_allowed
        return is_within_limit, max_allowed

    def create_razorpay_order(self, user_id: str, plan: str) -> Optional[Dict]:
        """
        Create Razorpay order for subscription

        Args:
            user_id: User identifier
            plan: Plan name

        Returns:
            Order details or None
        """
        if not self.razorpay_client:
            logger.error("Razorpay not configured")
            return None

        if plan not in self.PLANS:
            logger.error(f"Invalid plan: {plan}")
            return None

        plan_details = self.PLANS[plan]
        amount = plan_details['price_inr'] * 100  # Razorpay uses paise

        try:
            order = self.razorpay_client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 1,
                'notes': {
                    'user_id': user_id,
                    'plan': plan
                }
            })
            logger.info(f"Created Razorpay order for {user_id}: {order['id']}")
            return order
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {e}")
            return None

    def verify_razorpay_payment(self, payment_id: str, order_id: str, signature: str) -> bool:
        """
        Verify Razorpay payment signature

        Args:
            payment_id: Payment ID
            order_id: Order ID
            signature: Payment signature

        Returns:
            True if valid
        """
        if not self.razorpay_client:
            return False

        try:
            params = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            self.razorpay_client.utility.verify_payment_signature(params)
            logger.info(f"Verified Razorpay payment: {payment_id}")
            return True
        except Exception as e:
            logger.error(f"Payment verification failed: {e}")
            return False

    def create_stripe_checkout_session(self, user_id: str, plan: str, success_url: str, cancel_url: str) -> Optional[str]:
        """
        Create Stripe checkout session

        Args:
            user_id: User identifier
            plan: Plan name
            success_url: URL to redirect on success
            cancel_url: URL to redirect on cancel

        Returns:
            Checkout session URL or None
        """
        if not STRIPE_AVAILABLE:
            logger.error("Stripe not configured")
            return None

        if plan not in self.PLANS:
            logger.error(f"Invalid plan: {plan}")
            return None

        plan_details = self.PLANS[plan]
        price_id = plan_details.get('stripe_price_id')

        if not price_id:
            logger.error(f"Stripe price ID not configured for {plan}")
            return None

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=user_id,
                metadata={
                    'user_id': user_id,
                    'plan': plan
                }
            )
            logger.info(f"Created Stripe checkout session for {user_id}")
            return session.url
        except Exception as e:
            logger.error(f"Error creating Stripe session: {e}")
            return None

    def get_plan_comparison(self) -> List[Dict]:
        """Get plan comparison for display"""
        return [
            {
                'plan': plan_key,
                'name': details['name'],
                'price_inr': details['price_inr'],
                'price_usd': details['price'],
                'billing': details['billing'],
                'features': details['features']
            }
            for plan_key, details in self.PLANS.items()
        ]

    def upgrade_prompt_message(self, user_id: str, feature: str) -> str:
        """Get upgrade prompt message for a feature"""
        sub = self.get_subscription(user_id)
        current_plan = sub['plan']

        # Find which plan has this feature
        required_plan = None
        for plan_key, plan_details in self.PLANS.items():
            if plan_details['limits'].get(feature, False):
                required_plan = plan_key
                break

        if not required_plan:
            return "This feature is not available in any plan."

        plan_name = self.PLANS[required_plan]['name']
        price = self.PLANS[required_plan]['price_inr']

        return f"⚡ This feature requires {plan_name} plan (₹{price}/month). Upgrade to unlock!"


# Singleton instance
_subscription_manager = None

def get_subscription_manager() -> SubscriptionManager:
    """Get singleton subscription manager instance"""
    global _subscription_manager
    if _subscription_manager is None:
        _subscription_manager = SubscriptionManager()
    return _subscription_manager
