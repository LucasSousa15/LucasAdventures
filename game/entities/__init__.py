# game/entities/__init__.py
from .player import Player
from .cloud import Cloud
from .scenery import Scenery
from .camera import Camera
from .coin import Coin
from .coin_manager import CoinManager

__all__ = ['Player', 'Cloud', 'Scenery', 'Camera', 'Coin', 'CoinManager']