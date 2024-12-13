import matplotlib.pyplot as plt

def process_output_data(filename):
    lines = []
    try:
        with open(filename, 'r') as f:
            linear_data = dict()
            graph_data = dict()
            for line in f:
                linear_entries = dict()
                graph_entries = dict()
                split_line = line.split()
                if len(split_line) == 0:
                    continue
                n_regs = split_line[1]
                tp = None
                func_name = split_line[0].split('/')[-1]
                if 'Graph' in line:
                    tp = 'Graph'
                    if 'Time' in line:
                        graph_entries['time'] = float(line.split()[-1])
                    line = f.readline()
                    if 'spills' in line:
                        graph_entries['spills'] = int(line.split()[-1])
                    line = f.readline()
                    if 'registers' in line:
                        graph_entries['registers'] = int(line.split()[-1])
                    graph_data[func_name + '_' + n_regs] = graph_entries
                elif 'Linear' in line:
                    tp = 'Linear'
                    if 'Time' in line:
                        linear_entries['time'] = float(line.split()[-1])
                    line = f.readline()
                    if 'spills' in line:
                        linear_entries['spills'] = int(line.split()[-1])
                    line = f.readline()
                    if 'registers' in line:
                        linear_entries['registers'] = int(line.split()[-1])
                    linear_data[func_name + '_' + n_regs] = linear_entries
                else:
                    continue

        return linear_data, graph_data
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def compare_data(linear_data, graph_data):
    graph_modded_speed = dict()
    linear_modded_speed = dict()
    linear_spills = dict()
    graph_spills = dict()
    linear_regs = dict()
    graph_regs = dict()
    for key, value in linear_data.items():
        linear_modded_speed[key] = float(value['time'])
        linear_spills[key] = int(value['spills'])
        linear_regs[key] = int(value['registers'])
    for key, value in graph_data.items():
        graph_modded_speed[key] = float(value['time'])
        graph_spills[key] = int(value['spills'])
        graph_regs[key] = int(value['registers'])
    #     plt.plot(xidx, graph_modded_speed[modded_key], 'o', label=modded_key)
    # plt.legend()
    # plt.show()
    print("Head to head comparison")
    linear_speedup = dict()
    for key in linear_modded_speed.keys():
        linear_speedup[key] = graph_modded_speed[key] / linear_modded_speed[key]
        print("Name:", key, "Graph Execution Time: ", graph_modded_speed[key], "Linear Execution Time: ", linear_modded_speed[key], "Speedup: ", linear_speedup[key])
    print("Average speedup of Linear: ", str(sum(linear_speedup.values()) / len(linear_speedup.values())) + "x")
    reg_comparison = dict()
    for key in linear_regs.keys():
        reg_comparison[key] = graph_regs[key] / linear_regs[key]
        print("Name:", key, "Graph Registers: ", graph_regs[key], "Linear Registers: ", linear_regs[key], "Ratio: ", reg_comparison[key])
    print("Average Registers used by Graph vs Linear: ", str(sum(reg_comparison.values()) / len(reg_comparison.values())) + "x")
    spill_comparison = dict()
    for key in linear_spills.keys():
        spill_comparison[key] = linear_spills[key] - graph_spills[key]
        print("Name:", key, "Graph Spills: ", graph_spills[key], "Linear Spills: ", linear_spills[key], "Difference: ", spill_comparison[key])
    print("Average Spills used by Linear vs Graph: ", str(sum(spill_comparison.values()) / len(spill_comparison.values())))

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python bril_reader.py <filename>")
        sys.exit(1)
        
    filename = sys.argv[1]
    linear_data, graph_data = process_output_data(filename)

    compare_data(linear_data, graph_data)

if __name__ == "__main__":
    main() 