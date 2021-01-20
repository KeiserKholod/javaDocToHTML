import argparse
from pathlib import Path
from javaDocToHTML.converter import ConverterToHtml
from javaDocToHTML.doc_parser import DocFile


def get_files_from_dir(dir_name: str, files):
    for file in Path(dir_name).iterdir():
        if file.is_dir():
            get_files_from_dir(str(file), files)
        if file.name.endswith('.java'):
            files.append(DocFile.parse_file(dir_name + '/' + file.name))
    return files


def get_parser():
    parser = argparse.ArgumentParser(description='javaDocToHTML')
    parser.add_argument('files', type=str, nargs='+', default=[],
                        help='Path to files or dir\'s with files')
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    files_or_dirs = args.files
    for directory in files_or_dirs:
        if Path(directory).exists():
            files = get_files_from_dir(directory, [])
            converter = ConverterToHtml(files, 'html', directory + '/')
            converter.create_html_files()
        else:
            print(f'directory {directory} doesnt exist.')
