import blocks
import utils
import sys
import copy
from blocks import PhiNode
from utils import get_base, get_order
import time
import random

class CFG:
    def __init__ (self, blocks: dict, input_vars = None):
        self.input_vars = input_vars
        self.blocks = blocks
        self.vars = set() # The variables in this program
        self.defs = dict() # The variables and blocks in which they're defined
        self.read_variables()
        self.dominators = self.compute_dominators()
        self.strict_dominators = self.compute_strict_dominators()
        self.immediate_dominators = self.compute_immediate_dominators()
        self.dominance_frontiers = self.compute_dominance_frontiers()
        self.var_stack = dict.fromkeys(self.vars)
        self.counters = dict.fromkeys(self.vars)
        self.func_args = input_vars
        for var in self.vars:
            self.var_stack[var] = []
            self.counters[var] = 0
        if self.input_vars is not None:
            for var in self.input_vars:
                self.var_stack[var['name']] = [var['name'] + ".0"]
                self.counters[var['name']] = 1
                self.blocks['.start'].in_vars.add(var['name'] + ".0")
        self.terminating_blocks = set()
        for block in self.blocks.values():
            if len(block.succs) == 0:
                self.terminating_blocks.add(block.name())
    
    def __str__(self):
        str = ""
        for block_name, block in self.blocks.items():
            str += "{ "
            for pred in block.preds:
                str += pred + " "
            str += "} -> " + block.name() + " -> { "
            for succ in block.succs:
                str += succ + " "
            str += "}\n"
        return str
    
    def read_variables(self):
        self.vars = set()
        if self.input_vars is not None:
            for var in self.input_vars:
                self.vars.add(var['name'])
                self.defs[var['name']] = set()
        for block in self.blocks.values():
            for instr in block.instrs:
                if 'dest' in instr:
                    var = instr['dest']
                    if var not in self.defs:
                        self.defs[var] = set()
                    self.defs[var].add(block.name())
                    self.vars.add(var)
                

    def compute_dominators(self):
        doms = dict()
        for block_name in self.blocks:
            doms[block_name] = set(self.blocks.keys())
            
        doms[".start"] = {".start"}
        changed = True
        considered_blocks = set(self.blocks.keys()) - set([".start"])
        while changed:
            changed = False
            for block_name in considered_blocks:
                new_doms = set(self.blocks.keys())
                # The dominators of this block are the intersection 
                # of the dominators of its predecessors
                for pred in self.blocks[block_name].preds:
                    new_doms = new_doms.intersection(doms[pred])
                # Plus itself
                new_doms.add(block_name)
                # If the dominators of this block have changed, update them
                # and trigger a new iteration of the outer loop
                if new_doms != doms[block_name]:
                    doms[block_name] = new_doms
                    changed = True
        return doms

    def compute_strict_dominators(self):
        # Strict dominators are simply the dominators minus the block itself
        doms = self.compute_dominators()
        sdoms = dict()
        for block_name in self.blocks:
            sdoms[block_name] = doms[block_name] - set([block_name])
        return sdoms

    def compute_immediate_dominators(self):
        sdoms = self.compute_strict_dominators()
        idoms = dict.fromkeys(self.blocks.keys(), None)
        for block_name in self.blocks:
            # If this block has no strict dominators, skip it
            if len(sdoms[block_name]) == 0:
                continue
            # If this block has only one strict dominator, it is its immediate dominator
            if len(sdoms[block_name]) == 1:
                idoms[block_name] = next(iter(sdoms[block_name]))
                continue

            # For multiple strict dominators, find the one that is dominated by all others
            # This will be the "lowest" dominator in the dominator tree
            candidates = sdoms[block_name].copy()
            
            for sdom in sdoms[block_name]:
                # Remove sdom if it dominates any other candidate
                # Since it can't be the immediate dominator
                for other_sdom in sdoms[block_name]:
                    if other_sdom != sdom and sdom in sdoms[other_sdom]:
                        candidates.discard(sdom)
                        break
            if len(candidates) == 1:
                idoms[block_name] = next(iter(candidates))
            else:
                # If we have multiple candidates, something went wrong
                print(f"Warning: Multiple or no candidates for {block_name}: {candidates}")
        return idoms

    def compute_dominance_frontiers(self):
        dom_frontiers = dict()
        sdoms = self.compute_strict_dominators()
        for block_name in self.blocks:
            dom_frontiers[block_name] = set()
        for block_name in self.blocks:
            # The dominance frontier of a block is either a successor
            # or a successor of a successor
            check_list = list(self.blocks[block_name].succs)
            seen = set()
            while len(check_list) > 0:
                successor = check_list.pop()
                if successor in seen:
                    # prevent infinite iteration
                    continue
                elif block_name not in sdoms[successor]:
                    # if this successor is not strictly dominated by the block
                    # then it is in the dominance frontier
                    dom_frontiers[block_name].add(successor)
                else:
                    # if it is strictly dominated, add its successors to the check list
                    check_list.extend(self.blocks[successor].succs)
                seen.add(successor)
        return dom_frontiers


    def insert_phi_nodes(self):
        if len(self.blocks) <= 1:
            print(f"Cannot be any phi nodes in a program containing only {len(self.blocks)} blocks")
            return
        for v in self.vars:
            new_def_blocks = set()
            for block in self.defs[v]:
                for block_inner in self.dominance_frontiers[block]:
                    if v in self.blocks[block_inner].phi_nodes:
                        self.blocks[block_inner].phi_nodes[v].sources[block] = v
                    else:
                        self.blocks[block_inner].phi_nodes[v] = (PhiNode(v, {block: v}))
                new_def_blocks.update(self.dominance_frontiers[block])
            self.defs[v].update(new_def_blocks)
            new_def_blocks = set()
            while len(new_def_blocks) > 0:
                block = new_def_blocks.pop()
                for block_inner in self.dominance_frontiers[block]:
                    if v in self.blocks[block_inner].phi_nodes:
                        self.blocks[block_inner].phi_nodes[v].sources[block] = v
                    else:
                        self.blocks[block_inner].phi_nodes[v] = (PhiNode(v, {block: v}))
                        new_def_blocks.add(block_inner)
                        self.defs[v].add(block_inner)
        return

    def compute_liveness(self, do_time = False):
        # Initialize the blocks
        for block in self.blocks.values():
            block.compute_used_and_defined_vars(None)
            block.live_out = set()
            block.live_in = set()
        # Create worklist
        worklist = copy.deepcopy(self.terminating_blocks)
        start_time = time.time()
        while True:
            # Continue until no changes are made
            changed = False
            # This prevents infinite loops
            blocks_seen = set()
            while len(worklist) > 0:
                # Work through blocks in reverse-post order
                block = self.blocks[worklist.pop()]
                old_live_in = copy.deepcopy(block.live_in)
                old_live_out = copy.deepcopy(block.live_out)
                blocks_seen.add(block.name())
                # Compute live out variables
                for succ in block.succs:
                    block.live_out = block.live_out.union(self.blocks[succ].live_in)
                # Compute live in variables
                block.live_in = block.used_vars.union(block.live_out - block.defined_vars)
                # Check if changes were made
                if old_live_in != block.live_in or old_live_out != block.live_out:
                    changed = True
                # Add predecessors to worklist
                for pred in block.preds:
                    # This prevents infinite loops
                    if pred not in blocks_seen:
                        worklist.add(pred)
            if not changed:
                break
        end_time = time.time() 
        if do_time:
            print("Computing Liveness Time taken: ", end_time - start_time)
        return

    def is_phi(self, instr: dict):
        return instr['op'] == 'phi'
    
    def get_new_name(self, var: str):
        new_name = var + "." + str(self.counters[var])
        self.counters[var] += 1
        return new_name
    
    def get_current_name(self, var: str):
        res = peek(self.var_stack[var])
        if res is None:
            return var + ".0"
        return res

    def rename(self, block: blocks.Block, recursive_depth = 0, source_name = None):
        old_stacks = dict()
        for key, _ in self.var_stack.items():
            old_stacks[key] = copy.deepcopy(self.var_stack[key])
        for var, node in block.phi_nodes.items():
            if source_name in node.sources.keys():
                value = node.sources[source_name]
                new_args = dict()
                nval = self.get_current_name(get_base(value))
                node.sources[source_name] = nval
                new_dest = self.get_new_name(var)
                self.var_stack[var].append(new_dest)
                node.var = new_dest
            
        for instr in block.instrs:
            if 'args' in instr:
                new_args = []
                for arg in instr['args']:
                    new_arg = self.get_current_name(get_base(arg))
                    new_args.append(new_arg)
                instr['args'] = new_args
            if 'dest' in instr:
                d_arg = get_base(instr['dest'])
                new_dest = self.get_new_name(d_arg)
                self.var_stack[d_arg].append(new_dest)
                instr['dest'] = new_dest
        for s in block.succs:
            for instr in self.blocks[s].instrs:
                if self.is_phi(instr):
                    # For a phi node, all arguments should have the same base
                    curr_name = self.get_current_name(instr['base'])
                    if curr_name not in instr['args']:
                        instr['args'].append(curr_name)
                        instr['labels'].append(block.name())

        ext_idoms = self.get_idominated_blocks(block)
        for idom in ext_idoms:
            self.rename(self.blocks[idom], recursive_depth + 1, block.name())
            self.rename(self.blocks[idom], recursive_depth + 1, block.name())

        for key, _ in self.var_stack.items():
            self.var_stack[key] = copy.deepcopy(old_stacks[key])

    def get_idominated_blocks(self, block: blocks.Block):
        ext_idoms = set()
        for block_i in self.blocks.values():
            if self.immediate_dominators[block_i.name()] is not None and block.name() in self.immediate_dominators[block_i.name()]:
                ext_idoms.add(block_i.name())
        return ext_idoms

    def convert_to_SSA(self):
        self.insert_phi_nodes()
        self.rename(self.blocks[".start"])

    def build_interference_graph(self):
        graph = Graph([], [])
        for var in self.vars:
            vertex = Vertex(var)
            graph.add_vertex(vertex)
        for block in self.blocks.values():
            for var in block.in_vars:
                for var_inner in block.in_vars:
                    if var != var_inner:
                        if not graph.contains_edge(Vertex(var), Vertex(var_inner)):
                            graph.add_edge(Vertex(var), Vertex(var_inner))
        return graph
    
    def convert_to_riscv_instrs(self, outfile):
        print("Converting to RISC-V instructions")
        with open(outfile, 'w') as f:
            for block in self.blocks.values():
                if block.name() == ".start":
                    f.write("main:\n")
                    continue
                f.write("." + block.name() + ":\n")
                for instr in block.instrs:
                    op = ''
                    args = []
                    dest = ''
                    str_instr = ""
                    if 'op' in instr:
                        op = instr['op']
                        if op == 'const':
                            op = 'li'
                            args.append(str(instr['value']))
                        elif op == 'id':
                            op = 'mv'
                        elif op == 'jmp':
                            op = 'j'
                            args.append('.' + instr['labels'][0])
                        elif op == 'eq':
                            op = 'sub'
                    str_instr += op + " "
                if 'dest' in instr:
                    str_instr += instr['dest'] + ", "
                if 'args' in instr:
                    for arg in instr['args']:
                        args.append(arg)
                str_instr += ", ".join(args)
                if op == 'ret':
                    str_instr = "mv a0, " + instr['args'][0]
                    f.write('\t' + str_instr + "\n")
                    f.write('\tjr ra' + "\n")
                elif op == 'br':
                    op = 'beq'
                    args.append('zero')
                    args.append('.' + instr['labels'][0])
                    str_instr = op + " " + ", ".join(args)
                    f.write('\t' + str_instr + "\n")
                    f.write('\tj ' + instr['labels'][1] + "\n")
                else:
                    f.write('\t' + str_instr + "\n")

