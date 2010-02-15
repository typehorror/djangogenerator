import re 
import unicodedata

def slugify(value):
    """
    Normalizes string, removes non-alpha characters,
    and converts spaces to _.
    """
    slug = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    slug = unicode(re.sub('[^\w\s-]', '', slug).strip())
    # remove name starting with number
    slug = re.sub('^\d+', '', slug)
    return re.sub('[-\s]+', '_', slug)
