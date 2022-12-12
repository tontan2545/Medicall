from typing import TypedDict, Optional, Union, Dict


class Message(TypedDict):
    topic: Optional[str]
    payload: Optional[Union[str, Dict]]
