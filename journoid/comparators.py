import Levenshtein

from journoid import text

def contains(source_value, reference_value, **kw):
    source_value_norm = text.normalize_plain(source_value)
    reference_value_norm = text.normalize_plain(reference_value)
    return reference_value_norm in source_value_norm

def distance(source_value, reference_value, task=None, **kw):
    threshold = float(task.get('threshold', 0.2))
    source_value_norm = text.normalize_plain(source_value)
    reference_value_norm = text.normalize_plain(reference_value)
    length = max([len(source_value_norm), len(reference_value_norm)])
    max_distance = int(length * threshold) + 1
    #print [max_distance]
    return Levenshtein.distance(reference_value_norm, source_value_norm) \
            < max_distance


def opencorporates_status(source_value, reference_value, **kw):
    import requests
    print "OC CHECK", [source_value]
    res = requests.get('http://opencorporates.com/reconcile/gb',
            params={'query': source_value})
    if not len(res.json.get('result')):
        return False
    first = res.json.get('result')[0]
    if first.get('score') < 70:
        return False
    res = requests.get(first.get('uri')+'.json')
    company = res.json.get('company')
    return company.get('current_status').strip().lower() != 'active'

COMPARATORS = {
    'contains': contains,
    'distance': distance,
    'company_status': opencorporates_status
    }

