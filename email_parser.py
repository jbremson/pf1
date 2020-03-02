import argparse
from typing import List
# Email Parser

def single_line_parser(line: str) -> List:
    return line.split(":", 1)

def is_multiline(parsed_line: List) -> bool:
    return len(parsed_line[0]) > 0 and not parsed_line[1]


def email_parser(body: str)-> dict:
    out = {}
    lines = body.splitlines()
    i = 0
    label = ''
    val = ''
    while i < len(lines):
        print(lines[i])
        if ":" not in lines[i]:
            pass
        else:
            slp = single_line_parser(lines[i])
            if len(slp) == 2 and slp[1]:
                out[slp[0]] = slp[1]
            elif is_multiline(slp):
                subsection = ""
                while len(lines[i]) > 1:
                    subsection += lines[i]
                    i += 1
                sub_keys = email_parser(subsection)
                if len(sub_keys) == 1:
                    # This is a single line key value pair
                    # that is split.
                    out[slp[0]] = sub_keys[slp[0]]
                else:
                    out[slp[0]] = sub_keys
        i += 1

    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help='Path to the file to parse.')
    args = parser.parse_args()
    with open(args.filepath) as fh:
        body = fh.read()
    print(email_parser(body))



