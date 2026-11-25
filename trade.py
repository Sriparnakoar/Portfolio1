
# # import pandas as pd

# # # Load trades
# # df = pd.read_csv("trades_test.csv")

# # results = []

# # for _, trade in df.iterrows():

# #     quantity = trade["quantity"]
# #     price = trade["price"]
# #     action = trade["action"]
# #     if (
# #         pd.isna(quantity)
# #         or pd.isna(price)
# #         or quantity <= 0
# #         or price <= 0
# #         or action not in ["Buy", "Sell"]
# #     ):
# #         decision = "Rejected"
# #         reason = "Invalid trade data."

# #     else:
# #         decision = "Needs Manual Sign-off"
# #         reason = "Portfolio reference data unavailable."

# #     results.append({
# #         "portfolio_id": trade["portfolio_id"],
# #         "security_id": trade["security_id"],
# #         "action": action,
# #         "quantity": quantity,
# #         "price": price,
# #         "security_type": trade["security_type"],
# #         "decision": decision,
# #         "reason": reason
# #     })
# # output = pd.DataFrame(results)
# # output.to_csv("trade_compliance_results.csv", index=False)
# # print(output)

# # print("\nResults saved to trade_compliance_results.csv")




# import csv
# import math
# portfolios = {}
# with open("portfolios_test.csv", "r") as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         portfolio_id = row["portfolio_id"]
#         if portfolio_id not in portfolios:
#             portfolios[portfolio_id] = {
#                 "cash_balance": float(row["cash_balance"]),
#                 "restricted_securities": [],
#                 "max_position_pct": float(row["max_position_pct"]),
#                 "current_holdings": []
#             }
#             restricted = row["restricted_securities"].strip()
#             if restricted:
#                 portfolios[portfolio_id]["restricted_securities"] = (
#                     restricted.split(";")
#                 )
#         security_id = row["security_id"].strip()
#         if security_id:

#             portfolios[portfolio_id]["current_holdings"].append({
#                 "security_id": security_id,
#                 "quantity": float(row["quantity"]),
#                 "market_price": float(row["market_price"])
#             })
# def check_trade(trade):

#     portfolio_id = trade["portfolio_id"].strip()
#     security_id = trade["security_id"].strip()
#     action = trade["action"].strip().capitalize()
#     try:
#         quantity = float(trade["quantity"])
#         price = float(trade["price"])

#     except (ValueError, TypeError):
#         return "Rejected", "Invalid trade data."

#     if (
#         not math.isfinite(quantity)
#         or not math.isfinite(price)
#         or quantity <= 0
#         or price <= 0
#         or action not in ["Buy", "Sell"]
#     ):

#         return "Rejected", "Invalid trade data."
#     portfolio = portfolios.get(portfolio_id)

#     if portfolio is None:
#         return "Rejected", "Portfolio not found."
#     cash_balance = portfolio["cash_balance"]
#     restricted = portfolio["restricted_securities"]
#     holdings = portfolio["current_holdings"]
#     max_position_pct = portfolio["max_position_pct"]
#     existing_quantity = 0

#     for holding in holdings:

#         if holding["security_id"] == security_id:

#             existing_quantity += holding["quantity"]
#     if security_id in restricted:
#         return (
#             "Rejected",
#             "Security is restricted for this portfolio."
#         )
#     if action == "Sell":
#         if existing_quantity < quantity:

#             return (
#                 "Rejected",
#                 "Insufficient holdings to sell."
#             )
#     if action == "Buy":
#         trade_cost = quantity * price
#         if trade_cost > cash_balance:
#             return (
#                 "Rejected",
#                 "Insufficient cash for this buy order."
#             )
#         post_trade_cash = cash_balance - trade_cost
#         post_trade_quantity = existing_quantity + quantity
#         post_trade_value = post_trade_quantity * price
#         value_of_other_holdings = 0
#         for holding in holdings:

#             if holding["security_id"] != security_id:

#                 holding_value = (
#                     holding["quantity"] * holding["market_price"]
#                 )

#                 value_of_other_holdings += holding_value

#         total_portfolio_value_after = (
#             post_trade_cash
#             + post_trade_value
#             + value_of_other_holdings
#         )
#         if total_portfolio_value_after <= 0:
#             return "Rejected", "Invalid portfolio value."

#         position_pct = (
#             post_trade_value / total_portfolio_value_after
#         )
#         if position_pct > max_position_pct:

#             return (
#                 "Needs Manual Sign-off",
#                 "Exceeds maximum position concentration — "
#                 "requires approval."
#             )
#     return "Approved", "Trade passed all compliance checks."
# results = []

