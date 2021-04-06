# Dreamhost DNS updater
This is a short Python3 CGI script to update Dreamhost DNS entries. This is necessary for firewalls like OPNsense
that don't directly support Dreamhost, but *do* support updating a DNS entry by URL.

WHile Dreamhost has an API, the DNS API doesn't support *updates* to a DNS entry. You can add an entry *or*
delete an entry with a single URL, but not both. This simple Python3 CGI script allows the OPNsense DynDNS plugin
to update your hostnames on Dreamhost with a single URL (per host, of course).

## Usage

This is a CGI script that should run on any CGI-enabled web server that provides the `requests` Python3 package (along with standard packages `uuid` and `cgi`).
It has been tested on Dreamhost's own web servers, where it works fine. Place it in a directory with the following entries in `.htaccess`:
```
AddHandler cgi-script .cgi
Options +ExecCGI
```

## Security

The script should be relatively safe: it only takes inputs and passes them along to Dreamhosts's API using multiple
requests rather than a single request. The script itself contains no secrets - the API key must be passed as part of the
URL.

There's a potential issue if you install this script in a location where an unauthorized person can see access logs, since
the API key is included in the URL. If this is an issue, it may be useful to modify the script to accept information in
the form of embedded form data (POST) rather than in the URL. However, if you're installing this on a Dreamhost server
in the first place, it's likely that the logs are only accessible to you (who knows the key) and Dreamhost (who could do
whatever they want to your DNS entries), so it's likely not an issue.
