import lxml.etree as ET
from . import database

class BookParser:
    def __init__(self, file):
        self.file = file
        self.root = self.get_root()

    def get_root(self):
        it = ET.iterparse(self.file)
        for _, el in it:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
        return it.root

    def get_tag_text(self, tag_name, default=""):
        tag = self.root.find('.//' + tag_name)
        if tag != None and tag.text:
            return tag.text
        return default

    def get_paragraphs(self):
        for paragraph in self.root.xpath(".//body[not(contains(@name, 'info'))]//p"):
            if paragraph.text:
                yield paragraph.text

    def parse(self):
        text = "\n".join(self.get_paragraphs())

        title = self.get_tag_text("book-title")
        author = self.get_tag_text("first-name") + " " + self.get_tag_text("last-name")
        chitanka_id = self.get_tag_text("id")
        year = int(self.get_tag_text("src-title-info//date", "0"))

        return database.Book(title=title, author=author, year=year, text=text, chitanka_id=chitanka_id)

