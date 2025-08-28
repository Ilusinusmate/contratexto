from src.domain.managers.connection_manager import ConnectionManager
from src.domain.managers.game_manager import GameStateManager
from src.models.instructions import BaseInstruction, SetNameInstruction, AskHintInstruction, CheckWordPositionInstruction, FrozenInstruction
from src.models.responses import BaseResponse, SetNameResponse, FrozenResponse, WordPositionResponse, ErrorResponse

class InstructionInterpreter():
    def __init__(
        self,
        game_manager: GameStateManager,
        connection_manager: ConnectionManager,
    ):
        self.game_manager = game_manager
        self.connection_manager = connection_manager



    def create_instruction(self, instruction: dict) -> BaseInstruction:
        match (instruction.get("type")):
            case "SET_NAME":
                return SetNameInstruction(**instruction)
            case "FROZEN":
                return FrozenInstruction(**instruction)
            case "HINT":
                return AskHintInstruction(**instruction)
            case "WORD":
                return CheckWordPositionInstruction(**instruction)
            case _:
                return BaseInstruction(**instruction)



    def execute_instruction(self, instruction: BaseInstruction) -> BaseResponse | None:
        if (instruction is BaseInstruction):
            return None
        
        if (instruction is SetNameInstruction):
            return self.set_name_instruction(instruction)

        if self.check_is_frozen(instruction):
            return FrozenResponse(
                status=False, 
                connection_id=instruction.connection_id,
            )

        if (instruction is CheckWordPositionInstruction):
            return self.check_word_position_instruction()

        if not self.can_use_perk(instruction):
            return ErrorResponse(
                error="Todos os perks já foram usados",
                connection_id=instruction.connection_id
            )

        if (instruction is FrozenInstruction):
            return self.freeze_instruction(instruction)

        if (instruction is AskHintInstruction):
            return self.ask_hint_instruction()



    def check_is_frozen(self, object: BaseInstruction) -> bool:
        return self.game_manager.is_player_frozen(object.connection_id)



    def can_use_perk(self, object: BaseInstruction) -> bool:
        return self.game_manager.can_use_perk(object.connection_id)



    def freeze_instruction(self, object: FrozenInstruction) -> ErrorResponse | None:
        self.game_manager.freeze_player(object.player_to_freeze_id)
        return None


    def ask_hint_instruction(self, object: AskHintInstruction):
        # TODO: implement
        raise NotImplementedError()
    


    def check_word_position_instruction(
        self,
        object: CheckWordPositionInstruction,
    ) -> WordPositionResponse:
        # TODO: implement
        raise NotImplementedError()



    def set_name_instruction(self, object: SetNameInstruction) -> SetNameResponse:
        self.game_manager.set_player_name(
            object.connection_id,
            object.nick_name,
        )
        return SetNameResponse(
            status=True,
            new_nick_name=object.nick_name,
            connection_id=object.connection_id
        )

        