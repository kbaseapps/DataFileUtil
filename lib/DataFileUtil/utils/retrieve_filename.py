"""
Fetch the file name from a remote URL.
"""
import requests
from typing import Optional
from requests.cookies import RequestsCookieJar
from urllib.parse import urlparse
import os

# Local
from DataFileUtil.implementation import log


def retrieve_filename(file_url: str, cookies: Optional[RequestsCookieJar] = None) -> str:
    """
    Fetch the file name from a URL using the Content-Disposition header,
    falling back to the filename found in the URL itself. We shorten any
    filename to at most 256 characters to avoid any filesystem errors.
    Args:
        file_url: HTTP(S) URL of the file to retrieve
    Returns:
        A file name using data from the given URL
    """
    try:
        # Fetch the headers
        with requests.get(file_url, cookies=cookies, stream=True) as response:
            try:
                content_disposition = response.headers['content-disposition']
            except KeyError:
                log('Parsing file name directly from URL')
                url = urlparse(file_url)
                file_name = os.path.basename(url.path)
            else:
                file_name = content_disposition.split('filename="')[-1].split('";')[0]
    except Exception as error:
        error_msg = 'Cannot connect to URL: {}\n'.format(file_url)
        error_msg += 'Exception: {}'.format(error)
        raise ValueError(error_msg)
    log(f'Retrieved file name from url: {file_name}')
    # Shorten any overly long filenames to avoid OSErrors
    # Our practical limit is 255 for eCryptfs
    if len(file_name) > 255:
        (basename, ext) = os.path.splitext(file_name)
        file_name = basename[0:255-len(ext)] + ext
    return file_name
