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

# FlagsContainer and FlagsAdapter are copied from Construct, and a one-line fix
# is applied to FlagsContainer as shown below.

class FlagsContainer(Container):
    def __pretty_str__(self, nesting = 1, indentation = "    "):
        attrs = []
        ind = indentation * nesting
        for k in self.keys():
            # This gives KeyError, so use getattr() instead
            #v = self.__dict__[k]
            v = getattr(self, k)
            if not k.startswith("_") and v:
                attrs.append(ind + k)
        if not attrs:
            return "%s()" % (self.__class__.__name__,)
        attrs.insert(0, self.__class__.__name__+ ":")
        return "\n".join(attrs)

class FlagsAdapter(Adapter):
    __slots__ = ["flags"]
    def __init__(self, subcon, flags):
        Adapter.__init__(self, subcon)
        self.flags = flags
    def _encode(self, obj, context):
        flags = 0
        for name, value in self.flags.items():
            if getattr(obj, name, False):
                flags |= value
        return flags
    def _decode(self, obj, context):
        obj2 = FlagsContainer()
        for name, value in self.flags.items():
            setattr(obj2, name, bool(obj & value))
        return obj2

def CheckBox(subcon):
    return Enum(subcon,
        Disabled = 0,
        Enabled = 1,
    )

def AdvBitmap(name):
    return FlagsAdapter(UBInt16(name),
        {
            "Custom AD": 1 << 14,
            "Service solicitation (GATT client)": 1 << 10,
            "Slave connection interval range": 1 << 8,
            "TX power level": 1 << 6,
            "Local name - use shortened": 1 << 5,
            "Local name - use complete": 1 << 4,
            "Local services": 1 << 0,
        },
    )

def AdvCustom(name):
    return FlagsAdapter(UBInt8(name),
        {
            "Enable custom AD #1": 1,
            "Enable custom AD #2": 2,
        },
    )

Target_00 = Struct("Target_00",
    Const(UBInt8("Setup format"), 3),
    Const(UBInt8("Unknown"), 2),
    UBInt16("DLL version"),
    Terminator,
)

