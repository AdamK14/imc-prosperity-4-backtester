"""Aggressive OSMIUM strategies to audit the ceiling gap."""
from datamodel import Order, OrderDepth, TradingState, Trade, Observation, Listing

PRODUCT = "ASH_COATED_OSMIUM"
LIMIT = 80

class Trader:
    """Strategy A: Passive MM at exact bot prices (9992/10008), max size both sides."""
    def run(self, state):
        od = state.order_depths.get(PRODUCT)
        if not od: return {}, 0, ""
        bids = sorted(od.buy_orders.items(), reverse=True)
        asks = sorted(od.sell_orders.items())
        if not bids or not asks: return {}, 0, ""
        pos = state.position.get(PRODUCT, 0)
        best_bid = bids[0][0]
        best_ask = asks[0][0]
        orders = []
        buy_cap = max(0, LIMIT - pos)
        sell_cap = max(0, LIMIT + pos)
        if buy_cap > 0: orders.append(Order(PRODUCT, best_bid, buy_cap))
        if sell_cap > 0: orders.append(Order(PRODUCT, best_ask, -sell_cap))
        return {PRODUCT: orders}, 0, ""
