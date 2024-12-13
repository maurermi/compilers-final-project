import sys
from utils import read_json_file, get_base, get_order
import copy

class PhiNode:
    def __init__(self, var: str, sources: dict):
        self.var = var
        self.sources = sources # key is the predecessor block, value is the variable

    def __str__(self):
        return f"PhiNode: {self.var} = {self.sources}"
    
    def __repr__(self):
        return f"PhiNode: {self.var} = {self.sources}"
    
    def __eq__(self, other):
        return self.var == other
    
    def __hash__(self):
        return hash(self.var)
    
    def useful(self):
        return len(self.sources) > 1

class Block:
    def __init__(self, instrs: list, id, preds: set, succs: set):
        self.instrs = instrs
        self.id = id
        self.preds = preds
        self.succs = succs
        self.used_vars = set()
        self.defined_vars = set()
        self.compute_used_and_defined_vars()
        self.out_vars = set()
        self.in_vars = set()
        self.in_vars = self.compute_in_vars()
        self.killed_vars = set()
        self.killed_vars = self.compute_killed_vars()
        self.live_vars_map = dict()
        self.live_out = set()
        self.live_in = set()
        self.phi_nodes = dict()
    
    def __str__(self):
        result = f"ID: {self.id}\nInstructions: \n"
        result += f"Phi nodes: \n"
        for phi, node in self.phi_nodes.items():
            result += f"{phi}\n"
        for instr in self.instrs:
            # if 'args' in instr:
            #     result += f"{id(instr['args'])}\n"
            result += f"{instr}\n"
        result += f"Predecessors: {self.preds}\nSuccessors: {self.succs}\n"
        return result
    
    def name(self):
        return self.id
    
    def add_pred(self, pred):
        self.preds.add(pred)
    
    def add_succ(self, succ):
        self.succs.add(succ)
    
    def add_in_var(self, var):
        self.in_vars.add(var)
    
    def add_out_var(self, var):
        self.out_vars.add(var)
    
    def compute_used_vars(self):
        for instr in self.instrs:
            if 'args' in instr:
                self.used_vars.update(instr['args'])
        return self.used_vars
    
    def compute_defined_vars(self):
        for instr in self.instrs:
            if 'dest' in instr:
                self.defined_vars.add(instr['dest'])
        return self.defined_vars
    
    def compute_used_and_defined_vars(self, func_args = None):
        self.defined_vars = set()
        self.used_vars = set()
        x = False
        if func_args is not None:
            if self.id == ".start":
                for arg in func_args:
                    self.defined_vars.add(arg['name'])
                    x = True
        for instr in self.instrs:
            if 'args' in instr:
                for arg in instr['args']:
                    if arg not in self.defined_vars:
                        self.used_vars.add(arg)
            if 'dest' in instr:
                self.defined_vars.add(instr['dest'])
        return self.used_vars, self.defined_vars
    
    def compute_in_vars(self):
        if len(self.preds) == 0:
            return set()
        self.in_vars = self.used_vars - self.defined_vars
        rhs_vars = copy.deepcopy(self.out_vars)
        for var in self.out_vars:
            if var in self.defined_vars:
                rhs_vars.remove(var)
        self.in_vars.update(rhs_vars)
        return self.in_vars
    
    def set_out_vars(self, out_vars):
        self.out_vars = out_vars
    
    def compute_out_vars(self):
        if len(self.succs) == 0:
            return set()
        self.out_vars = self.in_vars.union(self.defined_vars) - self.killed_vars
        return self.out_vars
    
    def compute_killed_vars(self):
        trimmed_def_vars = [get_base(var) for var in self.defined_vars]
        for var in self.in_vars:
            if get_base(var) in trimmed_def_vars:
                self.killed_vars.add(var)

        return self.killed_vars
    
    def compute_live_vars(self):
        current_live_vars = copy.deepcopy(self.out_vars)
        for idx, instr in enumerate(reversed(self.instrs)):
            live_vars = copy.deepcopy(current_live_vars) 
            if 'dest' in instr:
                live_vars -= {instr['dest']} # This should just remove things that match the base of the dest
            if 'args' in instr:
                live_vars |= set(instr['args'])
            self.live_vars_map[idx] = list(live_vars)
            current_live_vars = live_vars
        # live_vars['block_in'] = current_live
        return self.live_vars_map
    
    def reinitialize_vars(self):
        self.used_vars = set()
        self.defined_vars = set()
        self.in_vars = set()
        self.out_vars = set()
        self.killed_vars = set()
        self.used_vars = self.compute_used_vars()
        self.defined_vars = self.compute_defined_vars()
        self.in_vars = self.compute_in_vars()
        self.out_vars = self.compute_out_vars()
        self.killed_vars = self.compute_killed_vars()
    
