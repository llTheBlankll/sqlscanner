import threading
import scan
import argparse
import os


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def main(file: str):
    if file == "":
        print("No file was found.")
        return

    with open(file, "r") as f:
        vulnerableHosts: list = []
        notVulnerableHosts: list = []
        for url in f.readlines():
            sc: scan.Scanner = scan.Scanner(url.strip("\n"))
            scan_result: bool = sc.scan()
            if scan_result is True:
                vulnerableHosts.append(url)
                print("%s : TRUE" % url)
            else:
                notVulnerableHosts.append(url)
                print("%s : FALSE" % url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True, metavar="str")
    args = parser.parse_args()
    main(args.file)
