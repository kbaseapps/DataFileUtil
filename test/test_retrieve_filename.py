"""
Test the utility function found in lib/DataFileUtil/utils/retrieve_filename.py

We use example URLs pulled from DataFileUtil_server_test.py

In the future, we could use the `responses` URL mocking package instead.
"""
import unittest
from uuid import uuid4

from DataFileUtil.utils.retrieve_filename import retrieve_filename


class RetrieveFilenameTest(unittest.TestCase):

    def test_invalid_url(self):
        url = "xyz"
        with self.assertRaises(ValueError) as ctx:
            retrieve_filename(url)
        ex = str(ctx.exception)
        msg = f"Cannot connect to URL: {url}"
        self.assertTrue(msg in ex)

    def test_no_path_no_header(self):
        """Test the case where there is no filepath and no filename header."""
        url = "https://www.google.com"
        fn = retrieve_filename(url)
        # Assert that filename is a non-empty string
        self.assertTrue(isinstance(fn, str))
        self.assertTrue(len(fn) > 0)

    def test_use_url_filepath(self):
        """
        Test the case where we cannot fetch from the URL, so
        we fallback to the url filepath.
        """
        expected_fn = str(uuid4()) + ".txt"
        url = f"https://www.example.com/{expected_fn}"
        fn = retrieve_filename(url)
        self.assertEqual(fn, expected_fn)

    def test_use_resp_header(self):
        """
        Test the case where we get the filename from the response header.
        """
        expected_fn = 'file1.txt'
        url = f"https://anl.box.com/shared/static/4ero6ld3322gnfcbssegglbdbpdvpzae.txt"
        fn = retrieve_filename(url)
        self.assertEqual(fn, expected_fn)

    def test_use_url_filepath_no_header(self):
        """
        Test the case where we are able fetch from the URL, but we get no content header
        """
        expected_fn = "SP1.fq"
        url = f"http://molb7621.github.io/workshop/_downloads/{expected_fn}"
        fn = retrieve_filename(url)
        self.assertEqual(fn, expected_fn)

    def test_filename_truncation(self):
        """
        Test the case where the retrieved filename is too long, so we truncate
        to 255 chars.
        """
        ext = ".xyz"
        given_fn = str(uuid4()) * 20 + ext
        url = f"https://www.example.com/{given_fn}"
        expected_fn = given_fn[0:252] + ext
        fn = retrieve_filename(url)
        self.assertEqual(fn, expected_fn)
