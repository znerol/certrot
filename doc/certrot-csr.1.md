% certrot-csr(1) Certrot User Manuals
% Lorenz Schori
% November 16, 2018

# NAME

certrot-csr - Writes a status message to a file if certificate does not match CSR.

# SYNOPSIS

certrot-csr status-path csr.pem cert.pem

# DESCRIPTION

Examines the subject and the public key of both, a certificate and a CSR and
compares them. Writes a message to the *status-path* if they do not match.

Exits with zero status regardless of whether certificate and CSR do match ar
not. It is necessary to examine the *status-path* in order to determine the
result. Note that *status-path* is only created when certificate and CSR do
*not* match. Hence it is possible to trigger automatic certificate renewal if
the file exists.

Exits with a non-zero status if an error occured.
