from onedep_deposition.exceptions import InvalidDepositSiteException
from functools import wraps

def handle_invalid_deposit_site(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except InvalidDepositSiteException as e:
            if self._redirect:
                if hasattr(self, '_connect'):
                    self._connect(e.site)
                    return func(self, *args, **kwargs)
                else:
                    raise e
            else:
                raise e

    return wrapper
