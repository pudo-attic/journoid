from urllib2 import urlopen
from pprint import pprint
import hashlib
from messytables import CSVTableSet, type_guess, \
  types_processor, headers_guess, headers_processor, \
  offset_processor

from journoid.comparators import COMPARATORS
from journoid.notify import notify

# Terminology:
#
# * source - a dataset that is being processed
# * reference - a dataset that is used for matching
#
#

def load_data(config):
    if not 'url' in config:
        yield {
            config.get('field'): config.get('value')
            }
        return
    fh = urlopen(config.get('url'))
    table_set = CSVTableSet.from_fileobj(fh)
    row_set = table_set.tables[0]

    offset, headers = headers_guess(row_set.sample)
    row_set.register_processor(headers_processor(headers))
    row_set.register_processor(offset_processor(offset + 1))

    for row in row_set:
        row = [(c.column, c.value) for c in row]
        yield dict(row)

    fh.close()

def format_record(title, record):
    message = u"####### %s ########\n\n" % title
    for k, v in record.items():
        if len(v.strip()):
            #message += u" %s: %s\n" % (k.encode('utf-8'), v.encode('utf-8'))
            message += u" [%s]: %s\n" % (k, v)
    message += "\n\n"
    return message

def send_message(task, config, source, source_value, reference):
    subject = "[Journoid] %s matches %s" % (task.get('name'), source_value)
    print [subject]
    message = u"Your subscription to '%s' has detected the following match:\n\n" % task.get('name')
    message += format_record("Filter Entry", reference)
    message += format_record("Matching Record", source)

    notify(config, task.get('notify'), subject, message.encode('utf-8'))

def make_event_signature(task, index, source, reference):
    sig = (task.get('name'), index, source.items(), reference.items())
    sig = hashlib.sha1(repr(sig)).hexdigest()
    return sig

def match(comparator, source, reference, source_config,
          reference_config):
    source_field = source_config.get('field')
    source_value = source.get(source_field)
    reference_value = reference.get(reference_config.get('field'))
    return source_value, comparator(source_value, reference_value)


def process_task(task, config):
    source_config = task.get('source')
    reference_config = task.get('reference')
    references = load_data(reference_config)
    references = list(references)

    comparator = task.get('comparator', 'contains')
    comparator = COMPARATORS.get(comparator)

    for i, source in enumerate(load_data(source_config)):
        for reference in references:
            source_value, result = match(comparator, source, reference,
                           source_config, reference_config)
            if result:
                signature = make_event_signature(task, i, source, reference)
                print signature
                send_message(task, config, source, source_value, reference)


def process_tasks(config):
    for task in config.get('tasks', []):
        process_task(task, config)