def peek(stack: list):
    if len(stack) == 0:
        return None
    return stack[-1]

def shift_left(stack: list):
    if len(stack) == 0:
        return []
    return stack[1:]

def build_interference_graph(cfg: CFG, do_time = False):
    start_time = time.time()
    cfg.compute_liveness()
    graph = Graph([], [])
    for var in cfg.vars:
        graph.add_vertex(Vertex(var))
    for block in cfg.blocks.values():
        for var in block.defined_vars:
            for var_inner in block.live_out:
                if var != var_inner:
                    e = Edge(Vertex(var), Vertex(var_inner))
                    if e not in graph.edges:
                        graph.add_edge(Vertex(var), Vertex(var_inner))
    end_time = time.time()
    if do_time:
        print("Interference Graph Generation Time Elapsed: ", end_time - start_time)
    return graph

def compute_reaching_defs(cfg: CFG):
    block_seen_count = dict()
    for block in cfg.blocks.values():
        block_seen_count[block.name()] = 0
    cfg.blocks['.start'].in_vars = set()
    cfg.blocks['.start'].out_vars = cfg.blocks['.start'].defined_vars
    worker_queue = set(cfg.blocks['.start'].succs)
    while len(worker_queue) > 0:
        block = worker_queue.pop()
        block_seen_count[block] += 1
        for pred in cfg.blocks[block].preds:
            cfg.blocks[block].in_vars = cfg.blocks[block].in_vars.union(cfg.blocks[pred].out_vars)
        cfg.blocks[block].out_vars = cfg.blocks[block].defined_vars.union(cfg.blocks[block].in_vars) - cfg.blocks[block].killed_vars
        for succ in cfg.blocks[block].succs:
            worker_queue.add(succ)
        if block_seen_count[block] > 100:
            break
    worker_queue = set(cfg.blocks['.start'].succs)
    while len(worker_queue) > 0:
        block = worker_queue.pop()
        block_seen_count[block] += 1
        for pred in cfg.blocks[block].preds:
            cfg.blocks[block].in_vars = cfg.blocks[block].in_vars.union(cfg.blocks[pred].out_vars)
        cfg.blocks[block].out_vars = cfg.blocks[block].defined_vars.union(cfg.blocks[block].in_vars) - cfg.blocks[block].killed_vars
        for succ in cfg.blocks[block].succs:
            worker_queue.add(succ)
        if block_seen_count[block] > 100:
            break
    return cfg

