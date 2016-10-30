import argparse
import os


def are_files_duplicates(file_path1, file_path2):
    return os.path.getsize(file_path1) == os.path.getsize(file_path2)


def find_file_duplicates(dir_path):
    path_to_files = {}
    for root, dir_names, file_names in os.walk(top=dir_path):
        for file_name in file_names:
            if file_name in path_to_files:
                path_to_files[file_name].append(root)
            else:
                path_to_files[file_name] = [root]
    path_to_file_duplicates = {}
    for file_name, dir_names in path_to_files.items():
        while dir_names:
            dir_name1 = dir_names.pop(0)
            for dir_name2 in dir_names:
                file_path1 = os.path.join(dir_name1, file_name)
                file_path2 = os.path.join(dir_name2, file_name)
                if are_files_duplicates(file_path1, file_path2):
                    if file_name not in path_to_file_duplicates:
                        path_to_file_duplicates[file_name] = [dir_name1,
                                                              dir_name2]
                    elif dir_name1 not in path_to_file_duplicates[file_name]:
                        path_to_file_duplicates[file_name].append(dir_name1)
                    elif dir_name2 not in path_to_file_duplicates[file_name]:
                        path_to_file_duplicates[file_name].append(dir_name2)
    return path_to_file_duplicates


def print_file_duplicates(path_to_file_duplicates):
    output_message = 'Дубликаты файла %s найдены в следующих папках: %s'
    for file_name, dir_names in path_to_file_duplicates.items():
        file_duplicates_in_dir_names = ', '.join(dir_names)
        print(output_message % (file_name, file_duplicates_in_dir_names))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Скрипт принимает на вход
    путь к каталогу, затем просматривает все вложенные каталоги и выводит на
    экран найденные дубликаты файлов''')
    parser.add_argument('--dirpath', '-dir', default='asdf',
                        help='Имя верхнего каталога')
    dir_path = parser.parse_args().dirpath
    path_to_file_duplicates = find_file_duplicates(dir_path)
    print_file_duplicates(path_to_file_duplicates)
