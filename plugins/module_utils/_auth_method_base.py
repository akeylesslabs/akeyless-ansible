

class AkeylessAuthMethodBase:
    """Base class for individual auth method implementations"""

    def __init__(self, options):
        self.options = options

    def validate(self):
        self.validate_required_options(['access_id'])

    def authenticate(self, api):
        raise NotImplementedError('authenticate must be implemented')

    def validate_required_options(self, required_options):
        for option in required_options:
            if self.options.get(option) is None:
                raise ValueError(f"{option} is required for the {self.__class__.__name__} auth method")