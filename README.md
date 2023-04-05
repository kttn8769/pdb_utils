# pdb_utils
Only Python3 is supported. If Python2 is used, a SyntaxError will be raised.

Use --help flag to see each program usage.

```
python3 <path to the pdb_utils directory>/<name of program> --help
```

---

# Examples
## pu_pdb_edit.py
* Replace HSD to HIS

```
python3 <path to the pdb_utils directory>/pu_edit_pdb.py --i in.pdb --o out.pdb --procs hsd2his
```

## pu_find_missing_sidechains.py
* Find sidechain-missing residues in a PDB file.
* Requires
  * Biopython

```
python3 <path to the pdb_utils directory>/pu_find_missing_sidechains.py --i in.pdb --chain A
```
