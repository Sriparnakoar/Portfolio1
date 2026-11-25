
# import pandas as pd

# # Load trades
# df = pd.read_csv("trades_test.csv")

# results = []

# for _, trade in df.iterrows():

#     quantity = trade["quantity"]
#     price = trade["price"]
#     action = trade["action"]
#     if (
#         pd.isna(quantity)
#         or pd.isna(price)
#         or quantity <= 0
#         or price <= 0
#         or action not in ["Buy", "Sell"]
#     ):
#         decision = "Rejected"
#         reason = "Invalid trade data."

#     else:
#         decision = "Needs Manual Sign-off"
#         reason = "Portfolio reference data unavailable."

#     results.append({
#         "portfolio_id": trade["portfolio_id"],
#         "security_id": trade["security_id"],
#         "action": action,
#         "quantity": quantity,
#         "price": price,
#         "security_type": trade["security_type"],
#         "decision": decision,
#         "reason": reason
#     })
# output = pd.DataFrame(results)
# output.to_csv("trade_compliance_results.csv", index=False)
# print(output)

# print("\nResults saved to trade_compliance_results.csv")



import csv
import json
import math
with open("portfolios.json", "r") as file:
    portfolios = json.load(file)
def check_trade(trade):
    portfolio_id = trade["portfolio_id"]
    security_id = trade["security_id"]
    action = trade["action"].strip().capitalize()

    try:
        quantity = float(trade["quantity"])
        price = float(trade["price"])
    except (ValueError, TypeError):
        return "Rejected", "Invalid trade data."
    if (
        not math.isfinite(quantity)
        or not math.isfinite(price)
        or quantity <= 0
        or price <= 0
        or action not in ["Buy", "Sell"]
    ):
        return "Rejected", "Invalid trade data."
    portfolio = portfolios.get(portfolio_id)

    if portfolio is None:
        return "Rejected", "Portfolio not found."

    cash_balance = float(portfolio["cash_balance"])
    restricted = portfolio["restricted_securities"]
    holdings = portfolio["current_holdings"]
    max_position_pct = float(portfolio["max_position_pct"])
    existing_quantity = 0

    for holding in holdings:
        if holding["security_id"] == security_id:
            existing_quantity += float(holding["quantity"])
    if security_id in restricted:
        return (
            "Rejected",
            "Security is restricted for this portfolio."
        )
    if action == "Sell":

        if existing_quantity < quantity:
            return (
                "Rejected",
                "Insufficient holdings to sell."
            )

    if action == "Buy":

        trade_cost = quantity * price

        if trade_cost > cash_balance:
            return (
                "Rejected",
                "Insufficient cash for this buy order."
            )

        post_trade_cash = cash_balance - trade_cost
        post_trade_quantity = existing_quantity + quantity
        post_trade_value = post_trade_quantity * price
        value_of_other_holdings = 0
        for holding in holdings:

            if holding["security_id"] != security_id:

                holding_value = (
                    float(holding["quantity"])
                    * float(holding["market_price"])
                )

                value_of_other_holdings += holding_value

        total_portfolio_value_after = (
            post_trade_cash
            + post_trade_value
            + value_of_other_holdings
        )

        if total_portfolio_value_after <= 0:
            return (
                "Rejected",
                "Invalid portfolio value."
            )

        position_pct = (
            post_trade_value / total_portfolio_value_after
        )

        if position_pct > max_position_pct:

            return (
                "Needs Manual Sign-off",
                "Exceeds maximum position concentration — "
                "requires approval."
            )
    return "Approved", "Trade passed all compliance checks."
results = []

with open("trades_test.csv", "r") as file:

    reader = csv.DictReader(file)

    for trade in reader:

        decision, reason = check_trade(trade)

        results.append({
            "portfolio_id": trade["portfolio_id"],
            "security_id": trade["security_id"],
            "action": trade["action"],
            "quantity": trade["quantity"],
            "price": trade["price"],
            "security_type": trade["security_type"],
            "decision": decision,
            "reason": reason
        })
with open("trade_results.csv", "w", newline="") as file:

    fieldnames = [
        "portfolio_id",
        "security_id",
        "action",
        "quantity",
        "price",
        "security_type",
        "decision",
        "reason"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(results)
print("\nPORTFOLIO TRADE COMPLIANCE RESULTS")
print("=" * 65)

for result in results:

    print(
        result["portfolio_id"],
        result["security_id"],
        result["action"],
        "=>",
        result["decision"]
    )

    print("Reason:", result["reason"])
    print("-" * 65)


print("\nTotal trades:", len(results))

print(
    "Approved:",
    sum(r["decision"] == "Approved" for r in results)
)

print(
    "Rejected:",
    sum(r["decision"] == "Rejected" for r in results)
)

print(
    "Needs Manual Sign-off:",
    sum(
        r["decision"] == "Needs Manual Sign-off"
        for r in results
    )
)
print("\nResults saved to trade_results.csv")
