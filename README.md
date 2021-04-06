# Dreamhost DNS updater
This is a short Python3 CGI script to update Dreamhost DNS entries. This is necessary for firewalls like OPNsense
that don't directly support Dreamhost, but *do* support updating a DNS entry by URL.

WHile Dreamhost has an API, the DNS API doesn't support *updates* to a DNS entry. You can add an entry *or*
delete an entry with a single URL, but not both. This simple Python3 CGI script allows the OPNsense DynDNS plugin
to update your hostnames on Dreamhost with a single URL (per host, of course).
