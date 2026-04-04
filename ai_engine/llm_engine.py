"""
LLM-powered natural language interface and insights
Supports OpenAI GPT and Anthropic Claude
"""
import os
from typing import List, Dict, Optional
import pandas as pd
from loguru import logger

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not installed. LLM features will be limited.")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic not installed. Claude features will be limited.")


class LLMEngine:
    """LLM-powered natural language interface"""

    def __init__(self, provider: str = "openai", model: Optional[str] = None):
        """
        Initialize LLM Engine

        Args:
            provider: 'openai' or 'anthropic'
            model: Specific model to use (optional)
        """
        self.provider = provider

        if provider == "openai" and OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = OpenAI(api_key=api_key)
                self.model = model or "gpt-4"
                self.enabled = True
                logger.info(f"OpenAI LLM initialized with {self.model}")
            else:
                self.enabled = False
                logger.warning("OpenAI API key not found")

        elif provider == "anthropic" and ANTHROPIC_AVAILABLE:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
                self.model = model or "claude-3-sonnet-20240229"
                self.enabled = True
                logger.info(f"Anthropic Claude initialized with {self.model}")
            else:
                self.enabled = False
                logger.warning("Anthropic API key not found")
        else:
            self.enabled = False
            logger.warning(f"LLM provider {provider} not available")

    def natural_language_query(self, query: str, context: Dict) -> str:
        """
        Answer natural language questions about inventory data

        Args:
            query: User's question
            context: Data context (products, customers, insights)

        Returns:
            Natural language answer
        """
        if not self.enabled:
            return "LLM features not enabled. Please configure API key in .env file."

        # Build context string
        context_str = self._build_context(context)

        # Create prompt
        prompt = f"""You are an AI assistant for an inventory management system.
Answer the user's question based on the provided data context.

Context:
{context_str}

User Question: {query}

Provide a clear, concise answer with specific numbers and actionable insights."""

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert inventory and business analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                return response.choices[0].message.content

            elif self.provider == "anthropic":
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return message.content[0].text

        except Exception as e:
            logger.error(f"LLM query failed: {e}")
            return f"Error processing query: {str(e)}"

    def generate_narrative_report(self, data: Dict) -> str:
        """
        Generate narrative business report from data

        Args:
            data: Dictionary with insights, forecasts, risks

        Returns:
            Narrative report text
        """
        if not self.enabled:
            return "LLM features not enabled."

        # Extract key metrics
        summary = self._extract_key_metrics(data)

        prompt = f"""Generate a concise executive business report based on this inventory data:

{summary}

Write a professional report covering:
1. Current Situation Summary
2. Critical Alerts (if any)
3. Key Recommendations
4. Action Items

Keep it under 300 words, use business language, and focus on actionable insights."""

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a business analyst writing executive reports."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=600,
                    temperature=0.7
                )
                return response.choices[0].message.content

            elif self.provider == "anthropic":
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=600,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return message.content[0].text

        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return f"Error generating report: {str(e)}"

    def smart_recommendations(self, context: Dict) -> List[str]:
        """
        Generate smart recommendations based on data patterns

        Args:
            context: Business context and data

        Returns:
            List of recommendations
        """
        if not self.enabled:
            return ["LLM features not enabled. Configure API key to use smart recommendations."]

        context_str = self._build_context(context)

        prompt = f"""Based on this inventory and sales data, provide 5 specific, actionable business recommendations:

{context_str}

Focus on:
- Inventory optimization
- Revenue opportunities
- Risk mitigation
- Customer engagement

Format: Return exactly 5 recommendations, one per line, starting with a number."""

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a business strategy consultant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.8
                )
                text = response.choices[0].message.content

            elif self.provider == "anthropic":
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                text = message.content[0].text

            # Parse recommendations
            recommendations = [line.strip() for line in text.split('\n') if line.strip() and line.strip()[0].isdigit()]
            return recommendations[:5]

        except Exception as e:
            logger.error(f"Recommendations failed: {e}")
            return [f"Error generating recommendations: {str(e)}"]

    def chat_interface(self, messages: List[Dict[str, str]], context: Dict) -> str:
        """
        Chatbot interface for conversational queries

        Args:
            messages: List of {"role": "user/assistant", "content": "..."}
            context: Current data context

        Returns:
            Assistant response
        """
        if not self.enabled:
            return "LLM chatbot not enabled. Please configure API key."

        # Add system context
        context_str = self._build_context(context)
        system_message = f"""You are an AI assistant for Inventory Intelligence System.
You help traders make data-driven decisions about their inventory.

Current Data Context:
{context_str}

Answer questions clearly, provide specific numbers when available, and give actionable advice."""

        try:
            if self.provider == "openai":
                full_messages = [{"role": "system", "content": system_message}] + messages

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=full_messages,
                    max_tokens=400,
                    temperature=0.7
                )
                return response.choices[0].message.content

            elif self.provider == "anthropic":
                # Claude doesn't use system messages the same way
                user_message = f"{system_message}\n\nConversation:\n" + "\n".join([
                    f"{m['role']}: {m['content']}" for m in messages
                ])

                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=400,
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                return message.content[0].text

        except Exception as e:
            logger.error(f"Chat failed: {e}")
            return f"Error: {str(e)}"

    def _build_context(self, context: Dict) -> str:
        """Build context string from data"""
        parts = []

        if 'products_count' in context:
            parts.append(f"Total Products: {context['products_count']}")

        if 'customer_count' in context:
            parts.append(f"Total Customers: {context['customer_count']}")

        if 'revenue' in context:
            parts.append(f"Total Revenue: ₹{context['revenue']:,.0f}")

        # Customer segments summary
        if 'segment_summary' in context and context['segment_summary']:
            parts.append("\nCustomer Segments:")
            for segment, count in context['segment_summary'].items():
                parts.append(f"  - {segment}: {count} customers")

        # Customer details
        if 'customer_data' in context and context['customer_data']:
            parts.append(f"\nTop Customers (showing {len(context['customer_data'])}):")
            for cust in context['customer_data']:
                parts.append(f"  - {cust['name']}: {cust['segment']}, "
                           f"Spent ₹{cust['total_spent']:,.0f}, "
                           f"{cust['purchase_count']} purchases, "
                           f"Last seen {cust['days_since_last']:.0f} days ago")

        # High risk products with details
        if 'high_risk_products' in context:
            parts.append(f"\nHigh Risk Products: {context['high_risk_products']}")
            if 'high_risk_details' in context and context['high_risk_details']:
                parts.append("Details:")
                for item in context['high_risk_details']:
                    parts.append(f"  - {item['name']}: {item['days_left']:.0f} days left, {item['current_stock']} units in stock")

        # Urgent reorders with details
        if 'urgent_reorders' in context:
            parts.append(f"\nUrgent Reorders: {context['urgent_reorders']}")
            if 'urgent_reorder_details' in context and context['urgent_reorder_details']:
                parts.append("Details:")
                for item in context['urgent_reorder_details']:
                    parts.append(f"  - {item['name']}: Reorder {item['quantity']} units (₹{item['cost']:,.0f}) - {item['reason']}")

        # Top products
        if 'top_products' in context and context['top_products']:
            parts.append(f"\nTop Products (by stock): {', '.join(context['top_products'][:5])}")

        # Alerts
        if 'alerts' in context and context['alerts']:
            parts.append(f"\nActive Alerts: {len(context['alerts'])}")
            for i, alert in enumerate(context['alerts'][:3], 1):
                parts.append(f"  {i}. {alert}")

        # Transaction data summary (if available)
        if 'transactions' in context and not context['transactions'].empty:
            trans_df = context['transactions']
            parts.append(f"\nRecent Transactions: {len(trans_df)} total")
            if 'date' in trans_df.columns:
                parts.append(f"  Date range: {trans_df['date'].min()} to {trans_df['date'].max()}")

        return "\n".join(parts)

    def _extract_key_metrics(self, data: Dict) -> str:
        """Extract key metrics for report generation"""
        metrics = []

        if 'risk_df' in data and not data['risk_df'].empty:
            risk_df = data['risk_df']
            high_risk = len(risk_df[risk_df['risk_level'] == 'HIGH'])
            metrics.append(f"- {high_risk} products at HIGH risk")

        if 'smart_reorder_df' in data and not data['smart_reorder_df'].empty:
            reorder_df = data['smart_reorder_df']
            urgent = len(reorder_df[reorder_df['urgency'] == 'URGENT'])
            metrics.append(f"- {urgent} URGENT reorders required")

        if 'alerts' in data:
            metrics.append(f"- {len(data['alerts'])} active alerts")

        if 'price_intel' in data:
            price_intel = data['price_intel']
            if 'buying_opportunities' in price_intel:
                ops = len(price_intel['buying_opportunities'])
                metrics.append(f"- {ops} price buying opportunities")

        return "\n".join(metrics) if metrics else "No critical metrics at this time."

    def analyze_trends(self, data: pd.DataFrame, question: str) -> str:
        """
        Analyze trends and patterns in data

        Args:
            data: DataFrame with time-series data
            question: Specific question about trends

        Returns:
            Analysis result
        """
        if not self.enabled:
            return "Trend analysis requires LLM features."

        # Sample data for context
        data_summary = data.describe().to_string() if not data.empty else "No data"

        prompt = f"""Analyze this data and answer the question:

Data Summary:
{data_summary}

Question: {question}

Provide insights about trends, patterns, and predictions."""

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a data analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300
                )
                return response.choices[0].message.content

            elif self.provider == "anthropic":
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=300,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return message.content[0].text

        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return f"Error: {str(e)}"
