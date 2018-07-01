from gzip import GzipFile
from scrapy.exporters import JsonLinesItemExporter


class JsonLinesGzipItemExporter(JsonLinesItemExporter):
    def __init__(self, file, **kwargs):
        gzfile = GzipFile(fileobj=file)
        super(JsonLinesGzipItemExporter, self).__init__(gzfile, **kwargs)

    def finish_exporting(self):
        self.file.close()
