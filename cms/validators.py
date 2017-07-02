from django.core.exceptions import ValidationError
from urllib.parse import urlparse

class MaterialValidator(object):
    """Validator for common fields of material model"""

    @classmethod
    def validate_material_link(cls, url):
        """
        Validates material's link that it presents a vaild, pdf file not a broken url.
        """
        url_parsing = urlparse(url)
        if url_parsing.scheme and url_parsing.netloc:
            if not 'docs.google' or 'onedrive.live' or 'pdf' in url:
                raise ValidationError('Provided url should lead to pdf or doc file.')    
        else:
            raise ValidationError('Provided url is either not valid or broken.')

        