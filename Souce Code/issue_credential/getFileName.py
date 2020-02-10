import os


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return root, dirs, files


def main():
    file_dir = 'config'
    root, dirs, files = file_name(file_dir)
    print(root)
    print(dirs)
    print(files)


if __name__ == '__main__':
    main()
