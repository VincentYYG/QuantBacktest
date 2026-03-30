import os
from strategies.registry import STRATEGY_REGISTRY


def create_strategy(strategy_name: str, tickers, min_history: int):
    if strategy_name not in STRATEGY_REGISTRY:
        raise ValueError(f"Unsupported strategy_name: {strategy_name}")

    registry_item = STRATEGY_REGISTRY[strategy_name]

    required_keys = ["strategy_class", "config_loader"]
    for key in required_keys:
        if key not in registry_item:
            raise KeyError(
                f"Missing key '{key}' in STRATEGY_REGISTRY for strategy '{strategy_name}'. "
                f"Available keys: {list(registry_item.keys())}"
            )

    strategy_class = registry_item["strategy_class"]
    config_loader = registry_item["config_loader"]

    config_path = os.path.join("config", "strategies", f"{strategy_name}.yaml")
    strategy_config = config_loader(config_path)

    strategy = strategy_class(
        tickers=tickers,
        config=strategy_config,
        min_history=min_history
    )

    return strategy, config_path
