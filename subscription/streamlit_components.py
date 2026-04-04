"""
Streamlit UI components for subscription management
"""
import streamlit as st
from typing import Optional
from .subscription_manager import get_subscription_manager


def render_subscription_page(user_id: str):
    """Render complete subscription management page"""
    st.title("💳 Subscription & Billing")
    st.markdown("### Manage your StockSense subscription")

    sub_manager = get_subscription_manager()
    current_sub = sub_manager.get_subscription(user_id)
    current_plan = current_sub['plan']

    # Show current subscription
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Plan",
            sub_manager.PLANS[current_plan]['name'],
            help="Your active subscription plan"
        )

    with col2:
        status_icon = "✅" if current_sub['status'] == 'active' else "⚠️"
        st.metric(
            "Status",
            f"{status_icon} {current_sub['status'].title()}",
            help="Subscription status"
        )

    with col3:
        if current_sub.get('end_date'):
            import datetime
            end_date = datetime.datetime.fromisoformat(current_sub['end_date'])
            days_left = (end_date - datetime.datetime.now()).days

            # Check if trial
            is_trial = current_sub.get('is_trial', False) or current_sub.get('status') == 'trial'
            label = "Trial Days Left" if is_trial else "Days Remaining"

            st.metric(
                label,
                days_left,
                help="Days until renewal required" if not is_trial else "Days left in free trial"
            )
        else:
            st.metric("Billing", "Active", help="Active subscription")

    st.markdown("---")

    # Plan comparison
    st.subheader("📊 Choose Your Plan")

    cols = st.columns(3)
    plans = ['essential', 'professional', 'ai_plus']

    for idx, plan_key in enumerate(plans):
        with cols[idx]:
            plan = sub_manager.PLANS[plan_key]
            is_current = plan_key == current_plan

            # Card styling
            if is_current:
                st.success(f"✓ Current Plan")

            st.markdown(f"### {plan['name']}")

            # Price
            st.markdown(f"## **₹{plan['price_inr']:,}**")
            st.caption(f"per {plan['billing']}")
            st.caption(f"(${plan['price']} USD)")

            # Show trial badge for Essential
            if plan_key == 'essential' and not is_current:
                st.info("🎁 7-Day Free Trial")

            st.markdown("---")

            # Features
            for feature in plan['features'][:6]:  # Show first 6 features
                st.markdown(f"✓ {feature}")

            if len(plan['features']) > 6:
                with st.expander("See all features"):
                    for feature in plan['features'][6:]:
                        st.markdown(f"✓ {feature}")

            st.markdown("---")

            # Action button
            if is_current:
                if st.button(f"❌ Cancel {plan['name']}", key=f"cancel_{plan_key}"):
                    if sub_manager.cancel_subscription(user_id):
                        st.success("Subscription cancelled. You'll have access until the end of your billing period.")
                        st.experimental_rerun()
            else:
                # Check if on trial
                current_sub = sub_manager.get_subscription(user_id)
                is_trial = current_sub.get('is_trial', False) or current_sub.get('status') == 'trial'

                if is_trial and plan_key == 'essential':
                    st.info("✓ You're on trial")
                else:
                    button_text = f"Start Trial" if plan_key == 'essential' and not is_trial else f"⬆️ Upgrade to {plan['name']}"
                    if st.button(button_text, key=f"upgrade_{plan_key}"):
                        show_payment_options(user_id, plan_key)

    # Feature comparison table
    st.markdown("---")
    st.subheader("🔍 Detailed Feature Comparison")

    with st.expander("View full comparison"):
        render_feature_comparison_table()

    # Billing history (if applicable)
    if current_plan != 'free':
        st.markdown("---")
        st.subheader("📜 Billing History")
        render_billing_history(user_id)


def show_payment_options(user_id: str, plan: str):
    """Show payment options modal"""
    sub_manager = get_subscription_manager()
    plan_details = sub_manager.PLANS[plan]

    st.markdown("---")
    st.info(f"Upgrade to **{plan_details['name']}** - ₹{plan_details['price_inr']}/month")

    st.markdown("### Choose Payment Method:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🇮🇳 Razorpay (India)")
        st.caption("Credit/Debit Card, UPI, Netbanking")

        if st.button("Pay with Razorpay", key="razorpay"):
            order = sub_manager.create_razorpay_order(user_id, plan)
            if order:
                st.session_state['payment_order'] = order
                st.session_state['payment_plan'] = plan
                render_razorpay_checkout(order, plan_details)
            else:
                st.error("❌ Razorpay not configured. Please contact support.")

    with col2:
        st.markdown("#### 🌍 Stripe (International)")
        st.caption("Credit/Debit Card")

        if st.button("Pay with Stripe", key="stripe"):
            # In production, these would be your actual URLs
            success_url = "http://localhost:8501/?payment=success"
            cancel_url = "http://localhost:8501/?payment=cancelled"

            checkout_url = sub_manager.create_stripe_checkout_session(
                user_id, plan, success_url, cancel_url
            )

            if checkout_url:
                st.markdown(f"[Click here to complete payment]({checkout_url})")
                st.info("You'll be redirected to Stripe's secure checkout page")
            else:
                st.error("❌ Stripe not configured. Please contact support.")

    # Manual/Offline payment option
    with st.expander("💰 Offline Payment (Bank Transfer)"):
        st.markdown("""
        **For bulk/annual payments, contact us:**

        📧 Email: billing@stocksense.ai
        📱 WhatsApp: +91-XXXXX-XXXXX

        Bank Transfer Details:
        - Account Name: StockSense
        - Account No: XXXXXXXXXXXX
        - IFSC: XXXXXX
        - Bank: XXXX Bank

        Please include your User ID in the transfer reference.
        """)

        if st.button("I've completed offline payment", key="offline"):
            st.info("Thank you! Your payment will be verified within 24 hours.")


