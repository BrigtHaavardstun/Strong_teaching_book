import csv
import heapq
import os

def read_csv_in_chunks(file, chunk_size):
    while True:
        lines = []
        for _ in range(chunk_size):
            try:
                lines.append(next(file))
            except StopIteration:
                break
        if not lines:
            break
        yield lines

def k_way_merge(temp_file_readers, key=None):
    heap = []
    for i, reader in enumerate(temp_file_readers):
        try:
            row = next(reader)
            if key:
                heap.append((key(row), i, row))
            else:
                heap.append((row, i, row))
        except StopIteration:
            pass
    heapq.heapify(heap)
    
    while heap:
        if key:
            _, idx, row = heapq.heappop(heap)
        else:
            _, idx, row = heapq.heappop(heap)
        yield row
        
        try:
            next_row = next(temp_file_readers[idx])
            if key:
                heapq.heappush(heap, (key(next_row), idx, next_row))
            else:
                heapq.heappush(heap, (next_row, idx, next_row))
        except StopIteration:
            pass

def external_sort(input_filename, output_filename, chunk_size=10000, key=None):
    # Step 1 and 2: Read in chunks, sort, and write to temp files
    temp_files = []
    with open(input_filename, 'r') as input_file:
        csv_reader = csv.reader(input_file)
        for i, chunk in enumerate(read_csv_in_chunks(csv_reader, chunk_size)):
            chunk.sort(key=key)
            temp_file_name = f'temp_file_{i}.csv'
            with open(temp_file_name, 'w', newline='') as temp_file:
                csv.writer(temp_file).writerows(chunk)
            temp_files.append(temp_file_name)

    # Step 3: Merge sorted chunks
    with open(output_filename, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        
        # Reopen temp files for reading
        temp_file_readers = [csv.reader(open(temp_file, 'r')) for temp_file in temp_files]

        # Merge the chunks using k-way merge
        merged_chunks = k_way_merge(temp_file_readers, key)
        
        csv_writer.writerows(merged_chunks)
    
    # Clean up - Close and delete temp files
    for temp_file in temp_files:
        os.remove(temp_file)
        
from ConceptClass import sizeFunction_c
if __name__ == '__main__': 
    # Usage Example
    external_sort('all_booleans.txt', 'outputAnswerb.csv', chunk_size=100, key=lambda x: x[0])
    external_sort('outputAnswerb.csv', 'outputAnswerb.csv', chunk_size=100, key=lambda x: sizeFunction_c(x[0]))
