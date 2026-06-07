import sys
import struct

def bin_to_txt(bin_path, txt_path):
    with open(bin_path, 'rb') as fin, open(txt_path, 'w') as fout:
        while True:
            chunk = fin.read(4096)
            if not chunk:
                break
            for num in struct.iter_unpack('I', chunk):
                fout.write(str(num[0]) + "\n")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python bin2txt.py <input.bin> <output.txt>")
        sys.exit(1)
    bin_to_txt(sys.argv[1], sys.argv[2])
    print("Conversion completed.")