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

    
            
def parse_max_tp(list_of_files : list, repeat = 5):
    avg_results = {}
    data = []

    i = 0
    # read every file in the folder
    for file_path in list_of_files:
        file_name = os.path.basename(file_path).split('.txt')[0]
        print("parsing " + file_path)
        result = []
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
                
        for i in range(0, len(data), repeat):
            avg_tp = np.mean([x[0] for x in data[i:i+repeat]])
            std_tp = np.std([x[0] for x in data[i:i+repeat]])
            avg_lt = np.mean([x[1] for x in data[i:i+repeat]])
            result.append((avg_tp, std_tp, avg_lt))

        # sort the result
        result.sort(key=lambda x: x[0], reverse=True)
        # all throughputs 
        avg_results[file_name] = [x[0] for x in result]
        # all stds
        avg_results[file_name + "-std"] = [x[1] for x in result]
        avg_results[file_name + "-lt"] = [x[2] for x in result]
                
    return avg_results
        

def parse_tp_only(list_of_files : list, repeat = 5):
    avg_results = {}
    data = []

    i = 0
    # read every file in the folder
    for file_path in list_of_files:
        file_name = os.path.basename(file_path).split('.txt')[0]
        print("parsing " + file_path)
        result = []
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
                        data.append((throughput))
                        print(f"throughput: {throughput}")
                        i += 1
                        if i % repeat == 0:
                            print("---")
                            
                    else:
                        first_line = False

                    newrun = True
                elif line.startswith("Throughput:") and newrun:
                    throughput = line.split(':')[1].split(' ')[1].strip()
                    throughput = float(throughput)
                    newrun = False
            
            data.append(throughput)
            print(f"throughput: {throughput}")
                
        for i in range(0, len(data), repeat):
            avg_tp = np.mean([x for x in data[i:i+repeat]])
            std_tp = np.std([x for x in data[i:i+repeat]])
            result.append((avg_tp, std_tp))

        # all throughputs 
        avg_results[file_name] = [x[0] for x in result]
        # all stds
        avg_results[file_name + "-std"] = [x[1] for x in result]
                
    return avg_results

def parse_target_tp_vs_med_lt(list_of_files : list, repeat = 5):
    i = 0
    
    if len(list_of_files) > 1:
        raise Exception("This method only support one file")

    # read every file in the folder
    for file_path in list_of_files:
        file_name = os.path.basename(file_path).split('.txt')[0]
        print("parsing " + file_path)
        with open(file_path, 'r') as f:
            data = []
            lines = f.readlines()
            first_line = True
            at_type = -1
            for line in lines:
                    
                if line.startswith("Target Output TPS:"):
                    # new run
                    if not first_line:
                        data.append((target_tp, get_lt, update_lt, safe_update_lt))
                        print(f"throughput: {target_tp}, latency: {get_lt}, {update_lt}, {safe_update_lt}")
                        i += 1
                        if i % repeat == 0:
                            print("---")
                            
                    else:
                        first_line = False

                    target_tp = line.split(':')[1].strip()
                    target_tp = float(target_tp)

                elif line.startswith("Get operations"):
                    at_type = 0
                elif line.startswith("Update operations"):
                    at_type = 1
                elif line.startswith("Safe update operations"):
                    at_type = 2
                elif line.startswith("Average latency:"):                        
                    latency = line.split("Median latency:")[1].split(';')[0].strip("ms").strip()
                    latency = float(latency)
                    if at_type == 0:
                        get_lt = latency
                    elif at_type == 1:
                        update_lt = latency
                    elif at_type == 2:
                        safe_update_lt = latency
                    
            
            data.append((target_tp, get_lt, update_lt, safe_update_lt))
            print(f"throughput: {target_tp}, latency: {get_lt}, {update_lt}, {safe_update_lt}")
                    

    parsed_result = { "target_tp0": [], "get": [],  "get_std": [], 
                    "target_tp1": [], "update": [], "update_std": [], 
                    "target_tp2": [], "safe_update": [], "safe_update_std": [] }
    # to make it compatible with graphing script, target_tp is repeated, and stds are 0
                      
    for value in data:
        parsed_result["target_tp0"].append(value[0])
        parsed_result["target_tp1"].append(value[0])
        parsed_result["target_tp2"].append(value[0])
        parsed_result["get"].append(value[1])
        parsed_result["update"].append(value[2])
        parsed_result["safe_update"].append(value[3])
        parsed_result["get_std"].append(0)
        parsed_result["update_std"].append(0)
        parsed_result["safe_update_std"].append(0)
        
        

    # take the median of every reapt
    final_results = {}
    for key, value in parsed_result.items():
        medians = []
        for i in range(0, len(value), repeat):
            medians.append(np.median(value[i:i+repeat]))
        final_results[key] = medians

    print(final_results)
    return final_results


