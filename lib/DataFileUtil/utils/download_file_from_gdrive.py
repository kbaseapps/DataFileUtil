"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Requires enabling "Google Drive API" in console.cloud.google.com
"""
# [START drive_download_file]

from __future__ import print_function

import io
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import pathlib

def download_file_from_gdrive(real_file_id):
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    


    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(pathlib.Path(__file__).parent.resolve()) + "/google_authentication.json"
    creds, _ = google.auth.default()


    # create drive api client
    service = build('drive', 'v3', credentials=creds)
    file_id = real_file_id
    filename = service.files().get(fileId=file_id).execute().get('name')
    request = service.files().get_media(fileId=file_id)

    # This will cause an issue if the user downloads a "google_authentication.json" file, 
    # otherwise this downloads to the "utils" folder
    # This app is meant to be used once and then thrown away, so the container filessystem will be cleared each run
    output_filepath = str(pathlib.Path(__file__).parent.resolve()) + "/" + filename


    file = io.FileIO(output_filepath,'w')

    downloader = MediaIoBaseDownload(file, request)
    done = False
    # Might want to either pass in a logger, or delete the print statements
    while done is False:
        status, done = downloader.next_chunk()
        print(F'Download percentage: {int(status.progress() * 100)} %')
    print ("Downloaded to ", output_filepath)
    return output_filepath


if __name__ == '__main__':
    download_file_from_gdrive(real_file_id='1m3YLV7hlFluFJOA6ztTCe4DxN0Vn9-kZ')

