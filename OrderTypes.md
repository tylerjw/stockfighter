# Order Types
Stock exchanges give people placing orders limited control over the execution of those orders, in particular, under what circumstances the order "rests on" (goes into) the order book.

The order book is the data structure that makes a stock exchange a stock exchange: it is two queues, ordered by priority, of all offers to buy a stock ("bids" -- remember, b is for buy) and offers to sell a stock ("asks"). In Stockfighter, most exchanges implement price-time priority -- a "better" price always gets matched before a worse price, with ties getting broken by timestamp of the order.

Concrete example: The order book contains 3 asks: 2 @ $98, 3 @ $100 (placed 5 minutes ago), and 5 @ $100 (placed 4 minutes ago). An order comes in: limit buy 8 @ $105.

This order matches: 1. 2 @ $98. The order still has 6 shares unsatisfied, so it continues. 2. 3 @ $100. We match the order for 3, not the order for 5, because the order for 3 is older. The order still has 3 shares unsatisfied, so it continues. 3. 3 @ $100. This fully satisfies the incoming order. The resting ask for 5 now has only 2 shares left remaining.

An execution notice ("Hey, one of your orders just got a fill") is sent to the party sending in the order and the three parties which placed each of the resting orders. (In Stockfighter, for convenience, we also return the executions in the HTTP response to the API call placing the order. This affordance is unlikely in the real world.)

Note that, despite the fact that the buyer was willing to pay up to $105 per share, they actually got 8 shares for $790 ($98.75 each). Buyers sometimes pay less than they expected to. Sellers sometimes get more than they expected for their shares. The reverse never happens.

Limit orders (in API, "limit"): The most common order type, which works as specified above.
Market orders (in API, "market"): An order type you should never use for any reason, most especially not because you're a retail trader or an evil level designer suggested you try it. A market order doesn't specify a price -- it just continues matching orders until it is filled or it has exhausted one side of the order book. It never rests on the order book. Market orders routinely blow up in the face of people placing them, because what happens when you do a market order for 10 shares against a book which has 9 @ $10 and 1 @ $12,000? Yep, you pay $12,090. Never ever ever use market orders.
Fill-or-Kill orders (in API, "fill-or-kill"): Fill-or-kill (FOK) orders let you specify a limit price, like a limit order, but never rest on the book. Also, they're all-or-nothing (AON, in Wall Street parlance). Normally, if you place an order for 10 shares and the market can only give you 8, you get 8. With a FOK order, you get 0 (and the order gets immediately canceled).
Immediate-or-cancel orders (in API, "immediate-or-cancel"): Like FOK in that the order executes instantly and never rests on the book, but it isn't all-or-nothing. If you can only get 8 shares out of the 10 you wanted, you'll get the 8 shares.