def parse_target_tp_vs_percentile_lt(list_of_files : list, percentile : int, repeat = 5):
    i = 0

    if percentile != 99 and percentile != 95:
        raise Exception("This method only support 99 and 95 percentile")
    
    if len(list_of_files) > 1:
        raise Exception("This method only support one file")

    # read every file in the folder
    for file_path in list_of_files:
        file_name = os.path.basename(file_path).split('.txt')[0]
        print("parsing " + file_path)
        with open(file_path, 'r') as f:
            data = []
            lines = f.readlines()
            first_line = True
            at_type = -1
            for line in lines:
                    
                if line.startswith("Target Output TPS:"):
                    # new run
                    if not first_line:
                        data.append((target_tp, get_lt, update_lt, safe_update_lt))
                        print(f"throughput: {target_tp}, latency: {get_lt}, {update_lt}, {safe_update_lt}")
                        i += 1
                        if i % repeat == 0:
                            print("---")
                            
                    else:
                        first_line = False

                    target_tp = line.split(':')[1].strip()
                    target_tp = float(target_tp)

                elif line.startswith("Get operations"):
                    at_type = 0
                elif line.startswith("Update operations"):
                    at_type = 1
                elif line.startswith("Safe update operations"):
                    at_type = 2
                elif line.startswith("99th percentile latency:"):                
                    if percentile == 99:
                        latency = line.split("99th percentile latency:")[1].split(';')[0].strip("ms").strip()
                    elif percentile == 95:
                        latency = line.split("95th percentile latency:")[1].split(';')[0].strip().strip("ms").strip()
                    
                    latency = float(latency)
                    if at_type == 0:
                        get_lt = latency
                    elif at_type == 1:
                        update_lt = latency
                    elif at_type == 2:
                        safe_update_lt = latency
                    
            
            data.append((target_tp, get_lt, update_lt, safe_update_lt))
            print(f"throughput: {target_tp}, latency: {get_lt}, {update_lt}, {safe_update_lt}")
                    

    parsed_result = { "target_tp0": [], "get": [],  "get_std": [], 
                    "target_tp1": [], "update": [], "update_std": [], 
                    "target_tp2": [], "safe_update": [], "safe_update_std": [] }
    # to make it compatible with graphing script, target_tp is repeated, and stds are 0
                      
    for value in data:
        parsed_result["target_tp0"].append(value[0])
        parsed_result["target_tp1"].append(value[0])
        parsed_result["target_tp2"].append(value[0])
        parsed_result["get"].append(value[1])
        parsed_result["update"].append(value[2])
        parsed_result["safe_update"].append(value[3])
        parsed_result["get_std"].append(0)
        parsed_result["update_std"].append(0)
        parsed_result["safe_update_std"].append(0)
        
        

    # take the median of every reapt
    final_results = {}
    for key, value in parsed_result.items():
        medians = []
        for i in range(0, len(value), repeat):
            medians.append(np.median(value[i:i+repeat]))
        final_results[key] = medians

    print(final_results)
    return final_results


