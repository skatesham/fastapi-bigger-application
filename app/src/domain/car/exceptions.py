from app.resources.string_formatters import format_car_not_found, format_car_already_exists


class CarNotFoundError(Exception):
    """Raised when a car is not found"""
    
    def __init__(self, car_id: int):
        self.car_id = car_id
        super().__init__(format_car_not_found(car_id))


class CarAlreadyExistsError(Exception):
    """Raised when a car already exists"""
    
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(format_car_already_exists(field, value))
