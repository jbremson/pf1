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
                  'affected service(s)': ParseTypes.MULTI,
                  'e-mail': ParseTypes.SINGLE,
                  'phone': ParseTypes.SINGLE}


def single_line_parser(line: str) -> List:
    """Return a two element list if the input of the line is
        <key>: <value>

        Returns a single element list if the input of the line is
        <key>:
        """
    if line and line[0] in ["(", "-", "_", " "]:
        return []
    o = line.split(":", 1)
    if len(o) == 2 and o[1] == '':
        return [o[0]]
    return o


def is_pair(l: List) -> bool:
    return len(l) == 2


def is_single(l: List) -> bool:
    return len(l) == 1 and l[0] != ''

out = dict()

def email_parser(body: str) -> dict:
    lines = body.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        trigger = re.match(r'^([^:]+):', line.lower())
        if trigger:
            trg = trigger[1]
            for k in PARSE_TRIGGERS.keys():
                if trg.startswith(k):
                    trg = k # Handles abreviated keys
                    if PARSE_TRIGGERS[trg] is ParseTypes.SINGLE:
                        # Format is <key>:<value>
                        # or
                        # <key>:
                        # <blank_line>[0,1]
                        # <value> - Assuming only a single line for now.
                        slp = single_line_parser(line)
                        if is_pair(slp):
                            # <k>:<v>
                            out[trg] = slp[1]
                        elif is_single(slp):
                            # <k>: \n\n?<v>\n
                            i += 1
                            while not lines[i]:
                                i += 1
                            out[trg] = lines[i]
                    if PARSE_TRIGGERS[trg] is ParseTypes.MULTI:
                        # Assume sub values are either
                        # single line <k>:<v>
                        # or a comment
                        # The multi-block ends with a new line
                        out[trg] = dict()
                        i += 1
                        while not lines[i]:
                            i += 1  # advance to data
                        while lines[i]:
                            slp = single_line_parser(lines[i])
                            if is_pair(slp):
                                out[trg][slp[0]] = slp[1]
                            i += 1
        i += 1
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help='Path to the file to parse.')
    args = parser.parse_args()
    with open(args.filepath) as fh:
        body = fh.read()
    pprint(email_parser(body))
