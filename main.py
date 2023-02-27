import threading

import scan
import argparse
import os


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def main(file: str, threads: int):
    if file == "":
        print("No file was found.")
        return

    with open(file, "r") as f:
        vulnerable_hosts: list = []
        not_vulnerable_hosts: list = []
        thread_count: int = 0
        for url in f.readlines():
            if thread_count >= threads:
                print(threads)

            thread_count += 1
            sc: scan.Scanner = scan.Scanner(url.strip("\n"))
            sc.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True, metavar="str")
    parser.add_argument("--threads", "-t", metavar="int", default=10)
    args = parser.parse_args()
    print(type(args))
    main(args.file, args.threads)
