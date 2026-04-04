# 💳 StockSense Subscription System Setup Guide

Complete guide to setting up and using the subscription management system.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Payment Gateway Setup](#payment-gateway-setup)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Production Deployment](#production-deployment)

---

## 🎯 Overview

StockSense now includes a complete subscription management system with:

### Features
- ✅ **3 Subscription Tiers**: Essential (Free), Professional (₹999/mo), AI Plus (₹1,999/mo)
- ✅ **Payment Integration**: Razorpay (India) & Stripe (International)
- ✅ **Feature Gating**: Automatic access control based on subscription
- ✅ **Usage Limits**: Product/customer limits per plan
- ✅ **Subscription Management**: Upgrade, downgrade, cancel
- ✅ **Billing History**: Track payments and invoices

### Subscription Tiers

| Feature | Essential (Free) | Professional (₹999/mo) | AI Plus (₹1,999/mo) |
|---------|-----------------|----------------------|-------------------|
| Dashboard | ✓ | ✓ | ✓ |
| Products | Up to 5 | Up to 200 | Unlimited |
| Customers | Up to 10 | Unlimited | Unlimited |
| Demand Forecasting | ✗ | ✓ | ✓ |
| Customer Segmentation | ✗ | ✓ | ✓ |
| Smart Reorder | ✗ | ✓ | ✓ |
| AI Assistant | ✗ | ✗ | ✓ |
| Natural Language Queries | ✗ | ✗ | ✓ |
| Priority Support | ✗ | ✗ | ✓ |

---

## 🚀 Installation

### Step 1: Install Dependencies

```bash
# Install payment libraries
pip install razorpay>=1.3.0 stripe>=5.0.0

# Or install all requirements
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
python -c "import razorpay; print('Razorpay OK')"
python -c "import stripe; print('Stripe OK')"
```

---

## 💰 Payment Gateway Setup

### Option 1: Razorpay (Recommended for India)

**Step 1: Create Account**
1. Go to https://dashboard.razorpay.com/signup
2. Complete KYC verification
3. Get your API keys

**Step 2: Get API Keys**
1. Go to Settings → API Keys
2. Generate Test/Live keys
3. Save:
   - Key ID (e.g., `rzp_test_xxxxx`)
   - Key Secret (e.g., `xxxxx`)

**Step 3: Create Subscription Plans** (Optional - for recurring)
1. Go to Products → Subscriptions → Plans
2. Create plans:
   - **Professional**: ₹999/month
   - **AI Plus**: ₹1,999/month
3. Note down Plan IDs

**Step 4: Configure Webhooks** (Production)
1. Go to Settings → Webhooks
2. Add webhook URL: `https://your-domain.com/webhooks/razorpay`
3. Select events: `payment.captured`, `subscription.charged`

---

### Option 2: Stripe (For International Payments)

**Step 1: Create Account**
1. Go to https://dashboard.stripe.com/register
2. Complete business verification
3. Get your API keys

**Step 2: Get API Keys**
1. Go to Developers → API keys
2. Save:
   - Publishable key (starts with `pk_`)
   - Secret key (starts with `sk_`)

**Step 3: Create Products & Prices**
1. Go to Products → Add Product
2. Create two products:
   - **StockSense Professional**: $12/month
   - **StockSense AI Plus**: $24/month
3. Note down Price IDs (start with `price_`)

**Step 4: Configure Webhooks** (Production)
1. Go to Developers → Webhooks
2. Add endpoint: `https://your-domain.com/webhooks/stripe`
3. Select events: `checkout.session.completed`, `invoice.paid`

---

## ⚙️ Configuration

### Step 1: Update `.env` File

Copy `.env.example` to `.env` and add your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Razorpay (India)
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=your_secret_key
RAZORPAY_PLAN_PROFESSIONAL=plan_xxxxx
RAZORPAY_PLAN_AI_PLUS=plan_xxxxx

# Stripe (International)
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_PRICE_PROFESSIONAL=price_xxxxx
STRIPE_PRICE_AI_PLUS=price_xxxxx
```

### Step 2: Test Configuration

```python
# Test Razorpay
from subscription import get_subscription_manager

sub_manager = get_subscription_manager()
print(sub_manager.razorpay_client)  # Should not be None

# Test Stripe
import stripe
print(stripe.api_key)  # Should show your key
```

---

## 🧪 Testing

### Test Mode (Development)

**Razorpay Test Cards:**
- Success: `4111 1111 1111 1111`
- CVV: Any 3 digits
- Expiry: Any future date
- OTP: `0000`

**Stripe Test Cards:**
- Success: `4242 4242 4242 4242`
- 3D Secure: `4000 0027 6000 3184`
- CVV: Any 3 digits
- Expiry: Any future date

### Test Subscription Flow

```bash
# Run the app
streamlit run app_tally.py

# Steps:
# 1. Open http://localhost:8501
# 2. Click "💳 Manage Subscription"
# 3. Choose a plan
# 4. Test payment with test card
# 5. Verify subscription activation
```

### Manual Testing Checklist

- [ ] Free plan works by default
- [ ] Can upgrade to Professional
- [ ] Can upgrade to AI Plus
- [ ] Feature access controls work
- [ ] Usage limits are enforced
- [ ] Can cancel subscription
- [ ] Downgrade to Free works
- [ ] Payment verification works
- [ ] Billing history displays

---

## 🌐 Production Deployment

### Security Checklist

**✅ API Keys**
- [ ] Use LIVE keys (not TEST)
- [ ] Store keys in environment variables (NOT in code)
- [ ] Use different keys for staging/production
- [ ] Rotate keys regularly

**✅ Webhooks**
- [ ] Verify webhook signatures
- [ ] Use HTTPS URLs only
- [ ] Log all webhook events
- [ ] Handle webhook failures gracefully

**✅ Payment Security**
- [ ] Never store card details
- [ ] Use PCI-compliant payment forms
- [ ] Enable 3D Secure (when available)
- [ ] Set up fraud detection

### Environment Variables (Production)

```bash
# Production .env
APP_ENV=production
RAZORPAY_KEY_ID=rzp_live_xxxxx
RAZORPAY_KEY_SECRET=live_secret_key
STRIPE_SECRET_KEY=sk_live_xxxxx

# Webhook secrets
RAZORPAY_WEBHOOK_SECRET=whsec_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

### Database Setup (Production)

For production, replace JSON storage with a proper database:

```python
# Example: PostgreSQL
import psycopg2

# Store subscriptions in database
CREATE TABLE subscriptions (
    user_id VARCHAR(255) PRIMARY KEY,
    plan VARCHAR(50),
    status VARCHAR(50),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    payment_method VARCHAR(50),
    created_at TIMESTAMP
);
```

### Monitoring & Alerts

**Set up alerts for:**
- Failed payments
- Subscription cancellations
- High error rates
- Unusual payment patterns

**Tools:**
- Sentry for error tracking
- Mixpanel/Amplitude for analytics
- PagerDuty for critical alerts

---

## 🔧 Customization

### Adding New Plans

Edit `subscription/subscription_manager.py`:

```python
PLANS = {
    'your_new_plan': {
        'name': 'Enterprise Plus',
        'price': 50,
        'price_inr': 4999,
        'billing': 'monthly',
        'features': [
            'Everything in AI Plus',
            'Dedicated support',
            'Custom integrations'
        ],
        'limits': {
            'max_products': -1,
            'max_customers': -1,
            'forecasting': True,
            'customer_segmentation': True,
            'ai_assistant': True,
            'smart_reorder': True,
            'automated_insights': True,
            'custom_features': True  # Your custom feature
        }
    }
}
```

### Custom Feature Gates

```python
# In your feature code
from subscription.streamlit_components import check_feature_access

user_id = st.session_state.user_id

if check_feature_access(user_id, 'custom_features'):
    # Show premium feature
    st.success("Premium feature unlocked!")
else:
    # Show upgrade prompt
    st.warning("Upgrade to access this feature")
```

### Custom Pricing

```python
# Country-specific pricing
def get_pricing(country_code):
    pricing = {
        'IN': {'professional': 999, 'ai_plus': 1999},  # INR
        'US': {'professional': 12, 'ai_plus': 24},      # USD
        'EU': {'professional': 10, 'ai_plus': 20}       # EUR
    }
    return pricing.get(country_code, pricing['US'])
```

---

## 📊 Analytics & Metrics

### Key Metrics to Track

1. **Conversion Rate**: Free → Paid
2. **Churn Rate**: Cancellations/month
3. **MRR**: Monthly Recurring Revenue
4. **LTV**: Lifetime Value per customer
5. **CAC**: Customer Acquisition Cost

### Example Analytics Code

```python
from subscription import get_subscription_manager

sub_manager = get_subscription_manager()

# Get all subscriptions
all_subs = sub_manager.subscriptions

# Calculate metrics
paid_users = len([s for s in all_subs.values() if s['plan'] != 'free'])
total_users = len(all_subs)
conversion_rate = (paid_users / total_users) * 100 if total_users > 0 else 0

# MRR calculation
mrr = sum([
    sub_manager.PLANS[s['plan']]['price_inr']
    for s in all_subs.values()
    if s['plan'] != 'free' and s['status'] == 'active'
])

print(f"Conversion Rate: {conversion_rate:.2f}%")
print(f"MRR: ₹{mrr:,}")
```

---

## 🐛 Troubleshooting

### Issue: Payment not capturing

**Solution:**
```python
# Check Razorpay dashboard for failed payments
# Verify webhook is receiving events
# Check logs for errors
```

### Issue: Subscription not activating

**Solution:**
```python
# Manually activate for testing
from subscription import get_subscription_manager

sub_manager = get_subscription_manager()
sub_manager.create_subscription('user_id', 'professional', 'manual')
```

### Issue: Feature access not working

**Solution:**
```python
# Check user's subscription
sub = sub_manager.get_subscription('user_id')
print(sub)

# Check feature limits
limits = sub_manager.get_plan_limits('user_id')
print(limits)
```

---

## 📞 Support

### For Development Issues
- GitHub: https://github.com/yourusername/stocksense
- Email: dev@stocksense.ai

### For Payment Issues
- Razorpay Support: https://razorpay.com/support/
- Stripe Support: https://support.stripe.com/

### For Billing Questions
- Email: billing@stocksense.ai
- Phone: +91-XXXXX-XXXXX

---

## 📚 Resources

- [Razorpay Documentation](https://razorpay.com/docs/)
- [Stripe Documentation](https://stripe.com/docs)
- [StockSense API Docs](./API.md)
- [Feature Gate Guide](./FEATURES.md)

---

## 🎉 Quick Start Checklist

For a quick production setup:

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create Razorpay/Stripe accounts
- [ ] Get API keys
- [ ] Update `.env` with keys
- [ ] Test with test cards
- [ ] Switch to live keys
- [ ] Set up webhooks
- [ ] Configure monitoring
- [ ] Launch! 🚀

---

**Version:** 1.0.0
**Last Updated:** March 2026
**Questions?** Contact: support@stocksense.ai