def min_reg_count(interference_graph: CFG):
    reg_count = 0
    max_block = "N/A"
    for block in interference_graph.blocks.values():
        unique_in_vars = 0
        seen = set()
        for var in block.in_vars:
            if get_base(var) not in seen:
                unique_in_vars += 1
                seen.add(get_base(var))
        unique_out_vars = 0
        seen = set()
        for var in block.out_vars:
            if get_base(var) not in seen:
                unique_out_vars += 1
                seen.add(get_base(var))
        if max(unique_in_vars, unique_out_vars) > reg_count:
            reg_count = max(unique_in_vars, unique_out_vars)
            max_block = block.name()
    return reg_count, max_block

def compute_live_intervals(cfg: CFG):
    cfg.compute_liveness()
    definitions = dict()
    last_use = dict()
    ordered_blocks = list(cfg.blocks.values())
    for block in cfg.blocks.values():
        idx = 0
        if block.name() != ".start":
            idx = int(block.name().split('l')[1])
        ordered_blocks[idx] = block
    idx = 0
    for block in ordered_blocks:
        for instr in block.instrs:
            if 'dest' in instr and instr['dest'] not in definitions:
                definitions[instr['dest']] = idx
            if 'args' in instr:
                for arg in instr['args']:
                    last_use[arg] = idx
            idx += 1
    return definitions, last_use, ordered_blocks


