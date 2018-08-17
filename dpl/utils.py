import sys
import os
import logging


logging.basicConfig(
    level=logging.DEBUG, stream=sys.stderr,
    format=(
        '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | '
        'line %(lineno)d | %(message)s')
)


def get_logger(name):
    return logging.getLogger(name)


def create_output_dir(output_file_name):
    out_dir = os.path.dirname(output_file_name)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
