from enum import Enum
from dataclasses import dataclass

class ButtonColor(Enum):
    ONE = '#3498db'
    TWO = '#2ecc71'

class TaskStatus(Enum):
    COMPLETED = 'completed'
    PENDING = 'pending'
    FAILED = 'failed'
    UNLOADED = 'unloaded'

@dataclass
class TaskColors:
    background: str
    text: str

class TaskColorScheme:
    COMPLETED = TaskColors('#d7ead4', '#338309')
    PENDING = TaskColors('#f5f5f5', '#c3beba')
    FAILED = TaskColors('#fdeded', '#BC0000')
    UNLOADED = TaskColors('#FFF8B9', '#FAAB01')

BACKGROUND_PANEL_COLOR = '#f0f0f0'
TASKS_TEXT_COLOR = '#120D0C'

NORMA_WATER_SUPPLY = [2.3, 3.2, 3.7, 4.4, 5.0, 3.65, 3.84, 4.56, 5.5, 6.84, 7.6, 5.02, 11.86]
NORMA_WASTEWATER_DISPOSAL = [3.65, 6.99, 4.56, 5.5, 6.84, 7.6, 9.12, 11.86]