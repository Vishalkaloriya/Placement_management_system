from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from pathlib import Path
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from os import path

class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types.
        Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file
        size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop("max_upload_size")
        self.content_types = kwargs.pop("content_types")
        
        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under'
                                                '%s. Current filesize %s')
                                                % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass
        return data
    

@deconstructible
class FileExtensionValidator:
    extension_message = _(
        "File extension “%(extension)s” is not allowed. "
        "Allowed extensions are: %(allowed_extensions)s."
    )
    
    size_message = (
        "File size “%(size)s” is not allowed. "
        "Allowed size is upto: %(allowed_size)s."
    )
    extension_code = "invalid_extension"
    size_code = "invalid_filesize"

    def __init__(self, allowed_extensions=None, max_file_size=None, extension_message=None, size_message=None):
        if allowed_extensions is not None:
            allowed_extensions = [
                allowed_extension.lower() for allowed_extension in allowed_extensions
            ]
        if max_file_size is not None:
            max_file_size = 2621440
            
        self.allowed_extensions = allowed_extensions
        self.max_file_size = max_file_size
        
        if extension_message is not None:
            self.extension_message = extension_message
        if size_message is not None:
            self.size_message = size_message

    def __call__(self, value):
        extension = Path(value.name).suffix[1:].lower()
        if (
            self.allowed_extensions is not None
            and extension not in self.allowed_extensions
        ):
            
            raise ValidationError(
                self.extension_message,
                code=self.extension_code,
                params={
                    "extension": extension,
                    "allowed_extensions": ", ".join(self.allowed_extensions),
                    "value": value,
                },
            )
        
        size = value.size
        if (
            self.max_file_size is not None
            and size > self.max_file_size
        ):
            raise ValidationError(
                self.size_message,
                code=self.size_code,
                params={
                    "size": size,
                    "allowed_size": self.max_file_size,
                    "value": value,
                },
            )

