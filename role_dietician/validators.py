from django.core.exceptions import ValidationError

def validate_nutrition_limit(value):
    """check limits of macros"""
    if value < 0:
        raise ValidationError(
            "Значення ліміту не може бути від'ємним. Будь ласка, введіть число 0 або більше."
        )
    if value > 10000:
        raise ValidationError(
            "Значення виглядає помилковим (занадто велике). Перевірте введені дані."
        )

def validate_feedback_text(value):
    """checks feedback"""

    clean_text = value.strip()

    if not clean_text:
        raise ValidationError(
            "Порада не може бути порожньою. Напишіть рекомендації для користувача."
        )

    if len(clean_text) < 10:
        raise ValidationError(
            "Порада занадто коротка. Напишіть принаймні 10 символів, щоб вона була корисною."
        )

    if len(clean_text) > 5000:
        raise ValidationError(
            f"Порада занадто довга ({len(clean_text)} симв.). Максимум — 5000 символів."
        )
    if clean_text.isdigit():
        raise ValidationError(
            "Порада не може складатися лише з цифр. Напишіть змістовний текст."
        )

