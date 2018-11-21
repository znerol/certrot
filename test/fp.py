from __future__ import absolute_import, division, unicode_literals

import os
import shutil
import subprocess
import tempfile
import unittest

from .cert import *

class FpTestCase(unittest.TestCase):
    workdir = None

    def _cmd(self, *args, **kwds):
        kwds.setdefault("cwd", self.workdir)
        return subprocess.check_output(args, **kwds)

    def setUp(self):
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        if self.workdir is not None:
            shutil.rmtree(self.workdir)

    def testFingerprint(self):
        cert1 = gencert(genkey())
        certwrite(cert1, os.path.join(self.workdir, "cert1.pem"))

        cert2 = gencert(genkey())
        certwrite(cert2, os.path.join(self.workdir, "cert2.pem"))

        expected = certfp(cert1) + certfp(cert2)

        output = self._cmd("certrot-fp", "cert1.pem", "cert2.pem")
        self.assertEqual(expected, output)
