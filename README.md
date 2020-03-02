##Email Parsing Program

-Joel Bremson
 March 1, 2020

#Usage:

This should work with any recent version of Python3. It works for sure
with python 3.8.

```python ./email_parser.py <path_to_file>```

#Setup

In order to handle parsing without extensive inferences a couple of definitions
are required in setup in the PARSE_TRIGGER dict.

The parser will seek parse keys that are a string of text at the
start of a line followed by a colon. The identifying string need not be
complete, just long enough to disambiguate from other text.

Attached to each of the PARSE_TRIGGER string keys is a descriptive
that tells the parser what to expect.

    ParseTypes.SINGLE ->    Expect a key value pair of either a colon separated
                            pair on a single line, i.e. <k>:<v> OR a single key
                            value followed by one or more new lines and a single
                            line of text.

    ParseTypes.MULTI ->     Expect a single key with colon and new line followed by
                            any number of blank lines followed by simple <k>:<v>
                            pairs. Terminated by a new line.

Example:

```
PARSE_TRIGGERS = {'subject': ParseTypes.SINGLE,
                  'body': ParseTypes.SINGLE,
                  'customer': ParseTypes.SINGLE,
                  'pw reference number': ParseTypes.SINGLE,
                  'maintenance window': ParseTypes.MULTI,
                  'location of work': ParseTypes.SINGLE,
                  'affected service(s)': ParseTypes.MULTI,
                  'e-mail': ParseTypes.SINGLE,
                  'phone': ParseTypes.SINGLE}
```

# Design notes

This system could be expanded by replacing the ParseTypes enum with
objects designed to parse the various data types.

Ordinarily I would write tests. I didn't do that due to lack of time
but the main parsing code is easily available for testing.

If I were to refactor this code I would break up the ParseType branching
into their own routines.
