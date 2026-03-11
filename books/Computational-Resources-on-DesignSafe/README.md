# Computate Resources on DesignSafe
***Execution Systems and Data Environments***

by **Silvia Mazzoni**<br>
January 2026

---

DesignSafe provides an integrated cyberinfrastructure for research in natural hazards engineering, combining **interactive user interfaces**, **shared data services**, and **large-scale computational systems** into a unified platform. Together, these components support the full research lifecycle—from exploratory model development and testing, to large-scale simulation campaigns, to post-processing, visualization, and long-term data management.

At the center of DesignSafe’s computational capability is its close integration with the **Texas Advanced Computing Center (TACC)**. TACC supplies the high-performance computing systems, parallel filesystems, and scheduling infrastructure that power most analyses executed through DesignSafe. Whether a computation is launched from the web portal, a Jupyter notebook, or an automated pipeline, execution typically occurs on TACC resources such as **Stampede3**, enabling analyses that far exceed the capabilities of local machines.

This book focuses on **computational environments**, not applications or workflows. Specifically, it explains:

* **Interface environments** — where users interact with DesignSafe (web portal, JupyterHub, terminals, APIs)
* **Execution environments** — where computations actually run (HPC systems, batch queues, compute nodes)
* **File storage and data management** — how data moves, persists, and scales across environments

A key goal of this document is to help readers understand **where things happen**: where commands are issued, where jobs are executed, where data lives, and how these locations differ across environments. This understanding is essential for making informed decisions about performance, scalability, reproducibility, and cost.

***What this document does not focus on*** is the design of computational workflows themselves. Concepts such as workflow structure, job orchestration, SLURM behavior, and Tapis-based automation are addressed in a companion volume dedicated specifically to workflows. Instead, this book provides the **environmental foundation** upon which those workflows operate.

By the end of this document, readers should be able to confidently navigate DesignSafe’s computational landscape, understand the roles of its various environments, and choose appropriate execution and storage strategies for their research—regardless of the specific application they are running.




---
  
:::{include} TAILS.md
:::