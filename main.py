import threading
import prettytable
import scan
import argparse
import os
import colorama


colorama.init()


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def main(file: str, thread_count: int, timeout: int, exception: str):
    if file == "":
        print("No file was found.")
        return

    with open(file, "r") as f:
        vulnerable_hosts: list[str, ...] = []
        not_vulnerable_hosts: list[str, ...] = []
        threads: list[threading.Thread, ...] = []
        for url in f.readlines():
            if len(threads) >= thread_count:
                for thread in threads:
                    url, is_vulnerable = thread.join()
                    if is_vulnerable:
                        vulnerable_hosts.append(url)
                    else:
                        not_vulnerable_hosts.append(url)
                    threads.remove(thread)

            sc: scan.Scanner = scan.Scanner(url=url.strip(), timeout=timeout, exceptions=exception)
            sc.start()
            threads.append(sc)

        for thread in threads:
            thread.join()

        for vulnerable_host in vulnerable_hosts:
            print(vulnerable_host)

        print(f"{len(vulnerable_hosts)} VULNERABLE hosts and {len(not_vulnerable_hosts)} is NOT VULNERABLE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True, metavar="File", dest="file")
    parser.add_argument("--threads", "-t", metavar="Thread", dest="threads", default=10, type=int)
    parser.add_argument("--timeout", "-a", metavar="Timeout", dest="timeout", default=30, type=int)
    parser.add_argument("--exception", "-ex", metavar="Exception", dest="exception", type=str)
    args = parser.parse_args()
    main(args.file, args.threads, args.timeout, args.exception)
