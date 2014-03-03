#  Copyright (C) 2014  Instituto Nokia de Tecnologia - INdT
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
import re
from binascii import crc_hqx
import struct
from construct import *

Target_00 = Struct("Target_00",
    Const(UBInt8("setup_format"), 3),
    Const(UBInt8("unknown"), 2),
    UBInt16("dll_version"),
    Terminator,
)

def parse_setup(report_file):
    setup_data = None
    crc = 0xffff
    version = None
    for line in report_file.readlines():
        m = re.match("Generated with uBlue setup DLL version: 1.0.0.(\d+)$",
                line.strip())
        if m:
            version = int(m.group(1))

        if line.strip() == "[Setup Data]":
            setup_data = {}
        if not line.strip() or setup_data is None:
            continue
        if not re.match("^[0-9A-F-]+$", line.strip()):
            continue

        data = line.strip().split("-")
        assert int(data[0], 16) == len(data[1:])
        # Opcode: Setup (0x06)
        assert data[1] == '06'
        target = int(data[2], 16)
        if not setup_data.get(target):
            setup_data[target] = ""
        # Offset into target
        assert int(data[3], 16) == len(setup_data[target].decode("hex"))
        setup_data[target] += "".join(data[4:])

        if target == 0xf0:
            # Remove existing CRC when calculating new CRC
            data = data[:-2]
        crc = crc_hqx("".join(data).decode("hex"), crc)

    # Check CRC
    expected_crc = struct.unpack(">H",
            "".join(setup_data[0xf0].decode("hex")[-2:]))[0]
    assert crc == expected_crc

    return (version, setup_data)
