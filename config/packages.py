"""
Package configurations for Inventory Intelligence System
"""

PACKAGES = {
    'essential': {
        'name': '📦 Essential Package',
        'description': 'Basic inventory tracking and stock management',
        'price': '₹1,499/month',
        'features': [
            'Business Dashboard',
            'Stock Summary',
            'Basic Alerts',
            'Product List',
            'Customer List',
            'Sales Overview'
        ],
        'tabs': ['Dashboard', 'Stock Summary', 'Alerts']
    },

    'professional': {
        'name': '💼 Professional Package',
        'description': 'Advanced analytics with AI-powered insights',
        'price': '₹3,499/month',
        'features': [
            'All Essential features',
            '🔴 Stock Risk Analysis with Days Left',
            '📦 Smart Reorder Engine (Auto recommendations)',
            '💰 Price Intelligence (Buy/Sell signals)',
            'AI-Powered Forecasting',
            'Automated Alerts',
            'Export Reports (CSV)'
        ],
        'tabs': ['Dashboard', 'Stock Risk', 'Smart Reorder', 'Price Intelligence', 'Alerts']
    },

    'enterprise': {
        'name': '🚀 Enterprise Package',
        'description': 'Complete business intelligence suite',
        'price': '₹5,999/month',
        'features': [
            'All Professional features',
            '👥 Customer Intelligence (RFM Analysis)',
            '🎯 Cross-Sell Opportunities',
            '📊 Advanced Analytics Dashboard',
            'Customer Segmentation',
            'Dead Stock Detection',
            'Sales Trend Analysis',
            'Category Performance',
            'Stock Efficiency Metrics',
            'Priority Support',
            'Custom Reports'
        ],
        'tabs': [
            'Control Panel',
            'Dashboard',
            'Stock Risk',
            'Smart Reorder',
            'Customer Intelligence',
            'Price Intelligence',
            'Analytics'
        ]
    },

    'ai_plus': {
        'name': '🤖 AI Plus Package',
        'description': 'Ultimate AI-powered intelligence with LLM capabilities',
        'price': '₹9,999/month',
        'features': [
            'All Enterprise features',
            '🤖 Natural Language Queries (Ask in plain English)',
            '📝 Automated Report Generation (AI-written reports)',
            '💬 AI Chatbot Assistant (24/7 conversational help)',
            '🎯 Smart Recommendations (GPT-powered insights)',
            '📊 Trend Analysis (AI pattern detection)',
            '🔮 Market Intelligence (External trend analysis)',
            'Multi-language Support',
            'Voice Commands (coming soon)',
            'API Access for Custom Integration',
            'Dedicated AI Support',
            'Early Access to New AI Features'
        ],
        'tabs': [
            'Control Panel',
            'Dashboard',
            'Stock Risk',
            'Smart Reorder',
            'Customer Intelligence',
            'Price Intelligence',
            'Analytics',
            'AI Assistant'
        ]
    }
}


def get_package_features(package_name: str) -> dict:
    """Get features for a specific package"""
    return PACKAGES.get(package_name, PACKAGES['essential'])


def get_available_tabs(package_name: str) -> list:
    """Get available tabs for a package"""
    return PACKAGES.get(package_name, PACKAGES['essential'])['tabs']
