from datetime import date

class NutritionValidationError(Exception):
    """Custom exception for nutrition validation errors."""

class NutritionValidator:
    """Handles validation of nutrition input data."""

    REQUIRED_FIELDS = ["protein", "fat", "carbs", "fiber", "date", "meals_count"]

    @classmethod
    def validate(cls, data: dict) -> None:
        cls._check_required_fields(data)
        cls._check_numeric_values(data)
        cls._check_non_negative(data)
        cls._check_meals_count(data)
        cls._check_date(data)

    @classmethod
    def _check_required_fields(cls, data: dict) -> None:
        missing = [field for field in cls.REQUIRED_FIELDS if field not in data]
        if missing:
            raise NutritionValidationError(f"Missing required fields: {', '.join(missing)}")


    @staticmethod
    def _check_numeric_values(data: dict) -> None:
        for key, value in data.items():
            if not isinstance(value, (int, float)):
                raise NutritionValidationError(f"{key} must be a number.")


    @staticmethod
    def _check_non_negative(data: dict) -> None:
        for key, value in data.items():
            if value < 0:
                raise NutritionValidationError(f"{key} cannot be negative.")


    @staticmethod
    def _check_meals_count(data: dict) -> None:
        meals_count = data.get('meals_count')

        if not isinstance(meals_count, int):
            raise NutritionValidationError("meals_count must be an integer.")

        if meals_count < 1:
            raise NutritionValidationError("meals_count must be at least 1.")


    @staticmethod
    def _check_date(data: dict) -> None:
        entry_date = data.get("date")

        if not isinstance(entry_date, date):
            raise NutritionValidationError("data must be a valid date object.")

        if entry_date > date.today():
            raise NutritionValidationError("date cannot be in the future.")
