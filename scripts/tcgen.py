#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from multiprocessing import Pool


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def execute(filename):
    process = subprocess.Popen(['python3.9', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f'Generator ran into an error\n\n{err.decode()}')
    return out


def main(arguments):

    parser = argparse.ArgumentParser(description='Generate test cases')
    parser.add_argument('file', help="Input file", type=argparse.FileType('r'))
    parser.add_argument('-c', '--cases', help='Number of cases', type=int, default=10)
    parser.add_argument('-w', '--worker', help='Number of worker processes', type=int, default=2)
    parser.add_argument('-o', '--out', help="Output folder",
                        default=None, type=dir_path)

    args = parser.parse_args(arguments)

    pathname = os.path.abspath(args.file.name)

    filename = os.path.basename(pathname)
    args.out = args.out or os.path.dirname(pathname)

    name = filename.removesuffix('.py')
    try:
        os.makedirs(f'/{args.out}/{name}')
    except FileExistsError:
        print("DATA ALREADY GENERATED, OVERRIDING DATA")

    cnt = 0
    with Pool(processes=args.worker) as p:
        for data_in in p.imap_unordered(execute, [args.file.name] * args.cases):
            with open(f'/{args.out}/{name}/{cnt}.in', 'w') as f:
                f.write(data_in.decode())
            cnt += 1
            print('Generated %d / %d' % (cnt, args.cases))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
