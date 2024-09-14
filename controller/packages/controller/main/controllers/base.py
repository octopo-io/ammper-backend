from http import HTTPStatus
from typing import Optional
from typing import Tuple


class Controller:
    ACTIONS: list

    def __init__(self, action: str, data: dict):
        self._action = action
        self._data = data

    def _initial_check(self) -> Tuple[bool, Optional[Tuple[int, dict]]]:
        """
        Verifica que la acción solicitada sea válida.

        :return: True si la acción es válida, False si no lo es y datos de respuesta.
        """
        if self._action not in self.ACTIONS:
            return False, (
                HTTPStatus.BAD_REQUEST,
                {'error': 'invalid_action'}
            )
        return True, None

    def execute(self) -> Tuple[int, Optional[dict]]:
        """
        Ejecuta la acción solicitada.

        :return: Código de estado HTTP y datos de respuesta.
        """
        valid, error = self._initial_check()
        method = f'_{self._action}'
        return getattr(self, method)() if valid else error

    @property
    def data(self) -> dict:
        return self._data
