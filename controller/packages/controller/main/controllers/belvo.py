import base64
import requests

from http import HTTPStatus
from typing import Optional
from typing import Tuple

from config import BELVO_BASE_URL
from config import BELVO_SECRET_ID
from config import BELVO_SECRET_KEY
from controllers.base import Controller
from db.dao import LinkDAO
from utils.jwt import get_jwt_data


class BelvoController(Controller):
    ACTIONS = [
        'get_institutions'
    ]
    user_data = {}

    def _initial_check(self) -> Tuple[bool, Optional[Tuple[int, dict]]]:
        """
        Verifica que el token JWT sea válido y obtiene los datos del usuario.

        :return: True si el token es válido, False si no lo es y datos de respuesta.
        """
        status, result = super()._initial_check()

        if not status:
            return status, result

        if data := get_jwt_data(self.data.get('jwt')):
            self.user_data = data
            return True, None

        return False, (
            HTTPStatus.UNAUTHORIZED,
            {'error': 'invalid_jwt'}
        )

    def _get_institutions(self):
        """
        Obtiene las instituciones financieras disponibles.

        :return: Código de estado HTTP y datos de respuesta.
        """
        response = requests.get(f'{BELVO_BASE_URL}/institutions/', headers=self._headers)
        return HTTPStatus.OK, response.json()

    def _get_or_create_link(self):
        """
        Crea un enlace de acceso a una institución financiera.

        :return: Código de estado HTTP y datos de respuesta.
        """
        link_dao = LinkDAO()
        institution = self.data.get('institution')
        user_id = self.user_data.get('id')

        if link := link_dao.get_by_institution_and_user_id(institution, user_id):
            return HTTPStatus.OK, {
                'link_id': link.link_id
            }

        response = requests.post(f'{BELVO_BASE_URL}/links/', json={
            'institution': institution,
            'username': 'bnk100',
            'password': 'full',
            'access_mode': 'recurrent',
            'external_id': user_id
        }, headers=self._headers)

        data = response.json()
        link_dao.create(
            link_id=data.get('id'),
            institution=institution,
            user_id=user_id
        )
        link_dao.close_session()

        return HTTPStatus.CREATED, {
            'link_id': data.get('id')
        }

    def _get_accounts(self):
        """
        Obtiene las cuentas de un usuario.

        :return: Código de estado HTTP y datos de respuesta.
        """
        link_id = self.data.get('link_id')
        response = requests.get(f'{BELVO_BASE_URL}/accounts/?link={link_id}', headers=self._headers)
        return HTTPStatus.OK, response.json()

    def _get_transactions(self):
        """
        Obtiene las transacciones de una cuenta.

        :return: Código de estado HTTP y datos de respuesta.
        """
        account_id = self.data.get('account_id')
        link_id = self.data.get('link_id')
        response = requests.get(f'{BELVO_BASE_URL}/transactions/?account={account_id}&link={link_id}', headers=self._headers)
        return HTTPStatus.OK, response.json()

    @property
    def _headers(self):
        return {
            'Authorization': f'Basic {self._token}'
        }

    @property
    def _token(self):
        return base64.b64encode(f'{BELVO_SECRET_ID}:{BELVO_SECRET_KEY}'.encode('utf-8')).decode('utf-8')
