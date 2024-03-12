"""
Fetch the file name from a remote URL.
"""
from email.message import Message
from requests.cookies import RequestsCookieJar
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from uuid import uuid4
import os
import requests

# Local
from DataFileUtil.implementation import log


_CONTENT_DISPOSITION = 'content-disposition'


def retrieve_filename(file_url: str, cookies: Optional[RequestsCookieJar] = None) -> str:
    """
    Fetch the file name from a URL using the Content-Disposition header,
    falling back to the filename found in the URL itself. We shorten any
    filename to at most 255 characters to avoid any filesystem errors.
    If we are unable to retrieve a filename from either the header or URL path,
    then we generate a UUID and use that (without any extension).
    Args:
        file_url: HTTP(S) URL of the file to retrieve
    Returns:
        A file name using data from the given URL
    """
    try:
        # Fetch the headers
        # Not sure how expensive this is for us and and the remote host, but head doesn't
        # get the content dispo header
        with requests.get(file_url, cookies=cookies, stream=True) as response:
            try:
                content_disposition = response.headers[_CONTENT_DISPOSITION]
            except KeyError:
                log('Parsing file name directly from URL')
                url = urlparse(file_url)
                file_name = os.path.basename(url.path)
            else:
                file_name = _get_filename_from_header(response)
    except Exception as error:
        error_msg = 'Cannot connect to URL: {}\n'.format(file_url)
        error_msg += 'Exception: {}'.format(error)
        raise ValueError(error_msg)
    # Shorten any overly long filenames to avoid OSErrors
    # Our practical limit is 255 for eCryptfs
    if len(file_name) > 255:
        (basename, ext) = os.path.splitext(file_name)
        file_name = basename[0:255-len(ext)] + ext
    file_name = file_name.strip()
    if len(file_name) == 0:
        # Handle the case where there is no URL filepath, and no content header
        # We just generate a unique name
        file_name = str(uuid4())
    log(f'Retrieved file name: {file_name}')
    return file_name


def _get_filename_from_header(response):
    # https://stackoverflow.com/a/78073510/643675
    # https://peps.python.org/pep-0594/#cgi
    m = Message()
    m[_CONTENT_DISPOSITION] = response.headers[_CONTENT_DISPOSITION]
    return Path(m.get_filename()).name
    