from strategies.cross_sectional_momentum import CrossSectionalMomentumStrategy
from strategies.moving_average_crossover import MovingAverageCrossoverStrategy

from utils.config_loader import (
    load_cross_sectional_momentum_config,
    load_moving_average_crossover_config,
)

STRATEGY_REGISTRY = {
    "cross_sectional_momentum": {
        "strategy_class": CrossSectionalMomentumStrategy,
        "config_loader": load_cross_sectional_momentum_config,
    },
    "moving_average_crossover": {
        "strategy_class": MovingAverageCrossoverStrategy,
        "config_loader": load_moving_average_crossover_config,
    },
    ## You should take a REGISTRY for each of your strategies.
}