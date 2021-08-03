class InputParameterVerificationError(Exception):
    def __init__(self, message: str):
        """Конструктор."""
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        """Вывод ошибки."""
        return f'Ошибка: {self.message}'


class ResultVerificationError(Exception):
    """Ошибка ResultVerificationError срабатывает при не валидном
     результе."""

    def __init__(self, message: str):
        """Конструктор."""
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        """Вывод ошибки."""
        return f'Ошибка: {self.message}'


class ParamVerificationIsZero(Exception):
    """Ошибка своя."""

    def __init__(self, message: str):
        """Конструктор."""
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        """Вывод ошибки."""
        return f'Ошибка: {self.message}'
