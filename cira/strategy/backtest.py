from typing import List
import pandas as pd
import numpy as np
from cira.strategy import strategies
from cira.strategy import strategy


def fees(prices: np.ndarray, allocation: np.ndarray, fee_rate: float = 0.004) -> float:
    return fee_rate * np.matmul(prices.T, allocation)


def back_test(
    strat: strategy.Strategy,
    feature_data: pd.DataFrame,
    asset_prices: pd.DataFrame,
    capital=100_000.0,
    use_fees: bool = True,
    fee_rate: float = 0.004,
    allow_short_position: bool = False,
) -> pd.DataFrame:
    """
    DISCLAIMER:
    The results of this back test are based on historical data and do not guarantee future performance.
    The financial markets are inherently uncertain, and various factors can influence actual trading results.
    This back test is provided for educational and informational purposes only.
    Users should exercise caution and conduct additional research before applying any trading strategy in live markets.
    """
    portfolio_history = {
        "value": [],
        "timestamp": [],
    }
    assert len(feature_data) == len(asset_prices)
    total_value = capital
    nr_of_asset = np.zeros([len(asset_prices.keys())], float)
    i = 0
    for t, cur_price in asset_prices.iterrows():
        # if len(asset_prices) == i + 1:
        #    break
        if total_value > 0:
            f_data = feature_data.iloc[: i + 1]
            p_data = asset_prices.iloc[: i + 1]
            allocation = strat.iterate(f_data, p_data, nr_of_asset.copy(), capital)
            assert len(allocation) == len(
                nr_of_asset
            ), "tried to allocating more assets then is available"
            for a, _ in enumerate(allocation):
                if capital <= 0.0 and allocation[a] < 0.0:
                    allocation[a] = 0
                elif nr_of_asset[a] + allocation[a] < 0.0 and not allow_short_position:
                    allocation[a] = -nr_of_asset[a]
            asking = float(
                np.matmul(cur_price.values.T, allocation)
                + use_fees
                * fees(cur_price.values, np.abs(allocation), fee_rate=fee_rate)
            )
            if asking <= capital and capital > 0.0:
                capital -= asking
                nr_of_asset += allocation
            total_value = np.matmul(cur_price.values.T, nr_of_asset) + capital
        else:
            total_value = np.matmul(cur_price.values.T, nr_of_asset) + capital

        portfolio_history["timestamp"].append(t)
        portfolio_history["value"].append(total_value)
        i += 1

    df = pd.DataFrame(portfolio_history)
    df = df.set_index("timestamp")
    df.index = pd.to_datetime(df.index.get_level_values("timestamp"))
    df.rename(columns={"value": strat.name}, inplace=True)
    return df


def multi_strategy_backtest(
    strats: List[strategy.Strategy],
    feature_data: pd.DataFrame,
    asset_prices: pd.DataFrame,
    capital=100_000.0,
    use_fees: bool = True,
    fee_rate: float = 0.004,
    allow_short_position: bool = False,
):
    result = pd.DataFrame()
    result.index = asset_prices.index
    for s in strats:
        s_result = back_test(
            s,
            feature_data=feature_data,
            asset_prices=asset_prices,
            capital=capital,
            use_fees=use_fees,
            fee_rate=fee_rate,
            allow_short_position=allow_short_position,
        )
        result[s.name] = s_result[s.name]
    return result


def back_test_against_buy_and_hold(
    strat: strategy.Strategy,
    feature_data: pd.DataFrame,
    asset_prices: pd.DataFrame,
    capital=100_000.0,
    use_fees: bool = True,
    fee_rate: float = 0.004,
    allow_short_position: bool = False,
):
    use_fees *= use_fees # for buy and hold 
    buy_and_hold = strategies.BuyAndHold(fee_rate=fee_rate)
    return multi_strategy_backtest(
        strats=[strat, buy_and_hold],
        feature_data=feature_data,
        asset_prices=asset_prices,
        capital=capital,
        use_fees=use_fees,
        fee_rate=fee_rate,
        allow_short_position=allow_short_position,
    )