def form_blocks(program: dict):
    terminators = {'br', 'ret', 'jmp'}
    blocks = dict()

    current_block_id = ".start" # Should this be ".start" instead?
    current_block = Block([], current_block_id, set(), set())
    last_term = False
    for idx, instr in enumerate(program['instrs']):
        if 'label' not in instr:
            # if there is no current block, we have not properly created one beforehand -- this should never happen if this program is correct
            if not current_block:
                print("ERROR: No current block")
                exit(1)
            # append the instruction like any other
            current_block.instrs.append(instr)

        if 'label' in instr: # we may have a fallthrough
            label = instr['label']
            if current_block:
                if not last_term: # i.e. if this is a fallthrough, then this new block is a successor of the current block
                    current_block.succs = set([instr['label']])
                blocks.update({current_block_id: current_block}) # regardless add the current block to the list

            # update the current block
            if label in blocks:
                # if the label already exists, we update the current block to this one
                current_block = blocks[label]
            else:
                current_block = Block([instr], instr['label'], set([current_block_id]), set())
            if not last_term: # if the last block was a fallthrough, then the last block is a predecessor
                # it's possible that this is a new label, so we check and update accordingly
                if label not in blocks:
                    new_block = Block([], label, set(), set())
                    blocks.update({label: new_block})
                blocks[label].preds.add(current_block_id)
                current_block = blocks[label]
            # update the current block id to match this new block
            current_block_id = instr['label']

        if idx == len(program['instrs']) - 1: # this is the last instruction in the program
            if not current_block:
                exit(1)
            # this is the last instruction we will handle regardless of whether the next is a terminator
            blocks.update({current_block_id: current_block})
            break # exit the loop
        elif 'op' in instr and instr['op'] in terminators:
            # we have a terminator instruction
            op = instr['op']
            if op == 'br':
                # if there is a branch, there are two possible successors of this block
                current_block.succs.add(instr['labels'][0])
                current_block.succs.add(instr['labels'][1])

                # also update the 'preds' of the successor blocks or create these blocks if they are new to us
                if instr['labels'][0] in blocks:
                    blocks[instr['labels'][0]].preds.add(current_block_id)
                else:
                    new_block = Block([], instr['labels'][0], set([current_block_id]), set())
                    blocks.update({instr['labels'][0]: new_block})
                
                if instr['labels'][1] in blocks:
                    blocks[instr['labels'][1]].preds.add(current_block_id)
                else:
                    new_block = Block([], instr['labels'][1], set([current_block_id]), set())
                    blocks.update({instr['labels'][1]: new_block})

            elif op == 'jmp':
                # if there is a jump, there is only one possible successor of this block
                current_block.succs.add(instr['labels'][0])
                if instr['labels'][0] in blocks:
                    blocks[instr['labels'][0]].preds.add(current_block_id)
                else:
                    # NB: hanged the below line to create a block with no instructions, instead of one containing `instr`
                    new_block = Block([], instr['labels'][0], set([current_block_id]), set())
                    blocks.update({instr['labels'][0]: new_block})

            # if there is a return, it is to another function, so we ignore this as the scope changes
            blocks.update({current_block_id: current_block})
            # no matter what, we expect a label after this instr, so this current block will get replaced
            current_block = None
            last_term = True # this is so we don't consider the next instruction as a fallthrough
        elif last_term:
            last_term = False
    return blocks

def flatten_blocks(blocks):
    instrs = []
    for block in blocks:
        instrs += block
    return instrs

if __name__ == '__main__':
    form_blocks(read_json_file(sys.stdin))