def parse_target_tp_vs_idv_avg_lt(list_of_files : list, repeat = 5):
    i = 0
    
    if len(list_of_files) > 1:
        raise Exception("This method only support one file")

    # read every file in the folder
    for file_path in list_of_files:
        file_name = os.path.basename(file_path).split('.txt')[0]
        print("parsing " + file_path)
        with open(file_path, 'r') as f:
            data = []
            lines = f.readlines()
            first_line = True
            at_type = -1
            for line in lines:
                    
                if line.startswith("Target Output TPS:"):
                    # new run
                    if not first_line:
                        data.append((target_tp, get_lt, update, safe_update))
                        print(f"throughput: {target_tp}, latency: {get_lt}, {update}, {safe_update}")
                        i += 1
                        if i % repeat == 0:
                            print("---")
                            
                    else:
                        first_line = False

                    target_tp = line.split(':')[1].strip()
                    target_tp = float(target_tp)

                elif line.startswith("Get operations"):
                    at_type = 0
                elif line.startswith("Update operations"):
                    at_type = 1
                elif line.startswith("Safe update operations"):
                    at_type = 2
                elif line.startswith("Average latency:"):                        
                    latency = line.split("Average latency:")[1].split(';')[0].strip("ms").strip()
                    latency = float(latency)
                    if at_type == 0:
                        get_lt = latency
                    elif at_type == 1:
                        update = latency
                    elif at_type == 2:
                        safe_update = latency
                    
            
            data.append((target_tp, get_lt, update, safe_update))
            print(f"throughput: {target_tp}, latency: {get_lt}, {update}, {safe_update}")
                    


        
    avg_tp = []
    avg_get_lt = []
    std_get_lt = []
    avg_update_lt = []
    std_update_lt = []
    avg_safe_lt = []
    std_safe_lt = []
    # take the avg and std for every reapt
    for i in range(0, len(data), repeat):
        avg_tp.append(np.mean([x[0] for x in data[i:i+repeat]]))
        avg_get_lt.append(np.mean([x[1] for x in data[i:i+repeat]]))
        std_get_lt.append(np.std([x[1] for x in data[i:i+repeat]]))
        avg_update_lt.append(np.mean([x[2] for x in data[i:i+repeat]]))
        std_update_lt.append(np.std([x[2] for x in data[i:i+repeat]]))
        avg_safe_lt.append(np.mean([x[3] for x in data[i:i+repeat]]))
        std_safe_lt.append(np.std([x[3] for x in data[i:i+repeat]]))

    final_results = {}
    final_results["target_tp"] = avg_tp
    final_results["get"] = avg_get_lt
    final_results["get_std"] = std_get_lt
    final_results["update"] = avg_update_lt
    final_results["update_std"] = std_update_lt
    final_results["safe"] = avg_safe_lt
    final_results["safe_std"] = std_safe_lt

    print(final_results)
    return final_results


