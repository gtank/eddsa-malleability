import unittest
import rfc8032 as ed

class CurveFunctions(unittest.TestCase):
    def testIsOnCurve(self):
        self.assertTrue(ed.is_on_curve((0,1,1,0)))
        self.assertFalse(ed.is_on_curve((1,0,1,0)))
        self.assertTrue(ed.is_on_curve(ed.G))
        self.assertTrue(ed.is_on_curve(ed.point_mul(5, ed.G)))

    def testSmallOrder(self):
        O = (0, 1, 1, 0) # identity point
        Q = ed.point_mul(8, O)
        self.assertTrue(ed.point_equal(O, Q))

        P = (38214883241950591754978413199355411911188925816896391856984770930832735035197, 0, 1, 0)
        Q = ed.point_mul(8, P)
        self.assertTrue(ed.point_equal(O, Q))

        P = ed.G
        Q = ed.point_mul(8, P)
        self.assertFalse(ed.point_equal(O, Q))

class SignatureTests(unittest.TestCase):

    def testSignature(self):
        seed = b"0"*32
        msg = b"hello, world"
        R, s = ed.sign(seed, msg)
        sig = ed.point_compress(R) + int.to_bytes(s, 32, "little")
        self.assertTrue(ed.verify(ed.secret_to_public(seed), msg, sig))

    def testMalleability(self):
        seed = b"0"*32
        msg = b"hello, world"
        R, s = ed.sign(seed, msg)

        # Signature works?
        sig = ed.point_compress(R) + int.to_bytes(s, 32, "little")
        self.assertTrue(ed.verify(ed.secret_to_public(seed), msg, sig))

        # Scale s by the group order
        s = s + ed.q
        sig = ed.point_compress(R) + int.to_bytes(s, 32, "little")

        # It works in the original looser spec
        self.assertTrue(ed.verify_non_minimal(ed.secret_to_public(seed), msg, sig))

        # But not in the RFC
        self.assertFalse(ed.verify(ed.secret_to_public(seed), msg, sig))



