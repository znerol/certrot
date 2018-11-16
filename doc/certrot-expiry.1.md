% certrot-expiry(1) Certrot User Manuals
% Lorenz Schori
% November 16, 2018

# NAME

certrot-expiry - Writes a status message to a file if certificate is about to expire.

# SYNOPSIS

certrot-expiry status-path cert.pem ttl

# DESCRIPTION

Checks whether the certificate will expire within the time-to-live specified in
seconds.

Exits with zero status regardless of whether certificate will expire or not. It
is necessary to examine the *status-path* in order to determine the result.
Note that *status-path* is only created when certificate is about to expire.
Hence it is possible to trigger automatic certificate renewal if the file
exists.

Exits with a non-zero status if an error occured.

Common values for the ttl parameter:

86400
:   Twenty four hours.

604800
:   7 days.

2592000
:   30 days.
