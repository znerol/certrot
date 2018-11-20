from __future__ import absolute_import, division, unicode_literals

import datetime
import functools
import itertools
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

PY3 = sys.version_info[0] == 3

if PY3:
    iterbytes = iter
else:
    iterbytes = functools.partial(itertools.imap, ord)

class FpTestCase(unittest.TestCase):
    workdir = None

    def _cmd(self, *args, **kwds):
        kwds.setdefault("cwd", self.workdir)
        return subprocess.check_output(args, **kwds)

    def _gencert(self):
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=512,
            backend=default_backend()
        )

        # Generate self signed certificate.
        subject = issuer = x509.Name([
            x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, u"CA"),
            x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, u"San Francisco"),
            x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, u"My Company"),
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, u"localhost"),
        ])

        return x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=10)
        ).sign(key, hashes.SHA256(), default_backend())

    def _genfp(self, cert):
        hexbytes = ["{:02x}".format(b).upper() for b in iterbytes(cert.fingerprint(hashes.SHA256()))]
        return "SHA256 Fingerprint={:s}\n".format(":".join(hexbytes)).encode()

    def setUp(self):
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        if self.workdir is not None:
            shutil.rmtree(self.workdir)

    def testFingerprint(self):
        cert1 = self._gencert()
        with open(os.path.join(self.workdir, "cert1.pem"), "wb") as stream:
            stream.write(cert1.public_bytes(serialization.Encoding.PEM))

        cert2 = self._gencert()
        with open(os.path.join(self.workdir, "cert2.pem"), "wb") as stream:
            stream.write(cert2.public_bytes(serialization.Encoding.PEM))

        expected = self._genfp(cert1) + self._genfp(cert2)

        output = self._cmd("certrot-fp", "cert1.pem", "cert2.pem")
        self.assertEqual(expected, output)
