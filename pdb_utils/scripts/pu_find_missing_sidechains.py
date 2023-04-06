import sys
import argparse
from Bio.PDB import PDBParser, is_aa


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )
    parser.add_argument('--i', type=str, required=True, help='Input PDB file.')
    parser.add_argument('--chain', type=str, default=None, help='Chain ID to inspect. By default inspecting all the chains.')
    args = parser.parse_args()

    print('##### Command #####\n\t' + ' '.join(sys.argv))
    args_print_str = '##### Input parameters #####\n'
    for opt, val in vars(args).items():
        args_print_str += '\t{} : {}\n'.format(opt, val)
    print(args_print_str)
    return args


def find_missing_sidechains(structure, target_chain):
    missing_sidechains = []
    target_chain_found = False

    for model in structure:
        for chain in model:
            if target_chain is not None:
                if chain.id != target_chain:
                    continue
                else:
                    target_chain_found = True

            for residue in chain:
                if not is_aa(residue):
                    continue

                res_name = residue.get_resname()
                atoms = set(atom.get_name() for atom in residue)

                # Check for missing sidechain atoms
                if res_name not in ["GLY", "ALA"]:
                    if "CB" in atoms:
                        # Check for other sidechain atoms
                        sidechain_atoms = [atom.get_name() for atom in residue if atom.get_name() not in ['N', 'CA', 'C', 'O']]
                        if len(sidechain_atoms) == 1:  # Only CB is present
                            missing_sidechains.append((chain.id, residue.id[1], res_name))
                    else:
                        missing_sidechains.append((chain.id, residue.id[1], res_name))
                elif res_name == "ALA" and not "CB" in atoms:
                    missing_sidechains.append((chain.id, residue.id[1], res_name))

    if target_chain is not None and not target_chain_found:
        sys.exit(f'Target chain {target_chain} was not found in the given PDB file!')

    return missing_sidechains


def _main(infile, target_chain):
    parser = PDBParser()
    structure = parser.get_structure('PDB', infile)
    missing_sidechains = find_missing_sidechains(structure, target_chain=target_chain)
    if len(missing_sidechains) == 0:
        print('No missing sidechain was found.')
    else:
        print('Missing sidechains:')
        for (chain, resid, resname) in missing_sidechains:
            print(f'Chain {chain} , ResID {resid:5d} , ResName {resname}')


def main():
    args = parse_args()
    _main(args.i, args.chain)


if __name__ == '__main__':
    main()
