import os
import sys
import csv

def get_files(folder_paths : list, whitelist : list = []) -> list:
    ''' Get all the files in the folder '''
    result = []
    for folder_path in folder_paths:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                if len(whitelist) == 0 and file_name in whitelist:
                    continue
                result.append(folder_path + file_name)

    return result


def parse_tp_avg_lt(list_of_files : list):
    ''' Parse the throughput and average latency from the result files in the folder
     and output to a csv file '''
    result = {}

    i = 0
    # read every file in the folder
    for file_path in list_of_files:
            file_name = os.path.basename(file_path).split('.txt')[0]
            print("parsing " + file_path)
            with open(file_path, 'r') as f:
                data = []
                lines = f.readlines()
                latency, throughput = -1, -1
                for line in lines:
                    if line.startswith("Average latency:") and latency == -1:
                        if latency != -1 and throughput != -1:
                            raise Exception("Error: latency is found twice")

                        latency = line.split(';')[0].split(':')[1].strip("ms").strip()
                        latency = float(latency)
                    elif line.startswith("Throughput:"):
                        if throughput != -1:
                            raise Exception("Error: throughput is found twice")

                        throughput = line.split(':')[1].split(' ')[1].strip()
                        throughput = float(throughput)

                    if latency != -1 and throughput != -1:
                        data.append((throughput, latency))
                        latency, throughput = -1, -1
                    elif latency == -1 and throughput != -1:
                        raise Exception("Error: latency is not found")
                    
                # sort data by first item
                data.sort(key=lambda x: x[0])
                result[file_name] = data
                

    # parse result into dict of lists
    parsed_result = {}
    i = 0
    for key, value in result.items():
        tps = []
        lts = []
        for item in value:
            tps.append(item[0])
            lts.append(item[1])
        parsed_result[f"x{i}"] = tps
        parsed_result[key] = lts
        i += 1
    
    # convert into csv
    max_length = max(len(lst) for lst in parsed_result.values())

    # Create a list of lists to represent the rows in the CSV file
    rows = []

    # Append header row
    header = list(parsed_result.keys())
    rows.append(header)

    # Append data rows
    for i in range(max_length):
        row = [parsed_result[key][i] if i < len(parsed_result[key]) else '' for key in header]
        rows.append(row)

    # Write to CSV file
    with open(os.path.join("parsed.csv"), "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)


folder_paths = ["./results/pnc-n4-b500-repeat5/"]

if __name__ == "__main__":
    list_of_files = get_files(folder_paths)
    parse_tp_avg_lt(list_of_files)

    
