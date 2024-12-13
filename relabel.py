def read_bril_file(filename):
    """
    Reads a Bril file line by line and returns the lines
    
    Args:
        filename: Path to the Bril file to read
        
    Returns:
        List of lines from the file
    """
    lines = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Remove whitespace and comments
                line = line.strip()
                if line and not line.startswith('//'):
                    lines.append(line)
        return lines
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python bril_reader.py <filename>")
        sys.exit(1)
        
    filename = sys.argv[1]
    lines = read_bril_file(filename)
    bypassNext = False

    lctr = 0
    rename_map = dict()
    new_lines = []
    for line in lines:
        if line[0] == "@":
            new_lines.append(line)
            lctr = 0
            continue
        if line[0] == "#" or line[0] == "}":
            new_lines.append(line)
            continue
        if line.split()[0] == "ret":
            new_lines.append("  " + line)
            continue
        newname = f".l{lctr}"
        if len(line.split()) == 1:
            rename_map[line.split()[0].split(":")[0]] = newname
        else:
            if line.split()[0].split(":")[0] == "jmp" or line.split()[0].split(":")[0] == "br":
                new_instr = []
                for arg in line.split():
                    #print(rename_map[arg.strip(';')])
                    if arg.strip(';') in rename_map:
                        new_instr.append(rename_map[arg.strip(';')])
                    else:
                        new_instr.append(arg)
                new_line = "  " + " ".join(new_instr)
                new_lines.append(new_line)
            else:
                new_label = newname + ":"
                new_lines.append(new_label)
                new_lines.append("  " + line)
                lctr += 1
    new_lines = []
    lctr = 0
    written = False
    for line in lines:
        if line[0] == "@":
            new_lines.append(line)
            lctr = 0
            continue
        if line[0] == "#" or line[0] == "}":
            new_lines.append(line)
            continue
        # if line.split()[0] == "ret":
        #     new_lines.append("  " + line)
        #     continue
        newname = f".l{lctr}"
        if len(line.split()) == 1:
            rename_map[line.split()[0].split(":")[0]] = newname
            written = True
        else:
            if line.split()[0].split(":")[0] == "jmp" or line.split()[0].split(":")[0] == "br":
                new_instr = []
                for arg in line.split():
                    #print(rename_map[arg.strip(';')])
                    if arg.strip(';') in rename_map:
                        new_instr.append(rename_map[arg.strip(';')])
                    else:
                        new_instr.append(arg)
                new_line = "  " + " ".join(new_instr)
                new_lines.append(new_line)
            else:
                new_label = newname + ":"
                new_lines.append(new_label)
                new_lines.append("  " + line)
                lctr += 1
            written = False
    # if written:
    #     new_lines.append(newname + ":")
        
    
    for line in new_lines:
        if line[-1] != ":" and line[-1] != "}" and line[-1] != "{" and line[-1] != ";":
            print(line + ";")
        else:
            print(line)

    # if lines:
    #     print("Contents of Bril file:")
    #     for i, line in enumerate(lines, 1):
    #         print(f"{i}: {line}")

if __name__ == "__main__":
    main()