class Register:
    def __init__(self, var: str, start: int, end: int):
        self.var = var
        self.start = start
        self.end = end
        self.co_live_vars = set()
    
    def is_free(self):
        return self.var is None
    
    def when_free(self):
        return self.end
    
    def __str__(self):
        return f"Register(var={self.var}, start={self.start}, end={self.end})"
    
    def allocate(self, var: str, start: int, end: int):
        self.var = var
        self.start = start
        self.end = end
    
    def free(self):
        self.var = None
        self.start = -1
        self.end = -1
    
    def add_co_live_var(self, var: str):
        self.co_live_vars.add(var)
    
    def get_co_live_vars(self):
        return self.co_live_vars

class Vertex:
    def __init__(self, name: str):
        self.name = name
        self.co_live_vars = set()
        self.reg_assignment = None
        self.reg_idx = -1
    
    def is_same(self, other):
        return self.name == other.name
    
    def __eq__(self, other):
        return self.is_same(other) and self.co_live_vars == other.co_live_vars and self.reg_assignment == other.reg_assignment
    
    def __str__(self):
        return f"Vertex(name={self.name})"
    
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return f"Vertex(name={self.name})"
    
    def set_reg_idx(self, idx: int):
        self.reg_idx = idx
    
    def get_reg_idx(self):
        return self.reg_idx

