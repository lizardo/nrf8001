nRF8001 Experiments
===================

Tools and documentation related to my nRF8001 experiments:

* `diff_setup_data.py`: Compare nRF8001 setup data from two nRFgoStudio report
  files.
* `parse_setup_data.py`: Extract setup data from a nRFgoStudio report and dump
  it in human readable format.
* `target_format.py`: a parser/build grammar for setup data using Construct.
* `tests/`: automated test scripts. Currently, contains "conformity" tests for
  nRFgoStudio UI.

Note that these tools are at an early stage at the moment, and there are
various unknown/unsupported fields. If you find issues running any of them (as
you sure will), please file an issue in
https://github.com/lizardo/nrf8001/issues and attach the
`ublue_setup.gen.out.txt` file that reproduces it, along with the XML file for
nRFgoStudio, so I can fix it.

Usage
=====

For help using the tools, run `./tool.py --help` on Linux (on other systems,
try running `python tool.py --help` instead).

Some example usage scenarios:

    $ ./diff_setup_data.py \
        tests/nrfgostudio/default/default/ublue_setup.gen.out.txt \
        tests/nrfgostudio/device_name/no_name/ublue_setup.gen.out.txt
    ...
    $ ./parse_setup_data.py \
        tests/nrfgostudio/default/default/ublue_setup.gen.out.txt
    ...

You can also use the `target_format.py` module directly to write your own tool
that parses setup messages. See `parse_setup_data.py` source code for API usage
example.

License
=======

All code is released under the terms of the GNU GPL v2. See LICENSE file for
details.
