% certrot-server(1) Certrot User Manuals
% Lorenz Schori
% November 16, 2018

# NAME

certrot-server - Writes a status message to a file if server uses an unexpected certificate.

# SYNOPSIS

certrot-server status-path fingerprints.txt -connect example.com:443 -servername example.com [*s\_client options*]...

# DESCRIPTION

Connects to the specified TLS server and retrieves its certificate. Compares
the SHA256 fingerprint with a list of supplied fingerprints and writes a status
message to the specified *status-path* if the server fingerprint is not found
in the supplied fingerprints.

Exits with zero status regardless of whether fingerprint is found or not. It
is necessary to examine the *status-path* in order to determine the result.
Note that *status-path* is only created when the servers certificate
fingerprint is missing from the supplied list of fingerprints. Hence it is
possible to trigger automatic certificate renewal/deployment if the file
exists.

Exits with a non-zero status if an error occured.

# SEE ALSO

`s_client` (1SSL).