class Edge:
    def __init__(self, u: Vertex, v: Vertex):
        self.u = u
        self.v = v
    
    def is_same(self, other):
        return (self.u.is_same(other.u) and self.v.is_same(other.v)) or (self.u.is_same(other.v) and self.v.is_same(other.u))
    
    def __eq__(self, other):
        return self.is_same(other)
    
    def __str__(self):
        return f"Edge(u={self.u.name}, v={self.v.name})"
    
    def __hash__(self):
        return hash(self.u.name ^ self.v.name)
    
    def __repr__(self):
        return f"Edge(u={self.u.name}, v={self.v.name})"

class Graph:
    def __init__(self, vertices: list, edges: list):
        self.vertices = vertices
        self.edges = edges

    def add_vertex(self, vertex: Vertex):
        self.vertices.append(vertex)
    
    def add_edge(self, u: Vertex, v: Vertex):
        self.edges.append(Edge(u, v))
    
    def contains_edge(self, u: Vertex, v: Vertex):
        return Edge(u, v) in self.edges or Edge(v, u) in self.edges
    
    def contains_edge_from_edge(self, edge: Edge):
        return edge in self.edges

    def __str__(self):
        string = ""
        for vertex in self.vertices:
            string += f"Vertex: {vertex.name} -> "
            string += "\n"
        string += "\n"
        for edge in self.edges:
            string += f"Edge: {edge.u.name} -> {edge.v.name}"
            string += "\n"
        return string
    
    def edges_from_vertex(self, vertex: Vertex):
        edges = []
        for edge in self.edges:
            if edge.u.is_same(vertex) or edge.v.is_same(vertex):
                edges.append(edge)
        return edges

    def contains_vertex_with_less_than_k_edges(self, k: int):
        for vertex in self.vertices:
            if len(self.edges_from_vertex(vertex)) < k:
                return vertex
        return None

    def remove_vertex(self, vertex: Vertex):
        self.vertices.remove(vertex)
        edges_to_remove = []
        for edge in self.edges:
            if edge.u.is_same(vertex) or edge.v.is_same(vertex):
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            self.edges.remove(edge)
        return edges_to_remove

    def remove_edge(self, edge: Edge):
        self.edges.remove(edge)

    def is_empty(self):
        return len(self.vertices) == 0 and len(self.edges) == 0
    
    def make_graph_mermaid(self):
        cfg = "graph TD\n"
        vertex_to_reg_idx = dict()
        for vertex in self.vertices:
            vertex_to_reg_idx[vertex.name] = vertex.get_reg_idx()
        for edge in self.edges:
            cfg += f"    {edge.u.name}:{str(vertex_to_reg_idx[edge.u.name])} --> {edge.v.name}:{str(vertex_to_reg_idx[edge.v.name])}\n"
        return cfg


