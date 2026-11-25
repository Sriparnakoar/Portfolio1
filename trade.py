
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
import math
portfolios = {}
with open("portfolios_test.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        portfolio_id = row["portfolio_id"]
        if portfolio_id not in portfolios:
            portfolios[portfolio_id] = {
                "cash_balance": float(row["cash_balance"]),
                "restricted_securities": [],
                "max_position_pct": float(row["max_position_pct"]),
                "current_holdings": []
            }
            restricted = row["restricted_securities"].strip()
            if restricted:
                portfolios[portfolio_id]["restricted_securities"] = (
                    restricted.split(";")
                )
        security_id = row["security_id"].strip()
        if security_id:

            portfolios[portfolio_id]["current_holdings"].append({
                "security_id": security_id,
                "quantity": float(row["quantity"]),
                "market_price": float(row["market_price"])
            })
def check_trade(trade):

    portfolio_id = trade["portfolio_id"].strip()
    security_id = trade["security_id"].strip()
    action = trade["action"].strip().capitalize()

    # STEP 1: VALIDATION

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

    # GET PORTFOLIO DATA

    portfolio = portfolios.get(portfolio_id)

    if portfolio is None:
        return "Rejected", "Portfolio not found."

    cash_balance = portfolio["cash_balance"]

    restricted = portfolio["restricted_securities"]

    holdings = portfolio["current_holdings"]

    max_position_pct = portfolio["max_position_pct"]

    # FIND EXISTING HOLDINGS

    existing_quantity = 0

    for holding in holdings:

        if holding["security_id"] == security_id:

            existing_quantity += holding["quantity"]
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
                    holding["quantity"] * holding["market_price"]
                )

                value_of_other_holdings += holding_value

        total_portfolio_value_after = (
            post_trade_cash
            + post_trade_value
            + value_of_other_holdings
        )
        if total_portfolio_value_after <= 0:
            return "Rejected", "Invalid portfolio value."

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

    writer = csv.DictWriter(file, fieldnames=fieldnames)

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
print("\nTOTAL TRADES:", len(results))

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
