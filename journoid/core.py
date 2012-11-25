import argparse
import json
import os

from journoid.process import process_tasks

def main():
    parser = argparse.ArgumentParser(description='Run notifications on data.')
    parser.add_argument('config', metavar='CONFIG', type=unicode,
                        help='path of the configuration file')
    #parser.print_help()
    args = parser.parse_args()
    with open(args.config, 'rb') as fh:
        config = json.load(fh)
    config['_prefix'] = os.path.dirname(args.config)
    process_tasks(config)


if __name__ == '__main__':
    main()
