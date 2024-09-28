import json
import sys
from collections import namedtuple

# Represents the operation and its arguments
Value = namedtuple('Value', ['op', 'args'])

class ImprovedLVN:
    def __init__(self):
        self.var2num = {}  # Maps variables to their value numbers
        self.value2num = {}  # Maps operations to value numbers
        self.num2var = {}  # Maps value numbers to variable names
        self.next_vn = 0  # Counter for the next value number
        self.var_origins = {}  # Maps variables to their original source

    def fresh_value_number(self):
        """Generate a fresh value number."""
        vn = self.next_vn
        self.next_vn += 1
        return vn

    def canonicalize(self, value):
        """Canonicalize commutative operations like addition and multiplication."""
        if value.op in ('add', 'mul'):
            return Value(value.op, tuple(sorted(value.args)))
        return value

    def get_canonical_var(self, var):
        """Get the canonical variable name."""
        return self.var_origins.get(var, var)

    def process_block(self, block):
        """Perform LVN on a single block."""
        new_block = []
        for instr in block:
            if 'dest' not in instr:
                new_block.append(instr)
                continue

            if 'args' in instr:
                # Fetch canonical variable names for arguments
                canon_args = [self.get_canonical_var(arg) for arg in instr['args']]
                
                if instr['op'] == 'id':
                    # For 'id' operations, directly use the canonical source
                    self.var_origins[instr['dest']] = canon_args[0]
                    self.var2num[instr['dest']] = self.var2num[canon_args[0]]
                    new_instr = {'op': 'id', 'dest': instr['dest'], 'args': canon_args}
                else:
                    # Create a value for the current instruction
                    val = self.canonicalize(Value(instr['op'], tuple(canon_args)))

                    if val in self.value2num:
                        # It's redundant; use the previous result
                        vn = self.value2num[val]
                        canonical_var = self.get_canonical_var(self.num2var[vn])
                        self.var_origins[instr['dest']] = canonical_var
                        new_instr = {'op': 'id', 'dest': instr['dest'], 'args': [canonical_var]}
                    else:
                        # It's new; assign a fresh value number
                        vn = self.fresh_value_number()
                        self.value2num[val] = vn
                        self.num2var[vn] = instr['dest']
                        self.var_origins[instr['dest']] = instr['dest']
                        new_instr = {**instr, 'args': canon_args}

                self.var2num[instr['dest']] = vn
            else:
                # Handle constant or operations without arguments
                vn = self.fresh_value_number()
                self.var2num[instr['dest']] = vn
                self.num2var[vn] = instr['dest']
                self.var_origins[instr['dest']] = instr['dest']
                new_instr = instr

            new_block.append(new_instr)

        return new_block

    def run_lvn(self, bril_program):
        """Run LVN on the entire program."""
        for func in bril_program['functions']:
            func['instrs'] = self.process_block(func['instrs'])
        return bril_program

if __name__ == '__main__':
    # Read input JSON from stdin
    bril_program = json.load(sys.stdin)
    # Initialize the LVN optimizer
    optimizer = ImprovedLVN()
    # Run LVN optimization
    optimized_program = optimizer.run_lvn(bril_program)
    # Output the optimized program
    json.dump(optimized_program, sys.stdout, indent=2)