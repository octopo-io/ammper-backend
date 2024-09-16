from http import HTTPStatus

from controllers import AVAILABLE_CONTROLLERS


def main(args: dict, context: object) -> dict:
    controller = args.get('controller')
    action = args.get('action')
    jwt = args.get('http', {}).get('headers', {}).get('authorization', '').replace('JWT ', '')
    data = args.get('data', {})
    data['jwt'] = jwt

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