# with open("trades_test.csv", "r") as file:
#     reader = csv.DictReader(file)
#     for trade in reader:
#         decision, reason = check_trade(trade)
#         results.append({
#             "portfolio_id": trade["portfolio_id"],
#             "security_id": trade["security_id"],
#             "action": trade["action"],
#             "quantity": trade["quantity"],
#             "price": trade["price"],
#             "security_type": trade["security_type"],
#             "decision": decision,
#             "reason": reason

#         })
# with open("trade_results.csv", "w", newline="") as file:

#     fieldnames = [
#         "portfolio_id",
#         "security_id",
#         "action",
#         "quantity",
#         "price",
#         "security_type",
#         "decision",
#         "reason"
#     ]

#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(results)
# print("\nPORTFOLIO TRADE COMPLIANCE RESULTS")

# print("=" * 65)
# for result in results:
#     print(
#         result["portfolio_id"],
#         result["security_id"],
#         result["action"],
#         "=>",
#         result["decision"]
#     )
#     print("Reason:", result["reason"])
#     print("-" * 65)
# print("\nTOTAL TRADES:", len(results))

# print(
#     "Approved:",
#     sum(r["decision"] == "Approved" for r in results)
# )

# print(
#     "Rejected:",
#     sum(r["decision"] == "Rejected" for r in results)
# )

# print(
#     "Needs Manual Sign-off:",
#     sum(
#         r["decision"] == "Needs Manual Sign-off"
#         for r in results
#     )
# )
# print("\nResults saved to trade_results.csv")


import csv
import os
 
 
def is_positive_number(value):
    if value is None:
        return False
    if isinstance(value, bool):
        return False
    if not isinstance(value, (int, float)):
        return False
    return value > 0
 
 
def build_result(decision, reason):
    return {"decision": decision, "reason": reason}
 
 
def load_trades(filepath):
    trades = []
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            trade = {
                "portfolio_id": row.get("portfolio_id", "").strip(),
                "security_id": row.get("security_id", "").strip(),
                "action": row.get("action", "").strip(),
                "security_type": row.get("security_type", "").strip(),
            }
            try:
                trade["quantity"] = float(row.get("quantity", "").strip())
            except (ValueError, AttributeError):
                trade["quantity"] = None
            try:
                trade["price"] = float(row.get("price", "").strip())
            except (ValueError, AttributeError):
                trade["price"] = None
            trades.append(trade)
    return trades
 
 
def load_portfolio_reference(filepath):
    portfolios = {}
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            portfolio_id = row["portfolio_id"].strip()
            portfolio = portfolios.setdefault(
                portfolio_id,
                {
                    "restricted_securities": [],
                    "max_position_pct": float(row["max_position_pct"]),
                    "current_holdings": [],
                },
            )
 
            restricted_security = row["restricted_security"].strip()
            if (
                restricted_security
                and restricted_security not in portfolio["restricted_securities"]
            ):
                portfolio["restricted_securities"].append(restricted_security)
 
            portfolio["current_holdings"].append(
                (
                    row["holding_security"].strip(),
                    float(row["holding_quantity"]),
                    float(row["holding_market_price"]),
                )
            )
    return portfolios
 
 
def collect_cash_balances(trades):
    portfolio_ids = []
    seen = set()
    for trade in trades:
        pid = trade["portfolio_id"]
        if pid and pid not in seen:
            portfolio_ids.append(pid)
            seen.add(pid)
 
    cash_balances = {}
    print("\n===== Enter Cash Balance for Each Portfolio =====\n")
    for pid in portfolio_ids:
        while True:
            user_input = input(f"  Cash balance for portfolio '{pid}': $")
            try:
                amount = float(user_input.strip())
                if amount < 0:
                    print("    Cash balance cannot be negative. Please try again.")
                    continue
                cash_balances[pid] = amount
                break
            except ValueError:
                print("    That is not a valid number. Please try again.")
    print()
    return cash_balances
 
 
