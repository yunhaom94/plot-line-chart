import os
import sys
import csv

import numpy as np

def get_files(folder_paths : list, whitelist : list = []) -> list:
    ''' Get all the files in the folder '''
    result = []
    for folder_path in folder_paths:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                if len(whitelist) != 0 and file_name not in whitelist:
                    continue
                result.append(folder_path + file_name)

    return result

def output_csv(parsed_result : dict, file_name):
    ''' Output the parsed result to a csv file '''
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
    with open(os.path.join(file_name), "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)


def parse_tp_avg_lt(list_of_files : list, repeat = 5):
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
                newrun = False
                first_line = True
                for line in lines:
                    if line.startswith("Benchmark Results:"):
                        # new run
                        if newrun:
                            raise Exception("Error: new run before previous run is finished")

                        if not first_line:
                            data.append((throughput, latency))
                            print(f"throughput: {throughput}, latency: {latency}, latency_std: {latency_std}")
                            i += 1
                            if i % repeat == 0:
                                print("---")
                                
                        else:
                            first_line = False

                        newrun = True
                    elif line.startswith("Average latency:") and newrun:                        
                        latency = line.split(';')[0].split(':')[1].strip("ms").strip()
                        latency = float(latency)
                        latency_std = line.split('Stdv latency:')[1].strip("ms").strip()
                    elif line.startswith("Throughput:") and newrun:
                        throughput = line.split(':')[1].split(' ')[1].strip()
                        throughput = float(throughput)
                        newrun = False
                
                data.append((throughput, latency))
                print(f"throughput: {throughput}, latency: {latency}, latency_std: {latency_std}")
                    

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
    
    # output_csv(parsed_result)
        
    avg_results = {}
    last_tps_std = [] 
    
    for key, value in parsed_result.items():
        means = []
        stds = []
        
        for i in range(0, len(value), repeat):
            means.append(sum(value[i:i+repeat])/repeat)
            stds.append(np.std(value[i:i+repeat]))

        if key.startswith("x"): # at throughput column
            last_tps_std = stds
            avg_results[key] = means
        else:
            avg_results[key] = means
            avg_results[key + "-ltstd"] = stds

    return avg_results

    
            


        
                
            



folder_paths = ["./results/pnc/pnc-n4-b1000-repeat5/"]
whitelist = ["pnc-n4-5050RW-1.txt"]

if __name__ == "__main__":
    list_of_files = get_files(folder_paths, whitelist)
    result_dict = parse_tp_avg_lt(list_of_files, 5)
    output_csv(result_dict, "result.csv")

    
