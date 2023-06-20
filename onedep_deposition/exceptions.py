class DepositApiException(Exception):
    def __init__(self, message, status_code=0):
        super().__init__(message)
        self.status_code = status_code

class InvalidDepositSiteException(Exception):
    def __init__(self, site: str):
        super().__init__(f"Invalid deposit site")
        self.site = site
