#!/usr/bin/env python
# Copyright (c) 2014  Instituto Nokia de Tecnologia (INdT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function
import argparse
from target_format import parse_setup

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare nRF8001 setup data " +
            "from two nRFgoStudio report files.")
    parser.add_argument("report", type=file, nargs=2,
            help="report generated by nRFgoStudio (ublue_setup.gen.out.txt)")
    args = parser.parse_args()

    version, data1 = parse_setup(args.report[0])
    version, data2 = parse_setup(args.report[1])

    print("File #1: " + args.report[0].name)
    print("File #2: " + args.report[1].name)
    print()

    only_in_first = set(data1) - set(data2)
    if only_in_first:
        print("Targets only in %s: %s" % (args.report[0].name,
            ", ".join("0x%02X" % i for i in only_in_first)))

    only_in_first = set(data2) - set(data1)
    if only_in_first:
        print("Targets only in %s: %s" % (args.report[1].name,
            ", ".join("0x%02X" % i for i in only_in_first)))

    for target in sorted(set(data1) & set(data2)):
        d1 = data1[target].decode("hex")
        d2 = data2[target].decode("hex")
        for (offset, byte) in enumerate(d1):
            if offset == len(d2):
                break
            if byte != d2[offset]:
                print("[0x%02X] Differ at 0x%02X: %02X -> %02X" % (target,
                    offset, ord(byte), ord(d2[offset])))
        if len(d1) > len(d2):
            print("[0x%02X] Bytes only in %s: %s" % (target,
                args.report[0].name, " ".join("%02X" % i for i in d1[offset:])))
        elif len(d1) < len(d2):
            print("[0x%02X] Bytes only in %s: %s" % (target,
                args.report[1].name, " ".join("%02X" % i for i in d2[offset + 1:])))

#    print("Setup Data:")
#    pprint(setup_data)
#
#    print("\nTarget 0x00:")
#    target = Target_00.parse(setup_data[0x00].decode("hex"))
#    print(target)
#    assert target["dll_version"] == version
