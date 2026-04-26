# Created 2026-04-25

import sys

usage = ''

def set_usage(s: str):
    global usage
    usage = s

def assert_noerror(cond: bool, why: str, extra: str) -> None:
    if not cond:
        print('Assertion failed:', why)
        print(extra)
        sys.exit(1)

def assert_usage(cond: bool, why: str = ""):
    assert_noerror(
        cond,
        'improper usage' + (f' because {why}' if why else ''),
        usage
    )

def unpack_typed(array, *types) -> list:
    typeds = []

    for i in range(len(array)):
        if types[i] == None:
            typed = array[i]
        else:
            typed = types[i](array[i])
        typeds.append(typed)

    return typeds
