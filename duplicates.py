import argparse
import os


def are_files_duplicates(file_path1, file_path2):
    if os.path.getsize(file_path1) == os.path.getsize(file_path2):
        return True


def find_file_duplicates(dir_path):
    dirs_and_files = os.walk(top=dir_path)
    path_to_files = {}
    for dir in dirs_and_files:
        for file in dir[2]:
            if not path_to_files.get(file, []):
                path_to_files[file] = [dir[0] + '/']
            else:
                path_to_files[file].append(dir[0] + '/')
    file_duplicates = {}
    for file, dirs in path_to_files.items():
        while dirs:
            dir1 = dirs[0]
            dirs.pop(0)
            for dir2 in dirs:
                file_path1 = dir1 + file
                file_path2 = dir2 + file
                if are_files_duplicates(file_path1, file_path2):
                    if not file_duplicates.get(file, []):
                        file_duplicates[file] = [dir1, dir2]
                    elif dir1 not in file_duplicates[file]:
                        file_duplicates[file].append(dir1)
                    elif dir2 not in file_duplicates[file]:
                        file_duplicates[file].append(dir2)
    return file_duplicates


def print_file_duplicates(file_duplicates):
    output_message = 'Дубликаты файла %s найдены в следующих папках: %s'
    for file, dirs in file_duplicates.items():
        duplicates_in_dirs = ', '.join(dirs)
        print(output_message % (file, duplicates_in_dirs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Скрипт принимает на вход
    путь к git каталогу, затем просматривает все вложенные каталоги и удаляет
    найденные дубликаты файлов''')
    parser.add_argument('--dirpath', '-dir', default='asdf/',
                        help='Имя верхнего каталога')
    dir_path = parser.parse_args().dirpath
    if dir_path.endswith('/'):
        dir_path = dir_path[:-1]
    file_duplicates = find_file_duplicates(dir_path)
    print_file_duplicates(file_duplicates)
