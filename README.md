# Computational Workflows on DS Series
***A Series of Documents dedicated to Understanding Interfaces, Middleware, and Execution Environments***


by **Silvia Mazzoni**<br>
February 2026

---


This document is part of a documentation series that provides a **system-level view of how computational research runs on DesignSafe**. Rather than focusing on individual tools in isolation, the series explains how **user interfaces, middleware services, execution environments, and data systems work together** to support workflows that scale from interactive exploration to large-scale, automated studies.

Each document approaches the platform from a different angle — from conceptual architecture, to concrete execution patterns, to real scientific applications — helping users design workflows that are **robust, efficient, and reproducible** across DesignSafe’s ecosystem.

---

::::{grid} 1 1 1 1
:gutter: 3

:::{grid-item-card}
:class-header: bg-light text-center
<a href="https://designsafe-ci.github.io/training-OpenSees-on-DesignSafe/README.html" target="_blank" rel="noopener">
Computational Workflows on DesignSafe
</a>
^^^
***Platform Architecture & Workflow Concepts***<br>
This document introduces the *core workflow architecture of DesignSafe*, explaining how *interface environments* (web portal, JupyterHub, APIs), *middleware services*, *execution environments* (HPC systems and compute nodes), and *file storage systems* interact to support scalable and reliable computational research.
:::

:::{grid-item-card}
:class-header: bg-light text-center
<a href="https://designsafe-ci.github.io/training-OpenSees-on-DesignSafe/README.html" target="_blank" rel="noopener">
Computational Resources on DesignSafe
</a>
^^^
***Where and How Computation Runs***<br>
This document focuses on the *compute environments available on DesignSafe*, clarifying where analyses actually execute, how resources are allocated, and how users move between interactive and batch workflows. It emphasizes practical distinctions between login, execution, and storage systems, and how those distinctions affect performance and usability.
:::

:::{grid-item-card}
:class-header: bg-light text-center
<a href="https://designsafe-ci.github.io/training-OpenSees-on-DesignSafe/README.html" target="_blank" rel="noopener">
OpenSees-on-DesignSafe Training
</a>
^^^
***OpenSees as a Workflow Case Study***<br>
This document uses *OpenSees* as a concrete example of a *scalable scientific workflow* on DesignSafe — covering scripting, parameter studies, parallel execution, job submission, and results management. While OpenSees is the focus, the workflow patterns apply broadly to many computational applications.
:::

:::{grid-item-card}
:class-header: bg-light text-center
<a href="https://designsafe-ci.github.io/training-OpenSees-on-DesignSafe/README.html" target="_blank" rel="noopener">
OpsUtils Python Utilities
</a>
^^^
***Reusable Python Tools for Workflows***<br>
A custom Python utility library designed to support common workflow tasks on DesignSafe, including *job submission and monitoring, file and path management, data inspection, and automation*. These utilities encapsulate best practices and reduce boilerplate when building repeatable computational workflows.
:::
::::



---

## How to Read This Series

This series is designed to be **modular**, not strictly linear. You do **not** need to read every document from start to finish to benefit from it. Instead, think of each document as addressing a different layer of the same system.

**Recommended starting points depend on your goals:**

* **New to DesignSafe or feeling unsure where things run**
  Start with **Computational Workflows on DesignSafe** to build a mental model of how interfaces, middleware, execution environments, and storage fit together.

* **Deciding where and how to run computations**
  Read **Computational Resources on DesignSafe** to understand the differences between interactive and batch environments, where jobs actually execute, and how resource choices affect performance and scalability.

* **Running real scientific applications**
  Use **OpenSees-on-DesignSafe Training** as a concrete, end-to-end example of how a complex application is scripted, executed, parallelized, and managed across DesignSafe systems.

* **Automating and streamlining workflows**
  Refer to **OpsUtils Python Utilities** when building repeatable, script-driven workflows that involve job submission, monitoring, file management, or data inspection.

Many users will move **back and forth** between documents as their understanding deepens or their workflow evolves. That’s intentional: the series is meant to support **exploration, iteration, and scaling**, rather than a one-time, linear read.


---
  
:::{include} TAILS.md
:::