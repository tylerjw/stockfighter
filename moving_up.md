# Moving up in the world!
Reminder: These instructions are always available under the Instructions tab if you need to see them again.

After your impressive performance at your last job, you've moved on to Fielding, Suzuki, and Johnson. Warning: the gloves are off, now. Here is account FSJ39191529 and a mandate from one of our clients, a pension fund: they want you to purchase them 100,000 shares of OceanRiver Holdings (ORH). (Their asset manager thinks the company will have market-beating performance over the next few years. Maybe they're right, maybe they're not, but either way we get paid and I'm investing my bonus in cat food futures.)

This is called a block trade -- 100,000 shares is a lot of ORH to buy all at once, so the presence of someone wanting to do it suggests that someone who is smart and rich has better-than-market information about the stock. Executing block trades is one of the core problems of trading.

Why? Here's one of the reasons we on the sell-side make the big bucks: the client could try to buy these shares themselves, but if they just did the obvious thing and put in an order for 100,000 shares, they'd get shellacked.

Why? Supply and demand: sudden demand for a product with limited supply, like liquid shares of a stock, makes the market clearing price go up. Also, supply and demand: if you supply a sucker who broadcasts his intentions loudly, capitalism demands that the rest of the market eat the sucker alive. So instead you've got to be sneaky-sneaky about how you accumulate those 100,000 shares.

Luckily, this market maker is dumb as a box of rocks. They don't seem to remember prior orders well at all. You could probably get the full allocation done just by calling them up all day and ordering a few shares here and a few shares there... but I hear you're a programmer, and the stock exchange has an API, so why do anything manual and repetitive when you have a for loop available?

Your Goal
Purchase 100,000 shares of ORH.
Avoid causing a "price impact" -- our client wants these shares for the cheapest price possible, naturally.
You'll Be Fired If
You cause an excessive price impact in the stock. What's "excessive"? It's up to the risk desk.
You take too long. The client doesn't need their shares this instant but they want them quickly.
The market moves against you. What, that's unfair? Welcome to Wall Street, kid.
A Note From Starfighter:

We abstract the notion of time in Stockfighter. On this level, one trading day in the simulated world corresponds to about five seconds of wall-clock time. In real life, the market generally has off periods between trading days, but most of our levels don't -- our bots don't need sleep. Well, OK, technically speaking they do sleep() while waiting on you... like right now, because you're reading while you could be trading. Get coding!
