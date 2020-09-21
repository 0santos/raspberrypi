#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# cert.py Version 1.0
# Copyright (c) 2020 by Ernani Santos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import socket
import ssl
import os
import sys
import logging
import argparse
from urllib.parse import urlparse
from datetime import datetime

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%d-%b-%Y %H:%M:%S')
logger = logging.getLogger(__name__)


def get_der_cert(host, port):
    context = ssl.create_default_context()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            ssock.connect((host, port))
            ssl_info = ssock.getpeercert()

    cert_info(ssl_info)
    print('\nSSL connection done from %s:%s' % (host, port))

    try:
        cert = ssl.get_server_certificate((host, port))

      # convert to binary (DER format)

        der_cert = ssl.PEM_cert_to_DER_cert(cert)

      # save the certificate in (DER format)

        save_cert(host, der_cert)
    except Exception as e:
        logger.error('Error getting server certificate from %s:%s: %s'
                     % (host, port, e), exc_info=True)
        sys.exit(1)


def save_cert(host, der_cert):
    cert_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     'certs')
    if not os.path.exists(cert_path):
        os.makedirs(cert_path)
    with open(os.path.join(cert_path, '%s.%s' % (host, 'der')), 'wb') as file:
        file.write(der_cert)


def cert_info(cert):
    subject = dict(x[0] for x in cert['subject'])
    country = subject['countryName']
    issued_to = subject['commonName']
    organization = subject['organizationName']
    location = subject['stateOrProvinceName']
    issuer = dict(x[0] for x in cert['issuer'])
    issued_by = issuer['commonName']
    expiry_date = cert['notAfter']
    
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    assert expiry_date, "Cert doesn't have an expiry date."
    expiry = datetime.strptime(expiry_date, ssl_date_fmt)
    now = datetime.now()
    days_left = (expiry - now).days

   # print(cert)

    print('Country: %s' % country)
    print('Issued to: %s' % issued_to)
    print('Organization: %s' % organization)
    print('Province: %s' % location)
    print('Issued by: %s' % issued_by)
    print('Days left in cert expiry: %d' % days_left)


def main():
    """Retrieve and save out the ssl certificate.
    Args:
        URL (str): url to be picked up
   """

    parser = argparse.ArgumentParser(prog='cert', usage='%(prog)s [options] URL', description='Retrieve and save out the ssl certificate')
    parser.add_argument('url', metavar='URL', type=str, help='the URL to be picked up')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    parsed_url = urlparse(args.url)

    host = parsed_url.hostname
    if not host:
        print('Please provide a valid url')
        sys.exit(1)

    port = int(parsed_url.port or 443)
    print('Retrieve certificate from %s:%d' % (host, port))
    get_der_cert(host, port)


if __name__ == '__main__':
    main()
