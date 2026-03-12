# generate_task_commands()
***Generating PyLauncher Task Commands for Parameter Sweeps***

This utility provides a **general, reusable way to generate PyLauncher tasklists** (for example, a `runsList.txt` file) by expanding a single command template into **all combinations of parameter values**.

Instead of manually writing dozens or hundreds of nearly identical command lines, you define:

* **one base command**, and
* **a dictionary of parameters to sweep**,

and the utility produces **one shell command per parameter combination**, ready to be executed by PyLauncher.

---

## Why This Utility Exists

Large parametric studies are common in HPC workflows, but manually managing tasklists is:

* error-prone,
* hard to scale, and
* difficult to maintain.

This utility:

* keeps sweeps **explicit and readable**,
* guarantees **collision-free task generation**, and
* integrates cleanly with **SLURM + PyLauncher + Tapis-style workflows**.

---

## Function Overview

```python
generate_task_commands(base_command, sweep, *, placeholder_style="token")
```

### Purpose

Expand a command template into a list of fully resolved shell commands, one for each combination of sweep parameters.

---

## Parameters

### `base_command : str`

A command template containing **placeholders** for parameters to be swept.

Example:

```text
python3 -u simulate.py --alpha ALPHA --beta BETA --gamma GAMMA --output "$WORK/sweep_$SLURM_JOB_ID/line_$LAUNCHER_JID/slot_$LAUNCHER_TSK_ID"
```

The placeholders (`ALPHA`, `BETA`, `GAMMA`) must match the keys in the `sweep` dictionary.

Environment variables such as `$WORK`, `$SLURM_JOB_ID`, and `$LAUNCHER_TSK_ID` are intentionally **left unresolved** here and will be expanded by the shell at runtime.

---

### `sweep : Mapping[str, Sequence[Any]]`

A dictionary defining the parameter sweep.

Each key corresponds to a placeholder in `base_command`, and each value is a sequence of values to sweep over.

Example:

```python
{
    "ALPHA": [0.3, 0.5, 3.7],
    "BETA": [1.1, 2, 3],
    "GAMMA": ["a", "b", "c"],
}
```

All combinations are generated using a Cartesian product.

---

### `placeholder_style : {"token", "braces"}, optional`

Controls how placeholders are written in `base_command`.

* `"token"` (default):
  Placeholders appear as bare tokens:

  ```text
  --alpha ALPHA
  ```

* `"braces"`:
  Placeholders appear inside braces:

  ```text
  --alpha {ALPHA}
  ```

The brace style can be safer if parameter names might overlap with other text.

---

## Returns

### `List[str]`

A list of fully expanded command strings.

Each element corresponds to **one unique combination** of sweep parameters, in deterministic order based on the insertion order of the `sweep` dictionary.

---

## Example Usage

```python
inputFilename = "simulate.py"

base_command = (
    f'python3 -u {inputFilename} '
    f'--alpha ALPHA --beta BETA --gamma GAMMA '
    f'--output "$WORK/sweep_$SLURM_JOB_ID/line_$LAUNCHER_JID/slot_$LAUNCHER_TSK_ID"'
)

sweep_params = {
    "ALPHA": [0.3, 0.5],
    "BETA": [1, 2],
    "GAMMA": ["a", "b"],
}

commands = generate_task_commands(base_command, sweep_params)

for cmd in commands:
    print(cmd)
```

This produces one command per parameter combination, suitable for use in a PyLauncher tasklist.

---

## Writing a PyLauncher Tasklist

The companion helper function can write the generated commands directly to a file:

```python
write_tasklist(commands, "runsList.txt")
```

Each command is written on its own line, matching PyLauncher’s expected format.

---

## Notes on Environment Variables and Output Paths

### Environment Variables

Variables such as:

* `$WORK`
* `$SLURM_JOB_ID`
* `$LAUNCHER_JID`
* `$LAUNCHER_TSK_ID`

are **not interpreted by Python**. They are expanded by the **shell at runtime** when PyLauncher executes each command. This makes them ideal for constructing unique, collision-free output directories per task.

---

### Output Location Strategy

The example command writes outputs to:

```text
$WORK/sweep_<jobid>/line_<launcher_jid>/slot_<launcher_task_id>
```

This path is **outside the job execution directory**. This design choice:

* keeps the execution directory lightweight,
* reduces I/O and packaging overhead at job completion, and
* avoids unnecessarily archiving large sweep results when using Tapis-based workflows.

---

## When to Use This Utility

Use this pattern when you need to:

* run large parametric sweeps,
* generate PyLauncher `runsList.txt` files programmatically,
* keep job outputs well-organized and scalable, and
* minimize archiving overhead in HPC and Tapis workflows.


---

#### Files

You can find these files in **Community Data**.

````{dropdown} flatten_dict.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Misc/generate_task_commands.py
:language: none
````
