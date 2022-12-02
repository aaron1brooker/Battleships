import logging


class UserError(Exception):
    """Raised when anything unwanted/incorrect is inputed by the user"""

    def __init__(self, message: str):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)

        logging.error(message)
        self.message = message
