class PaymentResult:
    def __init__(self, is_success: bool, error_message: str = '', error_code: str = ''):
        """
        
        :param is_success:
        :param error_message: The message of the error
        :param error_code: The code of the error
        """
        self.is_success = is_success
        self.error_message = error_message
        self.error_code = error_code