# banking
def parse_target_tp_vs_idv_avg_lt2(list_of_files : list, repeat = 5):
    i = 0
    
    if len(list_of_files) > 1:
        raise Exception("This method only support one file")

    # read every file in the folder
    for file_path in list_of_files:
        file_name = os.path.basename(file_path).split('.txt')[0]
        print("parsing " + file_path)
        with open(file_path, 'r') as f:
            data = []
            lines = f.readlines()
            first_line = True
            at_type = -1
            for line in lines:
                    
                if line.startswith("Target Output TPS:"):
                    # new run
                    if not first_line:
                        data.append((target_tp, get_lt, deposit_lt, transfer_lt, withdraw_lt))
                        print(f"throughput: {target_tp}, latency: {get_lt}, {deposit_lt}, {transfer_lt}, {withdraw_lt}")
                        i += 1
                        if i % repeat == 0:
                            print("---")
                            
                    else:
                        first_line = False

                    target_tp = line.split(':')[1].strip()
                    target_tp = float(target_tp)

                elif line.startswith("View Ops"):
                    at_type = 0
                elif line.startswith("Deposit Ops"):
                    at_type = 1
                elif line.startswith("Transfer Ops"):
                    at_type = 2
                elif line.startswith("Withdraw Ops:"):
                    at_type = 3
                elif line.startswith("Average latency:"):                        
                    latency = line.split("Average latency:")[1].split(';')[0].strip("ms").strip()
                    latency = float(latency)
                    if at_type == 0:
                        get_lt = latency
                    elif at_type == 1:
                        deposit_lt = latency
                    elif at_type == 2:
                        transfer_lt = latency
                    elif at_type == 3:
                        withdraw_lt = latency
                    
            
            data.append((target_tp, get_lt, deposit_lt, transfer_lt, withdraw_lt))
            print(f"throughput: {target_tp}, latency: {get_lt}, {deposit_lt}, {transfer_lt}, {withdraw_lt}")
                    


        
    avg_tp = []
    avg_get_lt = []
    std_get_lt = []
    avg_deposit_lt = []
    std_deposit_lt = []
    avg_withdraw_lt = []
    std_withdraw_lt = []
    avg_transfer_lt = []
    std_transfer_lt = []
    # take the avg and std for every reapt
    for i in range(0, len(data), repeat):
        avg_tp.append(np.mean([x[0] for x in data[i:i+repeat]]))
        avg_get_lt.append(np.mean([x[1] for x in data[i:i+repeat]]))
        std_get_lt.append(np.std([x[1] for x in data[i:i+repeat]]))
        avg_deposit_lt.append(np.mean([x[2] for x in data[i:i+repeat]]))
        std_deposit_lt.append(np.std([x[2] for x in data[i:i+repeat]]))
        avg_transfer_lt.append(np.mean([x[3] for x in data[i:i+repeat]]))
        std_transfer_lt.append(np.std([x[3] for x in data[i:i+repeat]]))
        avg_withdraw_lt.append(np.mean([x[4] for x in data[i:i+repeat]]))
        std_withdraw_lt.append(np.std([x[4] for x in data[i:i+repeat]]))

    final_results = {}
    final_results["target_tp"] = avg_tp
    final_results["get"] = avg_get_lt
    final_results["get_std"] = std_get_lt
    final_results["deposit"] = avg_deposit_lt
    final_results["deposit_std"] = std_deposit_lt
    final_results["transfer"] = avg_transfer_lt
    final_results["transfer_std"] = std_transfer_lt
    final_results["withdraw"] = avg_withdraw_lt
    final_results["withdraw_std"] = std_withdraw_lt

    print(final_results)
    return final_results

# Hotstuff
def parse_tp_avg_lt2(list_of_files : list, repeat = 5):
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
                            print(f"throughput: {throughput}, latency: {latency}")
                            i += 1
                            if i % repeat == 0:
                                print("---")
                                
                        else:
                            first_line = False

                        newrun = True
                    elif line.startswith("Average latency:") and newrun:                        
                        latency = line.split(';')[0].split(':')[1].strip("ms\n")
                        latency = float(latency)
                    elif line.startswith("Throughput:") and newrun:
                        throughput = line.split(':')[1].split(' ')[1].strip()
                        throughput = float(throughput)
                        newrun = False
                
                data.append((throughput, latency))
                print(f"throughput: {throughput}, latency: {latency}")
                    

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
                
                

folder_paths = ["./results/orset/orset-n4-b500-repeat5/"]
whitelist = ["orset-n4-5050RW-1-objs.txt"]

if __name__ == "__main__":
    list_of_files = get_files(folder_paths, whitelist)
    result_dict = parse_tp_only(list_of_files, 5)
    output_csv(result_dict, "result.csv")

    
