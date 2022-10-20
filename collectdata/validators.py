from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize= value.size
    if filesize > 100000000:
        raise ValidationError("The maximum file size that can be uploaded is 100MB")
    else:
        return value


def validate_file_extention(value):
    file_extention = str(value).split('.')[-1]
    if file_extention != 'csv' and file_extention != 'tsv':
        raise ValidationError("file extention must be in the format ('csv' or 'tsv')")
    else:
        return value