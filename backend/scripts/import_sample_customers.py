"""Import sample customers from JSON data"""
import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from liquor_agent.core.database import AsyncSessionLocal
from liquor_agent.models.customer import Customer


async def import_customers():
    """Import sample customers from data/agent_knowledge_base.json"""
    # Load sample data - try multiple paths
    possible_paths = [
        Path("/app/data/agent_knowledge_base.json"),  # Docker path
        Path(__file__).parent.parent.parent.parent / "data" / "agent_knowledge_base.json",
    ]
    
    data_file = None
    for path in possible_paths:
        if path.exists():
            data_file = path
            break
    
    if not data_file:
        print(f"Data file not found in any of: {possible_paths}")
        return
    
    with open(data_file) as f:
        customers_data = json.load(f)
    
    async with AsyncSessionLocal() as db:
        for customer_data in customers_data:
            # Extract data
            profile = customer_data.get("profile", {})
            seg = customer_data.get("segmentation", {})
            behavioral = customer_data.get("behavioral_traits", {})
            financial = customer_data.get("financial_metrics", {})
            product_prefs = customer_data.get("product_preferences", {})
            
            # Create customer
            customer = Customer(
                email=profile.get("email", "unknown@example.com"),
                name=profile.get("name", "Customer"),
                phone=profile.get("phone"),
                rfm_segment=seg.get("rfm_segment"),
                churn_risk=seg.get("churn_risk", "low").lower(),
                is_night_buyer=behavioral.get("night_buyer", "No").lower() == "yes",
                success_rate_pct=financial.get("success_rate_pct"),
                total_spent=financial.get("total_spent", 0),
                avg_order_value=financial.get("avg_order_value", 0),
                primary_category=product_prefs.get("primary_category"),
                secondary_category=product_prefs.get("secondary_category"),
                raw_data=customer_data
            )
            
            db.add(customer)
        
        await db.commit()
        print(f"✅ Imported {len(customers_data)} customers")


if __name__ == "__main__":
    asyncio.run(import_customers())

