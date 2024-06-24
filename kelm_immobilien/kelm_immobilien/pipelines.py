import json
import os

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('output.json', 'w')
        self.file.write('[\n')

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.seek(self.file.tell() - 2, os.SEEK_SET)  # Move the pointer back to overwrite the last comma
        self.file.write(line)
        return item