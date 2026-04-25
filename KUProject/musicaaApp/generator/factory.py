from django.conf import settings
from .mock_strategy import MockSongGeneratorStrategy
from .suno_strategy import SunoSongGeneratorStrategy

def get_generator_strategy():
    """
    Factory function to retrieve the active generation strategy
    based on the GENERATOR_STRATEGY setting.
    """
    strategy_name = getattr(settings, 'GENERATOR_STRATEGY', 'mock').lower()

    if strategy_name == 'suno':
        return SunoSongGeneratorStrategy()
    elif strategy_name == 'mock':
        return MockSongGeneratorStrategy()
    else:
        # Fallback to mock if an unknown strategy is specified
        return MockSongGeneratorStrategy()
