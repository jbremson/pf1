import argparse
from pprint import pprint
from typing import List
# Email Parser

def single_line_parser(line: str) -> List:
    """Return a two element list if the input of the line is
        <key>: <value>

        Returns a single element list if the input of the line is
        <key>:
        """
    if line and line[0] in ["(","-","_"," "]:
        return []
    o = line.split(":", 1)
    if len(o) == 2 and o[1] == '':
        return [o[0]]
    return o


def next_line_idx(i: int, lines: List) -> int:
    """Return the index of the next non-empty line."""
    i += 1
    while not lines[i] and i < len(lines):
        i += 1
    return i

def is_pair(l: List) -> bool:
    return len(l) == 2

def is_single(l: List) -> bool:
    return len(l) == 1 and l[0] != ''



def email_parser(body: str)-> dict:
    lines = body.splitlines()
    out = dict()
    i = 0
    while i < len(lines):
        slp = single_line_parser(lines[i])
        if is_pair(slp):
            out[slp[0]] = slp[1]
        elif is_single(slp):
            i = next_line_idx(i, lines)
            line = lines[i]
            parsed_line = single_line_parser(line)
            if is_single(parsed_line):
                out[slp[0]] = parsed_line[0]
            elif is_pair(parsed_line):
                out[slp[0]] = "SOMETHING"

        i += 1
    return out



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help='Path to the file to parse.')
    args = parser.parse_args()
    with open(args.filepath) as fh:
        body = fh.read()
    pprint(email_parser(body))



