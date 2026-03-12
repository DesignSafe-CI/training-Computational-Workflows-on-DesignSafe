# designsafe-agnostic-app

***Agnostic Tapis App for General Execution: Python as well as OpenSees, OpenSeesMP, OpenSeesSP, and OpenSeesPy***

* **Version:** 1.0.1
* **Author:** *Silvia Mazzoni, DesignSafe*
* **Date:** January 18, 2026

**Platform:** DesignSafe / TACC Stampede3
**Runtime:** ZIP (HPC Batch)
**Execution System:** Stampede3
**Queue (default):** skx-dev

## 1. Purpose and Design Philosophy

*designsafe-agnostic-app* is a **general-purpose, HPC-oriented Tapis application** designed to support *many* computational workflows without baking assumptions into the app itself.

Instead of creating separate apps for:

* OpenSees vs OpenSeesMP
* Tcl vs Python
* Serial vs MPI
* Small vs large output jobs

this app acts as a **configurable execution driver**.

All behavior is controlled by:

* **app inputs**
* **environment variables**
* **wrapper logic**

This makes the app:

* reusable
* transparent
* automatable
* easy to fork and extend

Tapis orchestrates the job.
SLURM executes it.
**The wrapper enforces semantics and safety.**

---

## 2. High-Level Execution Model

At runtime, the following happens:

1. Tapis stages *inputDirectory*
2. A SLURM batch job is submitted
3. *tapisjob_app.sh* executes on the first node
4. The wrapper:

   * prepares the environment
   * stages inputs
   * selects MPI vs non-MPI execution
   * runs the main executable
   * manages outputs
   * produces structured logs

The **minimum mental model** for the app is:

**[UseMPI?]  BINARYNAME  INPUTSCRIPT  ARGUMENTS**

<details>
  <summary><b>Detailed Execution Mode</b></summary>
  
1. Tapis stages your **Input Directory** to the job working directory.
   
2. SLURM starts the batch job on Stampede3.
   
3. *tapisjob_app.sh* runs on the first allocated node and:
   
   - sets up summary and full environment logs
     
   - *cd*s into the Input Directory
     
   - prepares inputs (optional copy-in, optional unzip)
     
   - loads modules (optional file + optional list)
     
   - normalizes Python (*python* → *python3*)
     
   - installs Python packages (optional file + optional list)
     
   - optionally injects TACC-compiled OpenSeesPy (*opensees.so*)
     
   - optionally runs pre/post hooks
     
   - chooses MPI launcher (*ibrun*) or direct run
     
   - runs your executable + script + args
     
   - optionally zips output and/or moves results inside the exec system
     
   - records timers and exits with clear error handling

    
</details>




## 3. Logs you should look at first

Every job produces:
- ***SLURM-job-summary.log*** (compact “what happened”)
- ***SLURM-full-environment.log*** (full *env | sort* dump)

The summary log also records:
- launcher decision
- module/pip actions
- timers (run-only and total)



---

## 4. Summary

*designsafe-agnostic-app* provides a single, well-instrumented execution interface for:
- OpenSees (Tcl), OpenSeesMP/SP (MPI), OpenSeesPy
- general Python workflows
- reusable HPC job patterns (copy-in, unzip, hooks, packaging, output movement)

It is designed to be **debuggable, reproducible, and extensible**, and to serve as a template for future apps.


