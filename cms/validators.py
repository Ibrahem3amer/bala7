from django.core.exceptions import ValidationError
from urllib.parse import urlparse
import datetime

class MaterialValidator(object):
    """Validator for common fields of material model"""

    @classmethod
    def validate_material_link(cls, url):
        """
        Validates material's link that it presents a vaild, pdf file not a broken url.
        1   -> All is good.
        0   -> Provided url is either not valid or broken.
        -1  -> Provided url should lead to pdf or doc file.
        """
        url_parsing = urlparse(url)
        allowed     = ['docs.google', 'onedrive.live', 'pdf']
        
        # Check that url is valid url, and that url leads to allowed form of urls.
        if url_parsing.scheme and url_parsing.netloc:
            if not any( match in url for match in allowed):
                return -1
        else:
            return 0

        return 1

    
    @classmethod
    def validate_date(cls, date):
        """
        Accepts material date and assure that date is not at future.
        1   -> All is good.
        0   -> Year is in future
        """    
        now = datetime.datetime.now()
        if int(now.year) - int(date.year) < 0:
            return 0
        return 1
 



