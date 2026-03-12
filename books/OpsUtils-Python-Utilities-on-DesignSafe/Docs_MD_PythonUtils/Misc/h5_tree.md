# h5_tree()
***Compact HDF5 Structure Viewer***

*h5_tree()* prints a **compact, depth-limited tree** of the contents of an open HDF5 file (or group), showing **groups** and **datasets**, and (for datasets) the **shape** and **dtype**.

It is useful for quickly exploring unfamiliar *.hdf5* files without loading large datasets into memory.

---

## Function

```python
def h5_tree(h5: h5py.File, max_items: int = 500, max_depth: int = 6):
    ...
```

---

## Parameters

* ***h5*** (*h5py.File* or *h5py.Group*)
  An **open** HDF5 handle (typically returned by *h5py.File(...)*).
  You can also pass an HDF5 **group** (e.g., *h5["/some/group"]*) to print a subtree.

* ***max_items*** (*int*, default: *500*)
  Hard cap on the number of printed entries (groups + datasets).
  When reached, the traversal stops and prints:
  *... (stopped: max_items reached)*

* ***max_depth*** (*int*, default: *6*)
  Maximum recursion depth to explore.

  * Depth starts at *0* for the root handle you pass in.
  * When *depth > max_depth*, traversal stops descending further.

---

## Output Format

Each entry is printed on its own line:

* **Group**

  ```
  /path/to/group  [Group]
  ```

* **Dataset**

  ```
  /path/to/dataset  [Dataset] shape=(...) dtype=...
  ```

At the beginning it prints a header:

```
Tree (max_items=..., max_depth=...):
```

---

## Examples

### 1) Print the top-level tree of a file

```python
import h5py

with h5py.File("myfile.hdf5", "r") as h5:
    h5_tree(h5)
```

### 2) Limit depth (quick high-level overview)

```python
with h5py.File("myfile.hdf5", "r") as h5:
    h5_tree(h5, max_depth=2)
```

### 3) Limit printed items (avoid very large trees)

```python
with h5py.File("myfile.hdf5", "r") as h5:
    h5_tree(h5, max_items=100)
```

### 4) Print only a subtree (start from a group)

```python
with h5py.File("myfile.hdf5", "r") as h5:
    h5_tree(h5["/NGAWest2"], max_depth=4)
```

---

## Notes and Behavior

* **No data is read** from datasets. Only metadata (dataset type, shape, dtype) is accessed.
* Traversal order follows *g.keys()* (HDF5 group key order as exposed by *h5py*).
* The tree is **printed** (side effect). The function does not return a value.

---

## Common Use Cases

* Discovering dataset paths to use later (e.g., *h5["/path/to/dataset"]*)
* Checking where large arrays live and what their shapes/dtypes are
* Verifying expected file structure in pipelines and batch jobs



#### Files
You can find these files in Community Data.

```{dropdown} get_now_unix.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/h5_tree.py
:language: none
```

