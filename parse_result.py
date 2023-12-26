import os
import sys
import csv


def parse_tp_avg_lt(folder_path : str):
    ''' Parse the throughput and average latency from the result files in the folder
     and output to a csv file '''
    result = {}

    i = 0
    # read every file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            print("parsing" + file_name)
            with open(os.path.join(folder_path, file_name), 'r') as f:
                tps = []
                lts = []
                data = []
                lines = f.readlines()
                latency, throughput = -1, -1
                for line in lines:
                    if line.startswith("Average latency:") and latency == -1:
                        if latency != -1 and throughput != -1:
                            raise Exception("Error: latency is found twice")

                        latency = line.split(';')[0].split(':')[1].strip("ms").strip()
                        latency = float(latency)
                        lts.append(latency)
                    elif line.startswith("Throughput:"):
                        if throughput != -1:
                            raise Exception("Error: throughput is found twice")

                        throughput = line.split(':')[1].split(' ')[1].strip()
                        throughput = float(throughput)
                        tps.append(throughput)

                    if latency != -1 and throughput != -1:
                        data.append((throughput, latency))
                        latency, throughput = -1, -1
                    elif latency == -1 and throughput != -1:
                        raise Exception("Error: latency is not found")
                
                result["x" + str(i)] = tps
                result[file_name] = lts[:-1] # remove the last one
                i += 1

    

    max_length = max(len(lst) for lst in result.values())

    # Create a list of lists to represent the rows in the CSV file
    rows = []

    # Append header row
    header = list(result.keys())
    rows.append(header)

    # Append data rows
    for i in range(max_length):
        row = [result[key][i] if i < len(result[key]) else '' for key in header]
        rows.append(row)

    # Write to CSV file
    with open(os.path.join(folder_path, "parsed.csv"), "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)
        

        




if __name__ == "__main__":
    folder_path = sys.argv[1]
    parse_tp_avg_lt(folder_path)

    
