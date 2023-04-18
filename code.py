import os
import sys
import re
import numpy as np

def calculate_average_mbits(log_file_path):
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            pass
        last_line = line

        unit = last_line.split(" ")[-1]
        num = last_line.split(" ")[-2]
        if unit[0] == "M":
            return float(num)
        else:
            return 0.001 * float(num)

    # pattern = re.compile(r'\d+\.\d+ Mbits/sec')
    # matches = pattern.findall(log_content)

    # total_mbits = 0
    # count = 0

    # for match in matches:
    #     total_mbits += float(match.split()[0])
    #     count += 1

    # pattern = re.compile(r'\d+\.\d+ Kbits/sec')
    # matches = pattern.findall(log_content)


    # for match in matches:
    #     print(match)
    #     print(.001 * float(match.split()[0]))
    #     total_mbits += .1 * float(match.split()[0])

    #     count += 1



    # if count > 0:
    #     return total_mbits / count
    # else:
    #     return 0


def main():
    log_directory = sys.argv[1]
    log_files = [os.path.join(log_directory, log_file) for log_file in os.listdir(log_directory)]

    short_avg = 0
    short_list = []
    short_count = 0
    long_avg = 0

    for log_file in log_files:
        if os.path.isfile(log_file):
            if "short" in log_file:
                short_avg += calculate_average_mbits(log_file)
                short_list += [calculate_average_mbits(log_file)]
                short_count += 1
            else:
                long_avg = calculate_average_mbits(log_file)
            # print(f'Average Mbits/sec for {os.path.basename(log_file)}: {average_mbits:.2f}')
    print("Short:", np.median(short_list), "Long: ", long_avg, "Ratio: ", long_avg / np.median(short_list))

if __name__ == '__main__':
    main()
