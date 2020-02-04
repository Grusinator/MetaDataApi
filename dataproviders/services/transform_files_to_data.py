import logging

from django.core.files import File
from zipfile.ZipFile

from MetaDataApi.utils.django_model_utils.django_file_utils import FileType

logger = logging.getLogger(__name__)


def handle_zipfile(file):
    # Convert file and dir into absolute paths
    fullpath = os.path.join(settings.MEDIA_ROOT, thefile.path_relative)
    dirname = os.path.dirname(fullpath)

    # Get a real Python file handle on the uploaded file
    fullpathhandle = open(fullpath, 'r')

    # Unzip the file, creating subdirectories as needed
    zfobj = zipfile.ZipFile(fullpathhandle)
    for name in zfobj.namelist():
        if name.endswith('/'):
            try:  # Don't try to create a directory if exists
                os.mkdir(os.path.join(dirname, name))
            except:
                pass
        else:
            outfile = open(os.path.join(dirname, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()
    ZipFile.
    files = decompress_zipfile(file)
    for file in files:
        handle_data_formats(file)


def transform_data_file(file: File):
    if FileType.ZIP.value in file.name:
        handle_zipfile(file)
