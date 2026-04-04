"""
Automation engine for alerts, notifications, and auto-actions
"""
import pandas as pd
from typing import List, Dict, Callable
from datetime import datetime
from loguru import logger
from models.schemas import Insight, ForecastResult


class AutomationEngine:
    """Handle automated alerts and actions"""

    def __init__(self):
        self.alerts = []
        self.actions_taken = []

    def process_insights(self, insights: List[Insight]) -> Dict[str, List[str]]:
        """Process insights and trigger appropriate automations"""
        logger.info("Processing insights for automation...")

        automation_results = {
            'alerts_sent': [],
            'actions_taken': [],
            'recommendations': []
        }

        for insight in insights:
            if insight.priority == 'critical' and insight.action_required:
                # Send critical alerts
                alert_msg = self._send_alert(insight)
                automation_results['alerts_sent'].append(alert_msg)

            elif insight.priority == 'high' and insight.action_required:
                # Create action items
                action_msg = self._create_action_item(insight)
                automation_results['actions_taken'].append(action_msg)

            elif insight.insight_type == 'recommendation':
                automation_results['recommendations'].append(insight.title)

        logger.info(f"Automation complete: {len(automation_results['alerts_sent'])} alerts, "
                   f"{len(automation_results['actions_taken'])} actions")

        return automation_results

    def _send_alert(self, insight: Insight) -> str:
        """Send alert notification"""
        alert_message = f"[{insight.priority.upper()}] {insight.title}: {insight.description}"
        logger.warning(alert_message)

        # In production, this would integrate with:
        # - Email service
        # - Slack/Teams
        # - SMS gateway
        # - Push notifications

        self.alerts.append({
            'timestamp': datetime.now(),
            'message': alert_message,
            'insight': insight
        })

        return alert_message

    def _create_action_item(self, insight: Insight) -> str:
        """Create actionable task"""
        action_message = f"ACTION REQUIRED: {insight.title}"
        logger.info(action_message)

        # In production, this would:
        # - Create tasks in project management tools
        # - Add to order queue
        # - Trigger approval workflows

        self.actions_taken.append({
            'timestamp': datetime.now(),
            'action': action_message,
            'insight': insight,
            'status': 'pending'
        })

        return action_message

    def generate_reorder_recommendations(self, forecasts: List[ForecastResult]) -> pd.DataFrame:
        """Generate automated reorder recommendations"""
        reorder_list = []

        for forecast in forecasts:
            if forecast.recommended_order_quantity > 0:
                reorder_list.append({
                    'product_id': forecast.product_id,
                    'product_name': forecast.product_name,
                    'current_stock': forecast.current_stock,
                    'predicted_demand': forecast.predicted_demand,
                    'recommended_order': forecast.recommended_order_quantity,
                    'risk_level': forecast.risk_level,
                    'urgency': self._calculate_urgency(forecast)
                })

        reorder_df = pd.DataFrame(reorder_list)

        if not reorder_df.empty:
            # Sort by urgency
            urgency_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
            reorder_df['urgency_rank'] = reorder_df['urgency'].map(urgency_order)
            reorder_df = reorder_df.sort_values('urgency_rank').drop('urgency_rank', axis=1)

        return reorder_df

    def _calculate_urgency(self, forecast: ForecastResult) -> str:
        """Calculate urgency level for reordering"""
        days_of_stock = forecast.current_stock / (forecast.predicted_demand / 30) if forecast.predicted_demand > 0 else 999

        if days_of_stock < 7:
            return 'critical'
        elif days_of_stock < 14:
            return 'high'
        elif days_of_stock < 30:
            return 'medium'
        else:
            return 'low'

    def get_alert_summary(self) -> Dict:
        """Get summary of all alerts and actions"""
        return {
            'total_alerts': len(self.alerts),
            'total_actions': len(self.actions_taken),
            'critical_alerts': len([a for a in self.alerts if 'CRITICAL' in a['message']]),
            'pending_actions': len([a for a in self.actions_taken if a['status'] == 'pending'])
        }
