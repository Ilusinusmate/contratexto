from pydantic import BaseModel

class BaseInstruction(BaseModel):
    type: str
    connection_id: str


class SetNameInstruction(BaseInstruction):
    nick_name: str


class CheckWordPositionInstruction(BaseInstruction):
    word: str


class AskHintInstruction(BaseInstruction):
    pass

class FrozenInstruction(BaseInstruction):
    player_to_freeze_id: str