def check_trade(trade, portfolio):
    security_id = trade.get("security_id")
    action = trade.get("action")
    quantity = trade.get("quantity")
    price = trade.get("price")
 
    if not is_positive_number(quantity) or not is_positive_number(price):
        return build_result("Rejected", "Invalid trade data.")
 
    if action not in ("Buy", "Sell"):
        return build_result("Rejected", "Invalid trade data.")
 
    quantity = float(quantity)
    price = float(price)
 
    restricted = portfolio.get("restricted_securities", [])
    if security_id in restricted:
        return build_result("Rejected", "Security is restricted for this portfolio.")
 
    holdings = {}
    for held_security, held_quantity, held_market_price in portfolio.get("current_holdings", []):
        holdings[held_security] = (float(held_quantity), float(held_market_price))
 
    if action == "Sell":
        held_quantity = holdings.get(security_id, (0.0, 0.0))[0]
        if held_quantity < quantity:
            return build_result("Rejected", "Insufficient holdings to sell.")
        return build_result("Approved", "Trade approved.")
 
    trade_cost = quantity * price
    cash_balance = float(portfolio.get("cash_balance", 0.0))
 
    if trade_cost > cash_balance:
        return build_result("Rejected", "Insufficient cash for this buy order.")
 
    max_position_pct = float(portfolio.get("max_position_pct", 1.0))
 
    post_trade_cash = cash_balance - trade_cost
 
    existing_quantity = holdings.get(security_id, (0.0, 0.0))[0]
    post_trade_quantity = existing_quantity + quantity
 
    post_trade_value_of_this_security = post_trade_quantity * price
 
    value_of_other_holdings = 0.0
    for held_security, (held_quantity, held_market_price) in holdings.items():
        if held_security != security_id:
            value_of_other_holdings += held_quantity * held_market_price
 
    total_portfolio_value_after = (
        post_trade_cash
        + post_trade_value_of_this_security
        + value_of_other_holdings
    )
 
    if total_portfolio_value_after == 0:
        position_pct = 1.0
    else:
        position_pct = post_trade_value_of_this_security / total_portfolio_value_after
 
    if position_pct > max_position_pct:
        return build_result(
            "Needs Manual Sign-off",
            "Exceeds maximum position concentration - requires approval.",
        )
 
    return build_result("Approved", "Trade approved.")
 
 
def print_results(results):
    header = (
        f"{'No.':<5} {'Portfolio':<12} {'Security':<14} {'Action':<7} "
        f"{'Qty':>8} {'Price':>10}  {'Decision':<24} Reason"
    )
    separator = "-" * len(header)
 
    print("\n===== Trade Compliance Results =====\n")
    print(header)
    print(separator)
 
    for index, result in enumerate(results, start=1):
        quantity_display = result.get("quantity", "N/A")
        price_display = result.get("price", "N/A")
 
        if isinstance(quantity_display, (int, float)):
            quantity_display = f"{quantity_display:>8.0f}"
        else:
            quantity_display = f"{'N/A':>8}"
 
        if isinstance(price_display, (int, float)):
            price_display = f"{price_display:>10.2f}"
        else:
            price_display = f"{'N/A':>10}"
 
        print(
            f"{index:<5} {result['portfolio_id']:<12} {result['security_id']:<14} "
            f"{result['action']:<7} {quantity_display} {price_display}  "
            f"{result['decision']:<24} {result['reason']}"
        )
 
    print(separator)
 
    approved_count = sum(1 for r in results if r["decision"] == "Approved")
    rejected_count = sum(1 for r in results if r["decision"] == "Rejected")
    manual_count = sum(1 for r in results if r["decision"] == "Needs Manual Sign-off")
 
    print(f"\nSummary: {len(results)} trades processed")
    print(f"  Approved:              {approved_count}")
    print(f"  Rejected:              {rejected_count}")
    print(f"  Needs Manual Sign-off: {manual_count}")
    print()
 

def main():

    csv_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "trades_test.csv"
    )

    reference_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "portfolio_reference.csv"
    )

    # Check whether trade CSV exists
    if not os.path.exists(csv_filename):
        print(f"Error: {csv_filename} not found.")
        return

    # Check whether portfolio reference CSV exists
    if not os.path.exists(reference_filename):
        print(f"Error: {reference_filename} not found.")
        return

    # Load portfolio reference data
    portfolio_reference_data = load_portfolio_reference(
        reference_filename
    )

    # Load trade data
    trades = load_trades(csv_filename)

    if not trades:
        print("No trades found in the CSV file.")
        return

    print(f"\nLoaded {len(trades)} trade(s).")

    # Collect cash balances
    cash_balances = collect_cash_balances(trades)

    results = []

    for trade in trades:

        portfolio_id = trade["portfolio_id"]

        reference_data = portfolio_reference_data.get(
            portfolio_id
        )

        if reference_data is None:

            outcome = build_result(
                "Rejected",
                "Portfolio not found in reference data."
            )

        else:

            portfolio = dict(reference_data)

            portfolio["cash_balance"] = cash_balances.get(
                portfolio_id, 0.0
            )

            outcome = check_trade(trade, portfolio)

        results.append({**trade, **outcome})

    # Display final results
    print_results(results)


if __name__ == "__main__":
    main()
