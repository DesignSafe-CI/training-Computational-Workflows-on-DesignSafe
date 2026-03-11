# OpenSees Workflows

In practice, there are four main ways to run OpenSees on DesignSafe:

1. **Web Portal (Tapis Apps):** Submit preconfigured jobs directly to HPC.
2. **JupyterHub (local run):** Run OpenSees interactively inside a Jupyter container.
3. **JupyterHub (HPC submission):** Stage and launch jobs to HPC using Tapis Apps from your notebooks.
4. **SSH (manual SLURM):** Log into HPC systems and submit custom batch jobs.

The diagram below illustrates how these workflows map onto the DesignSafe architecture:

<img src="../../../shared/imagesWaysToRunOps/WaysToRunOpenSeesOnDS_all.jpg" alt="Workflows for OpenSees on DesignSafe" width="75%" />  

---

## Recommendations

Because each workflow has trade-offs, here are some practical guidelines:

### 1. Run small to medium jobs within JupyterHub

* Fastest turnaround — no queue wait and no walltime limits.
* Each container provides **8 processors**.

  <img src="../../../shared/imagesWaysToRunOps/WaysToRunOpenSeesOnDS_JupHub.jpg" alt="Workflows for OpenSees on DesignSafe -- Jupyter Hub" width="50%" />  

### 2. Submit medium to large jobs to HPC from JupyterHub

* Recommended for heavier workloads.
* Combines the convenience of Jupyter for file and script management with the scalability of HPC resources.

  <img src="../../../shared/imagesWaysToRunOps/WaysToRunOpenSeesOnDS_HPC.jpg" alt="Workflows for OpenSees on DesignSafe HPC" width="50%" />  


