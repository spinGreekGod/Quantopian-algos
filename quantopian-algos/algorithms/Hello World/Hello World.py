"""
This algorithm trades once per week by going 100% long in AAPL.

For more teaching examples, check out the Quantopian Lecture Series:
https://www.quantopian.com/lectures
and the Tutorials:
https://www.quantopian.com/tutorials

Please direct any questions, feedback, or corrections to feedback@quantopian.com
"""

import quantopian.algorithm as algo
import quantopian.optimize as opt


def initialize(context):
    """
    A core function called automatically once at the beginning of a backtest.
    Use this function for initializing state or other bookkeeping.
    Parameters
    ----------
    context : AlgorithmContext
        An object that can be used to store state that you want to maintain in 
        your algorithm. context is automatically passed to initialize, 
        before_trading_start, handle_data, and any functions run via schedule_function.
        context provides the portfolio attribute, which can be used to retrieve information 
        about current positions.
    """
    # Reference to the AAPL security.
    context.aapl = sid(24)

    # Rebalance every day, one hour and a half after market open.
    algo.schedule_function(
        rebalance,
        algo.date_rules.every_day(),
        algo.time_rules.market_open(hours=1, minutes=30)
    )


def rebalance(context, data):
    """
    A function scheduled to run once every day at 10:30AM ET in order to
    rebalance the longs and shorts lists.
    Parameters
    ----------
    context : AlgorithmContext
        See description above.
    data : BarData
        An object that provides methods to get price and volume data, check
        whether a security exists, and check the last time a security traded.
    """
    # Target a 100% long allocation of our portfolio in AAPL.
    objective = opt.TargetWeights({context.aapl: 1.0})

    # The Optimize API allows you to define portfolio constraints, which can be
    # useful when you have a more complex objective. In this algorithm, we
    # don't have any constraints, so we pass an empty list.
    constraints = []

    # order_optimal_portfolio uses `objective` and `constraints` to find the
    # "best" portfolio weights (as defined by your objective) that meet all of
    # your constraints. Since our objective is just "target 100% in AAPL", and
    # we have no constraints, this will maintain 100% of our portfolio in AAPL.
    algo.order_optimal_portfolio(objective, constraints)
    