def linear_scan_allocate_registers(cfg: CFG, reg_count: int, fname: str, spill_strategy = "longest_live_range"):
    # Linear scan register allocation
    definitions, last_use, ordered_blocks = compute_live_intervals(cfg)
    start_time = time.time()
    register_map = dict()
    free_registers = set()
    allocated_registers = set()
    memory_offloaded_vars = set()
    for i in range(reg_count):
        register_map[i] = Register(None, -1, -1)
        free_registers.add(i)

    instr_wise_reg_map = []
    var_to_reg_map = dict()

    current_instr = 0
    
    if cfg.func_args is not None:
        for arg in cfg.func_args:
            instr_wise_reg_map_inner = [str(i) for i in range(reg_count)]
            reg = free_registers.pop()
            var_to_reg_map[arg['name']] = reg
            register_map[reg].allocate(arg['name'], 0, last_use[arg['name']])
            allocated_registers.add(reg)
            for reg in allocated_registers:
                instr_wise_reg_map_inner[reg] += ": " + str(register_map[reg].var)
                var_to_reg_map[register_map[reg].var] = reg
            for reg in free_registers:
                instr_wise_reg_map_inner[reg] += ":  "

    for block in ordered_blocks:
        for instr in block.instrs:
            instr_wise_reg_map_inner = [str(i) for i in range(reg_count)]
            if 'dest' in instr:
                var = instr['dest']
                end = -1
                if var in var_to_reg_map:
                    continue
                if var in last_use:
                    end = last_use[var]
                if len(free_registers) == 0:
                    # Spill 
                    if spill_strategy == "longest_live_range":
                        last_free = -1
                        for reg in allocated_registers:
                            if register_map[reg].when_free() > last_free:
                                last_free = register_map[reg].when_free()
                                spill_reg = reg
                    else:
                        spill_reg = random.randint(0, reg_count - 1)
                    reg_old = register_map[spill_reg]
                    register_map[spill_reg].free()
                    memory_offloaded_vars.add(reg_old.var)
                    register_map[spill_reg].allocate(var, current_instr, end)
                else:   
                    regs_list = list(free_registers)
                    regs_list.sort()
                    reg_idx = regs_list[0]
                    free_registers.remove(reg_idx)
                    allocated_registers.add(reg_idx)
                    register_map[reg_idx].allocate(var, current_instr, end)
            for reg in copy.deepcopy(allocated_registers):
                if register_map[reg].when_free() == current_instr:
                    free_registers.add(reg)
                    allocated_registers.remove(reg)
                    register_map[reg].free()
            for reg in allocated_registers:
                instr_wise_reg_map_inner[reg] += ": " + str(register_map[reg].var)
                var_to_reg_map[register_map[reg].var] = reg
            for reg in free_registers:
                instr_wise_reg_map_inner[reg] += ":  "
            instr_wise_reg_map.append(instr_wise_reg_map_inner)
            current_instr += 1
    end_time = time.time()
    print(fname, reg_count, " Linear Scan Time Taken: ", end_time - start_time)
    print(fname, reg_count, " Linear Scan Number of spills: ", len(memory_offloaded_vars))
    
    # This is for visualizing the register allocation
    # for row in instr_wise_reg_map:
    #     string = ""
    #     for cell in row:
    #         if len(cell) > 6:
    #             string += cell + "\t"
    #         else:
    #             string += cell + "\t\t"
    #     print(string)
    # print()

    max_regs_in_use = 0
    for instr in instr_wise_reg_map:
        regs_in_use = 0
        for elem in instr:
            elem_clone = elem.strip()
            elem_clone =elem_clone.split(':')
            if elem_clone[1] != "":
                regs_in_use += 1
        if regs_in_use > max_regs_in_use:
            max_regs_in_use = regs_in_use
    print(fname, reg_count, " Linear Scan Maximum number of registers in use: ", max_regs_in_use)
    return instr_wise_reg_map, var_to_reg_map

