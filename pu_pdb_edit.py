'''pu_pdb_edit.py - A processing script for PDB files.

Processings can be specified by --procs option with space-separeted list of processings.
Available processing are:
\thsd2his : Replace every HSD (delta-protonated HIS) atom to HIS.
'''

import sys
import os
import copy
import argparse


def process_hsd2his(inlines, verbose=True):
    outlines = []
    for il in inlines:
        if (il[:6] == 'HETATM' or il[:6] == 'ATOM  ')  and il[17:20] == 'HSD':
            ol = 'ATOM  ' + il[6:17] + 'HIS' + il[20:]
            if verbose:
                print('< ' + il, end='')
                print('> ' + ol)
        else:
            ol = il
        outlines.append(ol)
    return outlines


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__
    )
    parser.add_argument('--i', required=True, type=str, help='Input PDB file.')
    parser.add_argument('--o', required=True, type=str, help='Output PDB file.')
    parser.add_argument('--procs', nargs='+', type=str, help='Space-separeted list of the desired processes.')
    parser.add_argument('--silent', action='store_true', help='Silence verbose outputs.')
    parser.add_argument('--overwrite', action='store_true', help='Allow overwritng the output file.')

    args = parser.parse_args()

    print('##### Command #####\n\t' + ' '.join(sys.argv))
    args_print_str = '##### Input parameters #####\n'
    for opt, val in vars(args).items():
        args_print_str += '\t{} : {}\n'.format(opt, val)
    print(args_print_str)
    return args


PROC_LIST = {
    'hsd2his': process_hsd2his
}


def main():
    args = parse_args()

    verbose = not args.silent

    if len(args.procs) == 0:
        print('No proc is specified.')
        sys.exit()

    assert os.path.exists(args.i), f'No such file named {args.i}.'
    if os.path.exists(args.o):
        if not args.overwrite:
            raise FileExistsError(f'Output file {args.o} already exists.')

    with open(args.i, 'r') as f:
        inlines = f.readlines()

    lines = copy.deepcopy(inlines)

    for proc_name in args.procs:
        if proc_name in PROC_LIST.keys():
            proc = PROC_LIST[proc_name]
            lines = proc(lines, verbose)
        else:
            print(f'Process name {proc_name} is not available.')

    if inlines == lines:
        print(f'No processing was performed.')
    else:
        with open(args.o, 'w') as f:
            f.writelines(lines)


if __name__ == '__main__':
    main()
