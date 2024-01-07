from .strategies import (
    BuyHoldTradingStrategy,
    DCATradingStrategy,
    SMATradingStrategy,
    RSITradingStrategy,
    ATRTradingStrategy,
    StochasticOscillatorTradingStrategy,
    MovingAverageConvergenceDivergenceTradingStrategy,
)


STRATEGIES = {
    BuyHoldTradingStrategy.id: BuyHoldTradingStrategy,
    DCATradingStrategy.id: DCATradingStrategy,
    SMATradingStrategy.id: SMATradingStrategy,
    RSITradingStrategy.id: RSITradingStrategy,
    ATRTradingStrategy.id: ATRTradingStrategy,
    StochasticOscillatorTradingStrategy.id: StochasticOscillatorTradingStrategy,
    MovingAverageConvergenceDivergenceTradingStrategy. id: MovingAverageConvergenceDivergenceTradingStrategy,
}

STRATEGY_CHOICES = [
    (BuyHoldTradingStrategy.id, BuyHoldTradingStrategy.name),
    (DCATradingStrategy.id, DCATradingStrategy.name),
    (SMATradingStrategy.id, SMATradingStrategy.name),
    (RSITradingStrategy.id, RSITradingStrategy.name),
    (ATRTradingStrategy.id, ATRTradingStrategy.name),
    (StochasticOscillatorTradingStrategy.id, StochasticOscillatorTradingStrategy.name),
    (MovingAverageConvergenceDivergenceTradingStrategy.id, MovingAverageConvergenceDivergenceTradingStrategy.name),
]
