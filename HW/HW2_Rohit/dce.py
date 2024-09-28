import sys
import json
import itertools

TERMINATORS = 'br', 'jmp', 'ret'

def myCFG(instrs):
    cur_block = []
    for instr in instrs:
        if 'op' in instr:
            cur_block.append(instr)
            if instr['op'] in TERMINATORS:
                yield cur_block
                cur_block = []
        else:
            if cur_block:
                yield cur_block
            cur_block = [instr]

    if cur_block:
        yield cur_block

def remove_reassigned(func):
    while True:
        blocks = list(myCFG(func['instrs']))
        flag = False
        
        for block in blocks:
            last_def = {}
            to_drop = set()
            for i, instr in enumerate(block):
                for var in instr.get('args', []):
                    if var in last_def:
                        del last_def[var]

                if 'dest' in instr:
                    dest = instr['dest']
                    if dest in last_def:
                        to_drop.add(last_def[dest])
                    last_def[dest] = i

            new_block = [instr for i, instr in enumerate(block)
                        if i not in to_drop]
            flag |= len(new_block) != len(block)
            block[:] = new_block

        func['instrs'] = list(itertools.chain(*blocks))
        if flag:
            break
    


def main():
    bril = json.load(sys.stdin)
    for func in bril['functions']:
        remove_reassigned(func)
    json.dump(bril, sys.stdout, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
