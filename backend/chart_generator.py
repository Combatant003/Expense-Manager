def get_chart_data(insight_json: dict) -> dict:
    categories = insight_json.get("categories", [])
    monthly = insight_json.get("monthly_trend", [])

    pie_labels = [c["category"] for c in categories]
    pie_data = [int(c["amount"]) for c in categories]  # 👈 Force int here

    bar_labels = [m["month"] for m in monthly]
    bar_data = [int(m["amount"]) for m in monthly]     # 👈 Force int here

    cumulative = []
    total = 0
    for amt in bar_data:
        total += amt
        cumulative.append(total)

    return {
        "pie": {
            "labels": pie_labels,
            "datasets": [{
                "data": pie_data,
                "backgroundColor": [
                    "#4F46E5", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899", "#94A3B8"
                ]
            }]
        },
        "bar": {
            "labels": bar_labels,
            "datasets": [{
                "label": "Monthly Expenditure ($)",
                "data": bar_data,
                "backgroundColor": "#3B82F6"
            }]
        },
        "top": {
            "labels": pie_labels,
            "datasets": [{
                "label": "Top Categories ($)",
                "data": pie_data,
                "backgroundColor": ["#F59E0B", "#3B82F6", "#10B981", "#8B5CF6", "#EC4899"]
            }]
        },
        "line": {
            "labels": bar_labels,
            "datasets": [{
                "label": "Cumulative Spend ($)",
                "data": cumulative,
                "borderColor": "#10B981",
                "backgroundColor": "#D1FAE5",
                "fill": True,
                "tension": 0.4
            }]
        }
    }