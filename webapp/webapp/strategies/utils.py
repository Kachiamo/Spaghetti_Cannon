from .strategies import (
    BuyHoldTradingStrategy,
    DCATradingStrategy,
    SMATradingStrategy,
    RSITradingStrategy,
)


STRATEGIES = {
    BuyHoldTradingStrategy.id: BuyHoldTradingStrategy,
    DCATradingStrategy.id: DCATradingStrategy,
    SMATradingStrategy.id: SMATradingStrategy,
    RSITradingStrategy.id: RSITradingStrategy,
}

STRATEGY_CHOICES = [
    (BuyHoldTradingStrategy.id, BuyHoldTradingStrategy.name),
    (DCATradingStrategy.id, DCATradingStrategy.name),
    (SMATradingStrategy.id, SMATradingStrategy.name),
    (RSITradingStrategy.id, RSITradingStrategy.name),
]
