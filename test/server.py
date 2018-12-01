from __future__ import absolute_import, division, unicode_literals

import concurrent.futures
import os
import select
import shutil
import socket
import ssl
import subprocess
import tempfile
import unittest

from .cert import *

class ServerTestCase(unittest.TestCase):
    workdir = None

    def _tls_setup(self):
        key = genkey(1024)
        keyfile = os.path.join(self.workdir, 'key.pem')
        keywrite(key, keyfile)

        cert = gencert(key)
        certfile = os.path.join(self.workdir, 'cert.pem')
        certwrite(cert, certfile)

        # TCP server socket.
        sock = socket.socket()
        sock.bind(('localhost', 0))
        sock.listen(5)
        port = sock.getsockname()[1]

        # Minimal TLS context.
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)

        return sock, port, context, cert, key

    def _tls_accept(self, sock, context, timeout=1):
        sock.setblocking(0)
        rs, ws, es = select.select([sock], [], [], timeout)

        self.assertTrue(sock in rs)

        ssock, addr = sock.accept()
        conn = context.wrap_socket(ssock, server_side=True)
        conn.recv()
        conn.close()

    def _tls_client(self, statusfile, fingerprints, port):
        self._cmd('certrot-server', statusfile, fingerprints, '-connect', 'localhost:{:d}'.format(port))

    def _run_server_and_client(self, sock, context, statusfile, fpfile, port):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            jobs = {
                executor.submit(self._tls_accept, sock, context),
                executor.submit(self._tls_client, statusfile, fpfile, port),
            }

            for future in concurrent.futures.as_completed(jobs):
                future.result()

    def _cmd(self, *args, **kwds):
        kwds.setdefault("cwd", self.workdir)
        return subprocess.check_output(args, **kwds)

    def setUp(self):
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        if self.workdir is not None:
            shutil.rmtree(self.workdir)

    def testServerCertFingerprintMatch(self):
        """
        Must not generate a status file when any fingerprint is matching the
        server cert.
        """
        sock, port, context, expectedcert, _ = self._tls_setup()

        otherkey = genkey(1024)
        othercert = gencert(otherkey)

        fpfile = os.path.join(self.workdir, 'fingerprints.txt')
        with open(fpfile, "wb") as stream:
            stream.write(certfp(othercert))
            stream.write(certfp(expectedcert))

        statusfile = os.path.join(self.workdir, 'status.txt')

        self._run_server_and_client(sock, context, statusfile, fpfile, port)
        self.assertFalse(os.path.exists(statusfile))

        sock.close()

    def testServerFingerprintMismatch(self):
        """
        Should generate a status file when no fingerprint is matching the
        server cert.
        """
        sock, port, context, _, _ = self._tls_setup()

        otherkey = genkey(1024)
        othercert = gencert(otherkey)

        fpfile = os.path.join(self.workdir, 'fingerprints.txt')
        with open(fpfile, "wb") as stream:
            stream.write(certfp(othercert))

        statusfile = os.path.join(self.workdir, 'status.txt')

        self._run_server_and_client(sock, context, statusfile, fpfile, port)
        self.assertTrue(os.path.exists(statusfile))

        sock.close()

    def testStatusClearedAfterRenewal(self):
        """
        Should remove status file when fingerprints match.
        """
        sock, port, context, expectedcert, _ = self._tls_setup()

        otherkey = genkey(1024)
        othercert = gencert(otherkey)

        fpfile = os.path.join(self.workdir, 'fingerprints.txt')
        with open(fpfile, "wb") as stream:
            stream.write(certfp(othercert))

        statusfile = os.path.join(self.workdir, 'status.txt')
        self._run_server_and_client(sock, context, statusfile, fpfile, port)

        self.assertTrue(os.path.exists(statusfile))

        # Certificate renewal (simulated by updating fingerprints).
        with open(fpfile, "wb") as stream:
            stream.write(certfp(expectedcert))

        self._run_server_and_client(sock, context, statusfile, fpfile, port)

        self.assertFalse(os.path.exists(statusfile))

        sock.close()
