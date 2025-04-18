import pandas as pd
from typing import Dict

def get_chart_data(text: str) -> Dict:
    # You can enhance this later to parse actual expense entries
    categories = ['Housing', 'Food', 'Transportation', 'Utilities', 'Entertainment']
    amounts = [1200, 800, 500, 300, 200]

    df = pd.DataFrame({
        'Category': categories,
        'Amount': amounts,
        'Month': ['Jan', 'Jan', 'Jan', 'Jan', 'Jan']
    })

    return {
        "pie": {
            "labels": df["Category"].tolist(),
            "datasets": [{
                "data": df["Amount"].tolist(),
                "backgroundColor": [
                    "#4F46E5", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899"
                ]
            }]
        },
        "bar": {
            "labels": df["Month"].tolist(),
            "datasets": [{
                "label": "Monthly Expenditure ($)",
                "data": df["Amount"].tolist(),
                "backgroundColor": "#3B82F6"
            }]
        },
        "top": {
            "labels": df["Category"].tolist(),
            "datasets": [{
                "label": "Top Categories ($)",
                "data": df["Amount"].tolist(),
                "backgroundColor": ["#F59E0B", "#3B82F6", "#10B981", "#8B5CF6", "#EC4899"]
            }]
        },
        "line": {
            "labels": ["Jan", "Feb", "Mar"],
            "datasets": [{
                "label": "Cumulative Spend ($)",
                "data": [800, 1600, 2500],
                "borderColor": "#10B981",
                "backgroundColor": "#D1FAE5",
                "fill": True,
                "tension": 0.4
            }]
        }
    }