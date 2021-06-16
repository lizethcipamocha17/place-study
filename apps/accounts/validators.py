from django.core.exceptions import ValidationError


def validate_photo_weight(photo):
    print("PHOTO", photo.size)
    if photo.size > (512 * 1024):
        raise ValidationError(
            f"La imagen es demasiado grande, el peso máximo permitido es de 512KB y el tamaño enviado es de {round(photo.size / 1024)}KB")

