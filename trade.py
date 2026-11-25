
import pandas as pd

# Load trades
df = pd.read_csv("trades_test.csv")

results = []

for _, trade in df.iterrows():

    quantity = trade["quantity"]
    price = trade["price"]
    action = trade["action"]
    if (
        pd.isna(quantity)
        or pd.isna(price)
        or quantity <= 0
        or price <= 0
        or action not in ["Buy", "Sell"]
    ):
        decision = "Rejected"
        reason = "Invalid trade data."

    else:
        decision = "Needs Manual Sign-off"
        reason = "Portfolio reference data unavailable."

    results.append({
        "portfolio_id": trade["portfolio_id"],
        "security_id": trade["security_id"],
        "action": action,
        "quantity": quantity,
        "price": price,
        "security_type": trade["security_type"],
        "decision": decision,
        "reason": reason
    })
output = pd.DataFrame(results)
output.to_csv("trade_compliance_results.csv", index=False)
print(output)

print("\nResults saved to trade_compliance_results.csv")