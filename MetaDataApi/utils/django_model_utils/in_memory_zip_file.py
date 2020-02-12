import io
import zipfile


class InMemoryZip:
    def __init__(self):
        # Create the in-memory file-like object
        self.zip_buffer = io.BytesIO()

    def append(self, filename_in_zip, file_content: str):
        '''Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip.'''
        with zipfile.ZipFile(self.zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr(filename_in_zip, io.BytesIO(str.encode(file_content, encoding="utf-8")).getvalue())

            # Mark the files as having been created on Windows so that
            # Unix permissions are not inferred as 0000
            for zfile in zip_file.filelist:
                zfile.create_system = 0

        return

    def read_binary(self):
        '''Returns a string with the contents of the in-memory zip.'''
        self.zip_buffer.seek(0)
        return self.zip_buffer.read()

    def read_str(self):
        self.zip_buffer.seek(0)
        return self.zip_buffer.read().decode()

    def write_to_file(self, filename):
        '''Writes the in-memory zip to a file.'''
        f = open(filename, "wb")
        f.write(self.read_binary())
        f.close()
