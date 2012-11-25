from journoid import text

def contains(source_value, reference_value, **kw):
    source_value_norm = text.normalize_plain(source_value)
    reference_value_norm = text.normalize_plain(reference_value)
    return reference_value_norm in source_value_norm

COMPARATORS = {
    'contains': contains
    }

