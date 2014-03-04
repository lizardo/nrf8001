nRF8001 Experiments
===================

Tools and documentation related to my nRF8001 experiments:

* diff\_setup\_data.py: Compare nRF8001 setup data from two nRFgoStudio report files.
* parse\_setup\_data.py: Extract setup data from a nRFgoStudio report and dump it
  in human readable format.
* target\_format.py: a parser/build grammar for setup data using Construct.
* tests/: automated test scripts. Currently, contains "conformity" tests for
  nRFgoStudio UI.

Note that these tools are at an early stage at the moment, and there are
various unknown/unsupported fields. If you find issues running any of them (as
you sure will), please file an issue in
https://github.com/lizardo/nrf8001/issues and attach the
ublue\_setup.gen.out.txt file that reproduces it, along with the XML file for
nRFgoStudio, so I can fix it.
