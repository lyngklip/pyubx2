'''
Created on 3 Oct 2020

Static method tests for pyubx2.UBXMessage

@author: semuadmin
'''

import unittest

from pyubx2 import UBXMessage, UBX_CLASSES
import pyubx2.ubxtypes_core as ubt
from pyubx2.ubxhelpers import itow2utc, gpsfix2str, dop2str, gnss2str, key_from_val


class StaticTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testVal2Bytes(self):  # test conversion of value to bytes
        INPUTS = [(2345, ubt.U2), (-2346789, ubt.I4), (b'\x44\x55', ubt.X2), (23.12345678, ubt.R4), (-23.12345678912345, ubt.R8)]
        EXPECTED_RESULTS = [b'\x29\x09', b'\xdb\x30\xdc\xff', b'\x44\x55', b'\xd7\xfc\xb8\x41', b'\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0']
        for i, inp in enumerate(INPUTS):
            (val, att) = inp
            res = UBXMessage.val2bytes(val, att)
            self.assertEqual(res, EXPECTED_RESULTS[i])

    def testBytes2Val(self):  # test conversion of bytes to value
        INPUTS = [(b'\x29\x09', ubt.U2), (b'\xdb\x30\xdc\xff', ubt.I4), (b'\x44\x55', ubt.X2), (b'\xd7\xfc\xb8\x41', ubt.R4), (b'\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0', ubt.R8)]
        EXPECTED_RESULTS = [2345, -2346789, b'\x44\x55', 23.12345678, -23.12345678912345]
        for i, inp in enumerate(INPUTS):
            (valb, att) = inp
            res = UBXMessage.bytes2val(valb, att)
            if att == ubt.R4:
                self.assertAlmostEqual(res, EXPECTED_RESULTS[i], 6)
            elif att == ubt.R8:
                self.assertAlmostEqual(res, EXPECTED_RESULTS[i], 14)
            else:
                self.assertEqual(res, EXPECTED_RESULTS[i])

    def testUBX2Bytes(self):
        res = UBXMessage.msgstr2bytes('CFG', 'CFG-MSG')
        self.assertEqual(res, (b'\x06', b'\x01'))

    def testKeyfromVal(self):
        res = key_from_val(UBX_CLASSES, 'MON')
        self.assertEqual(res, (b'\x0A'))

    def testCalcChecksum(self):
        res = UBXMessage.calc_checksum(b'\x06\x01\x02\x00\xf0\x05')
        self.assertEqual(res, b'\xfe\x16')

    def testGoodChecksum(self):
        res = UBXMessage.isvalid_checksum(b'\xb5b\x06\x01\x02\x00\xf0\x05\xfe\x16')
        self.assertTrue(res)

    def testBadChecksum(self):
        res = UBXMessage.isvalid_checksum(b'\xb5b\x06\x01\x02\x00\xf0\x05\xfe\x15')
        self.assertFalse(res)

    def testitow2utc(self):
        res = str(itow2utc(387092000))
        self.assertEqual(res, '11:31:16')

    def testgnss2str(self):
        GNSS = {0: 'GPS', 1: 'SBAS', 2: 'Galileo', 3: 'BeiDou',
                4: 'IMES', 5: 'QZSS', 6: 'GLONASS', 7: "7"}
        for i in range (0, 8):
            res = gnss2str(i)
            self.assertEqual(res, GNSS[i])

    def testgps2str(self):
        fixs = ['NO FIX', 'DR', '2D', '3D', 'GPS + DR', 'TIME ONLY']
        for i, fix in enumerate(range (0, 6)):
            res = gpsfix2str(fix)
            self.assertEqual(res, fixs[i])

    def testdop2str(self):
        dops = ['Ideal', 'Excellent', 'Good', 'Moderate', 'Fair', 'Poor']
        i = 0
        for dop in (1, 2, 5, 10, 20, 30):
            res = dop2str(dop)
            self.assertEqual(res, dops[i])
            i += 1

    def testcfgname2key(self):
        (key, typ) = UBXMessage.cfgname2key("CFG_NMEA_PROTVER")
        self.assertEqual(key, 0x20930001)
        self.assertEqual(typ, ubt.E1)
        (key, typ) = UBXMessage.cfgname2key("CFG_UART1_BAUDRATE")
        self.assertEqual(key, 0x40520001)
        self.assertEqual(typ, ubt.U4)

    def testcfgkey2type(self):
        (key, typ) = UBXMessage.cfgkey2name(0x20510001)
        self.assertEqual(key, "CFG_I2C_ADDRESS")
        self.assertEqual(typ, ubt.U1)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
