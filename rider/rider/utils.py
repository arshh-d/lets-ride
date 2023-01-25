
from django.core.exceptions import ValidationError
def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ValidationError as e:
            response = handle_exc(e)
        except Exception as e:
            response = handle_exc(e)

    return wrapper


def handle_exc(e):
    """
    Handle exceptions in views and create an appropriate response
    """
    response = {}
    msg = ""
    try:
        raise e
    except ValidationError:
        msg = "Validation error, not a valid UUID"
    except Exception:
        msg = "Exception raised"
    
    response['msg'] = msg
    return response