def graph_coloring_allocate_registers(cfg: CFG, reg_count: int, fname: str):
    k = reg_count
    graph = build_interference_graph(cfg)

    start_time = time.time()
    S = set()
    G = copy.deepcopy(graph)
    stack = [] # Working Stack
    registers = [i for i in range(reg_count)]
    reg_alloc = dict()
    for v in G.vertices:
        reg_alloc[v.name] = None

    while not G.is_empty():
        v = G.contains_vertex_with_less_than_k_edges(k)
        color = True
        if v is None:
            v = G.vertices[0]
            color = False
        stack_line = (v, G.edges_from_vertex(v), color)
        stack.append(stack_line)
        G.remove_vertex(v)
    old_stack = copy.deepcopy(stack)
    
    S_old = copy.deepcopy(S)
    while True: 
        stack = copy.deepcopy(old_stack)
        while len(stack) > 0:
            v, edges, color = stack.pop()
            if color:
                for edge in edges:
                    G.add_edge(edge.u, edge.v)
                neighbor_regs = []
                for edge in edges:
                    if not v.is_same(edge.v) and reg_alloc[edge.v.name] is not None:
                        neighbor_regs.append(reg_alloc[edge.v.name])
                    if not v.is_same(edge.u) and reg_alloc[edge.u.name] is not None:
                        neighbor_regs.append(reg_alloc[edge.u.name])
                # Use the first available register
                for reg in registers:
                    if reg not in neighbor_regs:
                        reg_alloc[v.name] = reg
                        v.set_reg_idx(reg)
                        G.add_vertex(v)
                        break
            else: # Color is false, indicates a spill
                allocated_neighbors = 0
                neighbor_regs = []
                for edge in edges: # Optimistically color
                    if not v.is_same(edge.u) and reg_alloc[edge.u.name] is not None:
                        neighbor_regs.append(reg_alloc[edge.u.name])
                        allocated_neighbors += 1
                    elif not v.is_same(edge.v) and reg_alloc[edge.v.name] is not None:
                        neighbor_regs.append(reg_alloc[edge.v.name])
                        allocated_neighbors += 1
                if allocated_neighbors < k:
                    # Allocate a register anyway
                    for edge in edges:
                        G.add_edge(edge.u, edge.v)
                    for reg in registers:
                        if reg not in neighbor_regs:
                            reg_alloc[v.name] = reg
                            v.set_reg_idx(reg)
                            print(v.name, reg)
                            G.add_vertex(v)
                            break
                else:
                    # Spill
                    reg_alloc[v.name] = None
                    S.add(v)
        if S == S_old:
            break
        S_old = copy.deepcopy(S)
    end_time = time.time()
    print(fname, reg_count, " Graph Coloring Time Taken: ", end_time - start_time)
    print(fname, reg_count, " Graph Coloring Number of spills: ", len(S))
    regs_in_use = set()
    for reg in reg_alloc.values():
        if reg is not None:
            regs_in_use.add(reg)
    print(fname, reg_count, " Graph Coloring Number of registers in use: ", len(regs_in_use))

    #print(G.make_graph_mermaid())

    return reg_alloc, S