def render_razorpay_checkout(order: dict, plan_details: dict):
    """Render Razorpay checkout UI"""
    st.markdown("### Complete Payment")

    # In a real implementation, you'd use Razorpay's JavaScript SDK
    # For now, show instructions
    st.code(f"""
Order ID: {order['id']}
Amount: ₹{order['amount'] / 100}
    """)

    st.info("""
    **Next Steps:**
    1. Use the Order ID above
    2. Complete payment through Razorpay
    3. Your subscription will be activated immediately
    """)

    # Payment verification form
    with st.form("verify_payment"):
        payment_id = st.text_input("Razorpay Payment ID")
        signature = st.text_input("Razorpay Signature")

        if st.form_submit_button("Verify Payment"):
            sub_manager = get_subscription_manager()
            if sub_manager.verify_razorpay_payment(payment_id, order['id'], signature):
                # Activate subscription
                plan = st.session_state.get('payment_plan')
                sub_manager.create_subscription(st.session_state['user_id'], plan, 'razorpay')
                st.success("✅ Payment verified! Your subscription is now active.")
                st.balloons()
                st.experimental_rerun()
            else:
                st.error("❌ Payment verification failed. Please contact support.")


def render_feature_comparison_table():
    """Render detailed feature comparison"""
    sub_manager = get_subscription_manager()

    features = {
        'Basic Features': {
            'Dashboard': ['✓', '✓', '✓'],
            'Product Analysis': ['Up to 5', 'Up to 200', 'Unlimited'],
            'Customer Management': ['Up to 10', 'Unlimited', 'Unlimited'],
        },
        'AI & Analytics': {
            'Demand Forecasting': ['✗', '✓', '✓'],
            'Customer Segmentation': ['✗', '✓', '✓'],
            'Smart Reorder': ['✗', '✓', '✓'],
            'AI Assistant': ['✗', '✗', '✓'],
            'Natural Language Queries': ['✗', '✗', '✓'],
        },
        'Support': {
            'Community Support': ['✓', '✓', '✓'],
            'Email Support': ['✗', '✓', '✓'],
            'Priority Support': ['✗', '✗', '✓'],
        }
    }

    for category, items in features.items():
        st.markdown(f"**{category}**")

        for feature, values in items.items():
            cols = st.columns([2, 1, 1, 1])
            cols[0].write(feature)
            cols[1].write(values[0])  # Free
            cols[2].write(values[1])  # Professional
            cols[3].write(values[2])  # AI Plus

        st.markdown("---")


def render_billing_history(user_id: str):
    """Render billing history"""
    # Placeholder for billing history
    st.info("Billing history will be displayed here once you have transactions.")


def render_upgrade_prompt(user_id: str, feature: str, required_plan: str):
    """Show upgrade prompt when feature is not available"""
    sub_manager = get_subscription_manager()
    message = sub_manager.upgrade_prompt_message(user_id, feature)

    st.warning(message)

    if st.button(f"Upgrade to {sub_manager.PLANS[required_plan]['name']}", key=f"upgrade_prompt_{feature}"):
        st.session_state['show_subscription_page'] = True
        st.experimental_rerun()


def check_feature_access(user_id: str, feature: str, show_prompt: bool = True) -> bool:
    """
    Check feature access and optionally show upgrade prompt

    Args:
        user_id: User ID
        feature: Feature name to check
        show_prompt: Whether to show upgrade prompt

    Returns:
        True if user has access
    """
    sub_manager = get_subscription_manager()
    has_access = sub_manager.has_feature_access(user_id, feature)

    if not has_access and show_prompt:
        # Find required plan
        required_plan = None
        for plan_key, plan_details in sub_manager.PLANS.items():
            if plan_details['limits'].get(feature, False):
                required_plan = plan_key
                break

        if required_plan:
            render_upgrade_prompt(user_id, feature, required_plan)

    return has_access


def render_plan_badge(user_id: str):
    """Render current plan badge in sidebar"""
    sub_manager = get_subscription_manager()
    current_sub = sub_manager.get_subscription(user_id)
    plan_name = sub_manager.PLANS[current_sub['plan']]['name']

    # Check if on trial
    is_trial = current_sub.get('is_trial', False) or current_sub.get('status') == 'trial'
    if is_trial:
        plan_name += " (Trial)"

    if current_sub['plan'] == 'essential':
        badge_color = "#4CAF50"
        icon = "📦"
    elif current_sub['plan'] == 'professional':
        badge_color = "#2196F3"
        icon = "⚡"
    else:  # ai_plus
        badge_color = "#9C27B0"
        icon = "🚀"

    st.markdown(f"""
    <div style='background-color: {badge_color}; padding: 10px; border-radius: 5px; text-align: center; color: white;'>
        <strong>{icon} {plan_name}</strong>
    </div>
    """, unsafe_allow_html=True)

    # Show upgrade button if not on highest plan or if trial expired
    if current_sub['plan'] != 'ai_plus' or current_sub.get('status') == 'expired':
        if st.button("⬆️ Upgrade Plan", key="sidebar_upgrade"):
            st.session_state['show_subscription_page'] = True
            st.experimental_rerun()
