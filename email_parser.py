import argparse
from enum import Enum
from pprint import pprint
import re
from typing import List


# Email Parser

class ParseTypes(Enum):
    SINGLE = 1
    MULTI = 2


PARSE_TRIGGERS = {'subject': ParseTypes.SINGLE,
                  'body': ParseTypes.SINGLE,
                  'customer': ParseTypes.SINGLE,
                  'pw reference number': ParseTypes.SINGLE,
                  'maintenance window': ParseTypes.MULTI,
                  'location of work': ParseTypes.SINGLE,
                  'affected services': ParseTypes.MULTI,
                  'email': ParseTypes.SINGLE,
                  'phone': ParseTypes.SINGLE}

out = dict()

def email_parser(body: str) -> dict:
    lines = body.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        trigger = re.match(r'^([^:]+):', line.lower())
        if trigger and trigger[1] in PARSE_TRIGGERS.keys():
           if PARSE_TRIGGERS[trigger] is ParseTypes.SINGLE:
               # Format is <key>:<value>
               # or
               # <key>:
               # <blank_line>[0,1]
               # <value> - Assuming only a single line for now.



        i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help='Path to the file to parse.')
    args = parser.parse_args()
    with open(args.filepath) as fh:
        body = fh.read()
    pprint(email_parser(body))