def verify_register_allocation(cfg: CFG, reg_alloc: dict, spilled_vars: set):
    graph = build_interference_graph(cfg)
    for vertex in graph.vertices:
        if vertex.name in reg_alloc and reg_alloc[vertex.name] is not None:
            reg = reg_alloc[vertex.name]
            for edge in graph.edges_from_vertex(vertex):
                if edge.u.name != vertex.name:
                    if reg_alloc[edge.u.name] == reg:
                        print("A Register conflict at ", vertex.name, " and ", edge.u.name)
                        return False
                elif edge.v.name != vertex.name:
                    if reg_alloc[edge.v.name] == reg:
                        print("B Register conflict at ", vertex.name, " and ", edge.v.name)
                        return False
    return True

class RegisterSpecs:
    def __init__(self, arg_regs: list, ret_regs: list, gp_regs: list, special_regs: list):
        self.arg_regs = arg_regs
        self.ret_regs = ret_regs
        self.gp_regs = gp_regs
        self.special_regs = special_regs


def reg_alloc_to_instrs(cfg: CFG, reg_alloc: dict, specs: RegisterSpecs):
    for block in cfg.blocks.values():
        for instr in block.instrs:
            if 'dest' in instr:
                if instr['dest'] in reg_alloc:
                    if reg_alloc[instr['dest']] == None:
                        dest_reg = "mr"
                    else:
                        dest_reg = specs.gp_regs[reg_alloc[instr['dest']]]
                    instr['dest'] = dest_reg
            if 'args' in instr:
                for i in range(len(instr['args'])):
                    if instr['args'][i] in reg_alloc:
                        if reg_alloc[instr['args'][i]] == None:
                            arg_reg = "mr"
                        else:
                            arg_reg = specs.gp_regs[reg_alloc[instr['args'][i]]]
                        instr['args'][i] = arg_reg
            # TODO: Handle memory loads
    return cfg

if __name__ == '__main__': 
    import sys

    if len(sys.argv) != 2:
        print("Usage: python cfg.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as file:
        program = utils.read_json_file(file)

    for func in program['functions']:
        fn_blocks = blocks.form_blocks(func)
        for block in fn_blocks.values():
            block.reinitialize_vars()
        cfg = CFG(fn_blocks, (func['args'] if 'args' in func else None))
        cfg.compute_liveness()

        graph = build_interference_graph(cfg)
        #print(graph)
        fname_prefix = filename.split('-')[0] + "_" + func['name']

        n_regs = 10
        res, allocated_registers = linear_scan_allocate_registers(cfg, n_regs, fname_prefix)
        print()
        regs, spilled_vars = graph_coloring_allocate_registers(cfg, n_regs, fname_prefix)
        if not verify_register_allocation(cfg, regs, spilled_vars):
            print("1 REGISTER ALLOCATION HAS CONFLICTS")
            sys.exit(1)
        print()
        n_regs = 7
        res, allocated_registers = linear_scan_allocate_registers(cfg, n_regs, fname_prefix)
        print()
        regs, spilled_vars = graph_coloring_allocate_registers(cfg, n_regs, fname_prefix)
        if not verify_register_allocation(cfg, regs, spilled_vars):
            print("2 REGISTER ALLOCATION HAS CONFLICTS")
            sys.exit(1)
        print()
        n_regs = 5
        res, allocated_registers = linear_scan_allocate_registers(cfg, n_regs, fname_prefix)
        print()
        regs, spilled_vars = graph_coloring_allocate_registers(cfg, n_regs, fname_prefix)
        if not verify_register_allocation(cfg, regs, spilled_vars):
            print("3 REGISTER ALLOCATION HAS CONFLICTS")
            sys.exit(1)

        arg_regs = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']
        ret_regs = ['ra']
        gp_regs = ['t0', 't1', 't2', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 't3', 't4', 't5', 't6']
        special_regs = ['fp', 'sp', 'gp', 'tp', 'zero']
        specs = RegisterSpecs(arg_regs, ret_regs, gp_regs, special_regs)
        cfg = reg_alloc_to_instrs(cfg, regs, specs)
        cfg.convert_to_riscv_instrs(fname_prefix + ".s")

        print()