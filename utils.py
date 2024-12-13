import json
import sys
import base64
from IPython.display import Image, display
import matplotlib.pyplot as plt

def read_json_file(input):
    try:
        data = json.load(input)
        return data
    except json.JSONDecodeError:
        print(f"Error: The input does not contain valid JSON.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

def flatten_blocks(blocks):
    instrs = []
    for block in blocks:
        instrs += block
    return instrs

def make_dominance_tree_mermaid(idoms: dict):
    tree = "graph TD\n"
    for block_name in idoms:
        if idoms[block_name] is not None:
            tree += f"    {idoms[block_name]} --> {block_name}\n"
    return tree

def make_cfg_mermaid(blocks: dict):
    cfg = "graph TD\n"
    for block_name in blocks:
        for succ in blocks[block_name].succs:
            cfg += f"    {block_name} --> {succ}\n"
    return cfg

def get_base(var: str):
    return var.split(".")[0]

def get_order(var: str):
    splits = var.split(".")
    if len(splits) == 1:
        return 0
    return int(splits[-1])