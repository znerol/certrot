from __future__ import absolute_import, division, unicode_literals

import os
import shutil
import subprocess
import tempfile
import unittest

from .cert import *

DAY = 24 * 3600

class ExpiryTestCase(unittest.TestCase):
    workdir = None

    def _cmd(self, *args, **kwds):
        kwds.setdefault("cwd", self.workdir)
        return subprocess.check_output(args, **kwds)

    def setUp(self):
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        if self.workdir is not None:
            shutil.rmtree(self.workdir)

    def testNonExpiredCert(self):
        certpath = os.path.join(self.workdir, "cert.pem")
        certwrite(gencert(genkey(), days=30), certpath)

        statuspath = os.path.join(self.workdir, "cert.status")
        self._cmd("certrot-expiry", statuspath, certpath, str(10 * DAY))
        self.assertFalse(os.path.exists(statuspath))

    def testExpiredCert(self):
        certpath = os.path.join(self.workdir, "cert.pem")
        certwrite(gencert(genkey(), days=1), certpath)

        statuspath = os.path.join(self.workdir, "cert.status")
        self._cmd("certrot-expiry", statuspath, certpath, str(10 * DAY))
        self.assertTrue(os.path.exists(statuspath))

    def testStatusClearedAfterRenewal(self):
        """
        Should remove status file after certificate has been replaced.
        """
        key = genkey()
        certpath = os.path.join(self.workdir, "cert.pem")
        certwrite(gencert(key, days=1), certpath)

        statuspath = os.path.join(self.workdir, "cert.status")
        self._cmd("certrot-expiry", statuspath, certpath, str(10 * DAY))
        self.assertTrue(os.path.exists(statuspath))

        # Certificate renewal.
        certwrite(gencert(key, days=30), certpath)

        self._cmd("certrot-expiry", statuspath, certpath, str(10 * DAY))
        self.assertFalse(os.path.exists(statuspath))
