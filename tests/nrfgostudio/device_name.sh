#!/bin/bash
set -e -u

. common/tap.sh 2

run_test 1 no_name "Empty Device Name"
run_test 2 one_char "One character Device Name"
