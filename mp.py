import sys
import os
import struct
import heapq
import multiprocessing as mp
from itertools import islice


def sort_chunk(args):
    lines, idx, tmpdir = args
    nums = sorted(int(line) for line in lines)
    tmp_path = os.path.join(tmpdir, f"chunk_{idx:06d}.tmp")
    with open(tmp_path, 'wb') as f:
        f.write(struct.pack(f'{len(nums)}I', *nums))
    return tmp_path


def ints_from_bin(filepath):
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            for num in struct.iter_unpack('I', chunk):
                yield num[0]


def external_sort(input_txt, k):
    total = 0
    with open(input_txt, 'r') as f:
        for line in f:
            if line.strip():
                total += 1

    if total <= k:
        nums = []
        with open(input_txt, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    nums.append(int(line))
        nums.sort()
        output_path = input_txt.rsplit('.', 1)[0] + '_sorted.txt'
        with open(output_path, 'w') as f:
            f.write("\n".join(map(str, nums)))
        return output_path

    tmpdir = os.path.dirname(input_txt) or "."
    num_chunks = (total + k - 1) // k
    tasks = []

    with open(input_txt, 'r') as f:
        for i in range(num_chunks):
            chunk = [line.strip() for line in islice(f, k) if line.strip()]
            if chunk:
                tasks.append((chunk, i, tmpdir))

    with mp.Pool(processes=mp.cpu_count()) as pool:
        temp_bin_files = pool.map(sort_chunk, tasks)

    output_path = input_txt.rsplit('.', 1)[0] + '_sorted.txt'
    iterators = [ints_from_bin(tf) for tf in temp_bin_files]

    with open(output_path, 'w') as out:
        for val in heapq.merge(*iterators):
            out.write(str(val) + "\n")

    for tf in temp_bin_files:
        os.remove(tf)

    return output_path


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python mp.py <txt_file> <k>")
        sys.exit(1)
    input_filename = sys.argv[1]
    mem_limit = int(sys.argv[2])
    result = external_sort(input_filename, mem_limit)
    print(f"Sorted file: {result}")