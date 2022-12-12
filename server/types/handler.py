from dataclasses import dataclass
from typing import Callable, Dict, Optional

from server.database import Database
from server.mqtt import MQTT
from server.serial import STM32Serial
from server.types.message import Message


@dataclass
class Handler:
    mqtt: MQTT
    serial: STM32Serial
    db: Database
    msg: Message
    patient_id: Optional[str]
    user_data: Dict
    sensor_data: Dict
    next: Callable
