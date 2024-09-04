
import os
import datetime

from config import settings


def CleanOldDocs():
    docs_dir = settings.MEDIA_ROOT + r"docs/"

    file_names = os.listdir(docs_dir)
    for file_name in file_names:
        file = docs_dir + file_name
        date = datetime.datetime.fromtimestamp(os.stat(file).st_ctime).date()

        if date == datetime.date.today():
            os.remove(file)
