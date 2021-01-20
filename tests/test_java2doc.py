import unittest
from pathlib import Path

from javaDocToHTML.__main__ import get_files_from_dir
from javaDocToHTML.converter import ConverterToHtml
from javaDocToHTML.doc_parser import Method


class Test(unittest.TestCase):
    files = get_files_from_dir(str(Path.cwd() / 'resources'), [])
    converter = ConverterToHtml(files, 'resources',
                                str(Path.cwd() / 'resources') + '/')
    converter.create_html_files()

    def test_project_exist(self):
        for i in {'', 'Book.html', 'Product.html', 'resources.html'}:
            assert Path(Path.cwd()
                        / 'resources' / 'resources_html_doc' / i).exists()

    def test_to_html(self):
        assert self.files[0].to_html().startswith('<head>')
        assert self.files[0].name == 'Book.java'
        assert len(self.files[0].classes) == 1
        assert len(self.files[0].comments) == 1

    def test_javadoc_parser(self):
        assert len(self.files) == 2
        assert self.files[0].name == 'Book.java'
        assert self.files[1].name == 'Product.java'
        assert len(self.files[0].classes) == len(self.files[0].comments) == 1
        assert len(self.files[1].classes) == len(self.files[1].comments) == 1

    def test_get_common_file(self):
        converter = ConverterToHtml([], 'project',
                                    str(Path.cwd() / 'resources'))
        converter.create_html_files()
        assert converter.project_name == 'project'
        assert len(converter.files) == 0
        assert (converter.get_common_file() ==
                '<head><title>project</title>'
                '<meta http-equiv="Content-Type" content="text/html; '
                'charset=utf-8"></head><body><br><h1>Project project</h1>'
                '<br><table id = "tbl"><tr><th colspan="2">Java files</th>'
                '</tr></table></body>')

    def test_method_details(self):
        method = Method('private void setName(String value);',
                        'private', 'setName', 'String value', 'void', None)
        assert (method.method_details_to_html() ==
                '<h4 class = \'details\'><i>method</i> '
                'setName :</h4><div class = \'detblock\'>'
                '<p class = \'left\'>private void setName(String value);</p>'
                '<p class = \'left\'><i>Access modifier:</i> private</p>'
                '<p class = \'left\'><i>Returns nothing</i></p></div>')