Target_10 = Struct("Target_10",
    Const(Field("Unknown @ 0x00", 4), "\x00" * 4),
    SymmetricMapping(UBInt8("Device security"),
        {
            "No security required": 0,
               "Security required": 2,
        },
    ),
    # FIXME: Number of remote services?
    Const(UBInt8("Unknown @ 0x05"), 0),
    CheckBox(UBInt8("Writeable device name (over the air)")),
    Const(UBInt8("Unknown @ 0x07"), 0),
    CheckBox(UBInt8("Writeable device name (from app controller)")),
    SymmetricMapping(UBInt8("32 kHz clock source"),
        {
                   "External crystal": 0,
             "Internal RC oscillator": 1,
             "External analog source": 3,
            "External digital source": 4,
        },
    ),
    SymmetricMapping(UBInt8("32 kHz clock accuracy"),
        {
                 "250-500 PPM": 0,
                 "150-250 PPM": 1,
                 "100-150 PPM": 2,
                  "75-100 PPM": 3,
                   "50-75 PPM": 4,
                   "30-50 PPM": 5,
                   "20-30 PPM": 6,
            "Less than 20 PPM": 7,
        },
    ),
    Enum(UBInt8("16 MHz clock source"),
        Crystal = 0,
        Digital = 1,
    ),
    EmbeddedBitStruct(
        BitField("Time before start", 6),
        Enum(BitField("Active signal", 2),
            Disable = 0,
            Active_high = 1,
            Active_low = 2,
        ),
    ),
    EmbeddedBitStruct(
        SymmetricMapping(BitField("Initial TX power", 7),
            {
                "-18 dBm": 0,
                "-12 dBm": 1,
                 "-6 dBm": 2,
                  "0 dBm": 3,
            },
        ),
        Flag("DC/DC converter"),
    ),
    SBInt8("External antenna gain"),
    UBInt8("Bytes in shortened name"),
    # FIXME: 0xC1 if Gapsettings/ServiceToAdvertise is not empty; 0x00 otherwise
    Const(UBInt8("Unknown @ 0x10"), 0),
    # FIXME: Gapsettings/ServiceToAdvertise (array of 16-bit Service UUIDs)
    Const(Field("Unknown @ 0x11", 13), "\x00" * 13),
    # FIXME: 0x01 if Gapsettings/SercieToSolicitate is not empty; 0x00 otherwise
    Const(UBInt8("Unknown @ 0x1E"), 0),
    # FIXME: Gapsettings/SercieToSolicitate (array of 16-bit Service UUIDs)
    Const(Field("Unknown @ 0x1F", 15), "\x00" * 15),
    AdvBitmap("ACI Bond Advertising"),
    Const(Field("Unknown @ 0x30", 2), "\x00" * 2),
    AdvBitmap("ACI Connect Advertising"),
    EmbeddedBitStruct(
        SymmetricMapping(Nibble("Required level of security"),
            {
                "Unauthenticated (Just Works)": 0,
                     "Authenticated (Passkey)": 1,
            },
        ),
        SymmetricMapping(Nibble("I/O capabilities"),
            {
                        "Display only": 0,
                      "Display yes/no": 1,
                       "Keyboard only": 2,
                                "None": 3,
                "Keyboard and display": 4,
            },
        ),
    ),
    EmbeddedBitStruct(
        ExprAdapter(Nibble("Maximum encryption key size"),
            encoder = lambda obj, ctx: obj - 7,
            decoder = lambda obj, ctx: obj + 7,
        ),
        ExprAdapter(Nibble("Mininum encryption key size"),
            encoder = lambda obj, ctx: obj - 7,
            decoder = lambda obj, ctx: obj + 7,
        ),
    ),
    Const(UBInt8("Unknown @ 0x36"), 0),
    Enum(UBInt16("Dynamic window limiting"),
        On = 0x0264,
        Off = 0xffff,
    ),
    Const(UBInt8("Unknown @ 0x39"), 0xFF),
    UBInt16("Bond timeout (seconds)"),
    UBInt8("Security request delay (seconds)"),
    Const(Field("Unknown @ 0x3D", 3), "\x05\x00\x00"),
    AdvBitmap("ACI Bond Scan Response"),
    Const(Field("Unknown @ 0x42", 2), "\x00" * 2),
    AdvBitmap("ACI Connect Scan Response"),
    Const(Field("Unknown @ 0x46", 2), "\x00" * 2),
    AdvBitmap("ACI Broadcast Advertising"),
    Const(Field("Unknown @ 0x4A", 2), "\x00" * 2),
    AdvBitmap("ACI Broadcast Scan Response"),
    AdvCustom("ACI Bond Advertising custom ADs"),
    AdvCustom("ACI Bond Scan Response custom ADs"),
    AdvCustom("ACI Connect Advertising custom ADs"),
    AdvCustom("ACI Connect Scan Response custom ADs"),
    AdvCustom("ACI Broadcast Advertising custom ADs"),
    AdvCustom("ACI Broadcast Scan Response custom ADs"),
    # FIXME: this field is set when Security is required, but not what it means
    # individually. Maybe Whitelist?
    IfThenElse("Unknown @ 0x54", lambda ctx: ctx["Device security"] ==
            "Security required",
        Const(UBInt8("Unknown @ 0x54"), 1),
        Const(UBInt8("Unknown @ 0x54"), 0),
    ),
    FlagsAdapter(UBInt8("Available custom ADs"),
        {
            "Custom AD #1 is present": 1,
            "Custom AD #2 is present": 2,
        },
    ),
    Terminator,
)

def UUID(name):
    return SymmetricMapping(UBInt16(name),
        {
                                 "Device Name": 0x2A00,
                                  "Appearance": 0x2A01,
            "Peripheral Preferred Connection Parameters": 0x2A04,
            "GATT primary service declaration": 0x2800,
            "GATT characteristic declaration": 0x2803,
        },
    )

def Attribute(name):
    return Struct(name,
        # FIXME: most likely there are bits for write and read permissions
        UBInt8("Permissions #1"),
        UBInt8("Permissions #2"),
        # FIXME: It is not clear yet why there are two different length fields,
        # but the field is selected based on the fields above.
        UBInt8("Length #1"),
        UBInt8("Length #2"),
        UBInt16("Handle"),
        UUID("Type"),
        Const(UBInt8("Unknown"), 1),
        # FIXME: It is still not clear how the value length is calculted.
        IfThenElse("Value", lambda ctx: ctx["Permissions #1"] == 0x06,
            Field("Value", lambda ctx: ctx["Length #2"]),
            Field("Value", lambda ctx: ctx["Length #1"]),
        ),
    )

Target_20 = Struct("Target_20",
    Attribute("GAP service"),
    Attribute("GAP Device Name characteristic"),
    Attribute("GAP Device Name characteristic value"),
    Attribute("GAP Appearance characteristic"),
    Attribute("GAP Appearance characteristic value"),
    Attribute("GAP PPCP characteristic"),
    Attribute("GAP PPCP characteristic value"),
    Attribute("GATT service"),
    Const(UBInt8("Unknown"), 0),
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
        assert data[1] == "06"
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
