# pdb_utils
## Installation
1. Activate a virtual environment which you want to install pdb_utils into.
```sh
conda activate some-env
```

2. Clone this repository
```sh
git clone https://github.com/kttn8769/pdb_utils.git
cd pdb_utils
```

3. Run dependency check
```sh
python ./check_dependencies.py
```

* If missing/conflicting dependencies are found, prepare the required dependencies with conda.

4. Install pdb_utils
```sh
pip install .
```

---

# Examples
* To see the help document of each program, invoke the program with --help flag. e.g.  `pu_edit_pdb --help`

## pu_pdb_edit
* Replace HSD to HIS

```
pu_edit_pdb --i in.pdb --o out.pdb --procs hsd2his
```

## pu_find_missing_sidechains
* Find sidechain-missing residues in a PDB file.

```
pu_find_missing_sidechains --i in.pdb --chain A
```
