class InputParameterVerificationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'Ошибка: {self.message}'


class ResultVerificationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'Ошибка: {self.message}'


class ParamVerificationIsZero(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'Ошибка: {self.message}'
