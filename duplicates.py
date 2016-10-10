import argparse
import os


def are_files_duplicates(file_path1, file_path2):
    file_name1 = file_path1.split('/')[-1]
    file_name2 = file_path2.split('/')[-1]
    # один из файлов уже может быть удалён
    if not os.path.exists(file_path1) or not os.path.exists(file_path2):
        return False
    if file_name1 == file_name2 and os.path.getsize(file_path1) == \
            os.path.getsize(file_path2):
        return True


def delete_files_duplicates(dir_path):
    dirs_and_files = list(os.walk(top=dir_path))
    output_message = 'Найдены дубликаты: %s и %s. Файл %s удалён.'
    is_deleted_file = False
    while dirs_and_files:
        dir1 = dirs_and_files[0]
        dirs_and_files.pop(0)
        for dir2 in dirs_and_files:
            dir1_files = dir1[2]
            dir2_files = dir2[2]
            for file1 in dir1_files:
                for file2 in dir2_files:
                    file_path1 = dir1[0] + '/' + file1
                    file_path2 = dir2[0] + '/' + file2
                    if are_files_duplicates(file_path1, file_path2):
                        os.remove(file_path2)
                        print(output_message % (file_path1, file_path2,
                                                file_path2))
                        is_deleted_file = True
    if not is_deleted_file:
        print('Дубликаты не найдены.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Скрипт принимает на вход
    путь к каталогу, затем просматривает все вложенные каталоги и удаляет
    найденные дубликаты файлов''')
    parser.add_argument('--dirpath', '-dir', default='asdf/',
                        help='Имя верхнего каталога')
    dir_path = parser.parse_args().dirpath
    if dir_path.endswith('/'):
        dir_path = dir_path[:-1]
    delete_files_duplicates(dir_path)
