import sys
from pathlib import Path

def main():
    if len(sys.argv) == 4:

        # PART COUNT
        try:
            int(sys.argv[2])
        except:
            print(f"<n_parts> must be a number, was '{sys.argv[2]}' which could not be converted to number")
            print("usage: %s <file> <n_parts> <out_dir>" % sys.argv[0])
            sys.exit(2)

        N_PARTS = int(sys.argv[2])
        data = [[] for _ in range(N_PARTS)]

        # INPUT FILE
        try:
            if not Path(sys.argv[1]).exists():
                print(f"<file> must be a valid filepath, requested file '{sys.argv[1]}' could not be found")
                print("usage: %s <file> <n_parts> <out_dir>" % sys.argv[0])
                sys.exit(2)
        except:
            print(f"could not resolve <file> as a valid path, may be the syntax was incorrect ('{sys.argv[1]}') ?")
            print("usage: %s <file> <n_parts> <out_dir>" % sys.argv[0])
            sys.exit(2)

        filepath = Path(sys.argv[1])

        # OUTPUT DIR
        try:
            if not Path(sys.argv[3]).is_dir():
                print(f"<out_dir> must be a valid directory, requested path '{sys.argv[1]}' does not point to a dir")
                print("usage: %s <file> <n_parts> <out_dir>" % sys.argv[0])
                sys.exit(2)
        except:
            print(f"could not resolve <out_dir> as a valid path, may be the syntax was incorrect ('{sys.argv[3]}') ?")
            print("usage: %s <file> <n_parts> <out_dir>" % sys.argv[0])
            sys.exit(2)

        out_dir = Path(sys.argv[3])

        with open(filepath.resolve(), "r", encoding="utf-8") as file:
            lines = file.readlines()
            sep = len(lines)/N_PARTS
            for i, line in enumerate(lines):
                for part in range(N_PARTS):
                    if i < sep*(part+1):
                        data[part].append(line)
                        break

        for part in range(N_PARTS):
            with open(f"{out_dir.resolve()}/{filepath.stem}-{part+1}{filepath.suffix}", "w", encoding="utf-8") as file:
                file.writelines(data[part])
        sys.exit(0)

    else:
        print("usage: %s <file> <n_parts> <out_dir>" % sys.argv[0])
        sys.exit(2)

if __name__ == '__main__':
    main()