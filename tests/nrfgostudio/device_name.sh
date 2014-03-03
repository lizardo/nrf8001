#!/bin/bash
set -e -u

. common/tap.sh 1

run_test 1 no_name "Empty Device Name"
