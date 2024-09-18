from http import HTTPStatus

from controllers import AVAILABLE_CONTROLLERS


def main(args: dict, context: object) -> dict:
    # Argumentos
    controller = args.get('controller')
    action = args.get('action')
    debug = args.get('debug', False)
    # Seguridad
    jwt = args.get('http', {}).get('headers', {}).get('authorization', '').replace('JWT ', '')
    # Data a trabajar
    institution = args.get('institution')
    account_id = args.get('account_id')
    data = args.get('data', {})
    data['jwt'] = jwt
    data['institution'] = institution
    data['account_id'] = account_id
    data['debug'] = debug

    response = {
        'body': {
            'error': 'invalid_controller'
        },
        'statusCode': HTTPStatus.BAD_REQUEST
    }

    if controller not in AVAILABLE_CONTROLLERS:
        return response

    Controller = AVAILABLE_CONTROLLERS[controller]
    controller = Controller(action=action, data=data)

    status, result = controller.execute()

    response['statusCode'] = status
    response['body'] = result

    return response
