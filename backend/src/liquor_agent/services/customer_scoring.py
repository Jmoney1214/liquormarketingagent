"""Customer scoring service using existing subagent logic"""
from typing import Dict, Any, List


class CustomerScoringService:
    """Service for scoring and ranking customers using subagent logic"""
    
    @staticmethod
    def score_customer(customer: Dict[str, Any]) -> float:
        """
        Score a customer based on churn risk, behavior, and value.
        
        Uses the existing scoring logic from src/liquor_agent/subagent.py
        
        Args:
            customer: Customer data dictionary
            
        Returns:
            Priority score (higher = more important to target)
        """
        score = 0.0
        
        # Extract data (handle both flat and nested structures)
        segmentation = customer.get("segmentation", {}) or {}
        behavioral_traits = customer.get("behavioral_traits", {}) or {}
        financial_metrics = customer.get("financial_metrics", {}) or {}
        
        # Also check for flat structure (from database)
        churn_risk = (customer.get("churn_risk") or segmentation.get("churn_risk", "")).lower()
        rfm_segment = customer.get("rfm_segment") or segmentation.get("rfm_segment", "")
        success_rate = customer.get("success_rate_pct") or financial_metrics.get("success_rate_pct")
        is_night_buyer = customer.get("is_night_buyer") or behavioral_traits.get("night_buyer", "").lower() == "yes"
        
        # Churn risk scoring (highest priority)
        if churn_risk == "high":
            score += 50
        elif churn_risk == "medium":
            score += 10
        
        # Success rate (lower success rate = higher priority)
        if success_rate is not None and isinstance(success_rate, (int, float)) and success_rate < 50:
            score += 15
        
        # Night buyer behavior
        if is_night_buyer:
            score += 5
        
        # High value customers
        if rfm_segment and ("Very_Frequent" in rfm_segment or "High_Value" in rfm_segment):
            score += 8
        
        return float(score)
    
    @staticmethod
    def generate_nudge(customer: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized offer and messaging for a customer.
        
        Uses the existing nudge logic from src/liquor_agent/subagent.py
        
        Args:
            customer: Customer data dictionary
            
        Returns:
            Dictionary with offer, message, and send_window
        """
        # Extract data
        product_prefs = customer.get("product_preferences", {}) or {}
        segmentation = customer.get("segmentation", {}) or {}
        
        # Also check flat structure
        primary_category = (customer.get("primary_category") or 
                           product_prefs.get("primary_category", "Mixed")).lower()
        churn_risk = (customer.get("churn_risk") or 
                     segmentation.get("churn_risk", "")).lower()
        rfm_segment = customer.get("rfm_segment") or segmentation.get("rfm_segment", "Unknown")
        
        # Default offer
        offer = "Discovery pack 3-for-2"
        message = "Convenience + scarcity framing"
        
        # Churn-based offers
        if churn_risk == "high":
            offer = "20% win-back discount"
        # Category-based offers
        elif any(k in primary_category for k in ["tequila", "whiskey"]):
            offer = "Premium bundle 15% off"
        elif any(k in primary_category for k in ["rum", "vodka", "beer", "wine"]):
            offer = "Value bundle $50+ free delivery"
        
        # Segment-based offers
        if "Low_Value_Frequent" in rfm_segment:
            offer = "Bundle uplift: buy 2 get 10% off"
        
        # Send window (evening hours when liquor purchases peak)
        send_window = ["18:00", "22:00"]
        
        return {
            "offer": offer,
            "message": message,
            "send_window": send_window,
            "channels": ["Email", "SMS"]
        }
    
    @classmethod
    def rank_and_generate_actions(
        cls,
        customers: List[Dict[str, Any]],
        limit: int = 300
    ) -> List[Dict[str, Any]]:
        """
        Score, rank, and generate actions for customers.
        
        This implements the full subagent workflow.
        
        Args:
            customers: List of customer dictionaries
            limit: Maximum number of actions to generate
            
        Returns:
            List of action dictionaries with customer, offer, and targeting info
        """
        # Score all customers
        scored_customers = [
            {**customer, "_score": cls.score_customer(customer)}
            for customer in customers
        ]
        
        # Sort by score (descending) and take top N
        ranked = sorted(scored_customers, key=lambda x: x["_score"], reverse=True)[:limit]
        
        # Generate actions
        actions = []
        for customer in ranked:
            nudge = cls.generate_nudge(customer)
            
            # Get email and name
            profile = customer.get("profile", {})
            email = customer.get("email") or profile.get("email", "unknown@example.com")
            name = customer.get("name") or profile.get("name", "Customer")
            
            action = {
                "email": email,
                "name": name,
                "segment": customer.get("rfm_segment", "Unknown"),
                "primary_category": customer.get("primary_category", "Mixed"),
                "offer": nudge["offer"],
                "send_window": nudge["send_window"],
                "channel": nudge["channels"],
                "creative_hint": f"{customer.get('primary_category', 'Mixed')} focus | {nudge['message']}",
                "reason": "priority=churn/success_rate/behavior",
                "priority_score": customer["_score"]
            }
            actions.append(action)
        
        return actions

