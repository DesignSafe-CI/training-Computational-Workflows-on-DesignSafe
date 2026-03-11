# Document Objectives

This document has four primary objectives.

---

## 1. Clarify the Execution Architecture

Provide a clear explanation of how OpenSees runs across different computational environments within DesignSafe, including:

* Web Portal submission
* JupyterHub execution
* Terminal-based workflows
* Tapis application submissions
* Direct SLURM execution on TACC HPC systems

Readers should understand where computation occurs, how jobs are scheduled, how files move between storage systems, and how middleware services interact with HPC infrastructure.

---

## 2. Provide Practical Workflow Guidance

Offer concrete, reproducible workflows for running OpenSees in multiple modes:

* Interactive execution
* Script-based execution
* Parallel MPI execution
* Web Portal app submission
* Programmatic API submission

This includes guidance on:

* Command structure
* Executable selection
* Input file organization
* Resource specification (nodes, cores, walltime)
* Output management

---

## 3. Enable Scalable and Automated Studies

Demonstrate how to move from single-model execution to large-scale studies by:

* Passing command-line arguments
* Dynamically generating input scripts
* Automating parameter sweeps
* Submitting and monitoring multiple jobs
* Leveraging Tapis APIs for programmatic workflows

The objective is to support reproducibility, scalability, and computational efficiency.

---

## 4. Integrate Training as a Structured Component

While this is a reference document, it includes structured training modules that:

* Walk through complete end-to-end workflows
* Provide guided notebook demonstrations
* Show step-by-step Web Portal submissions
* Compare multiple execution approaches

These training sections reinforce the architectural explanations and provide practical experience applying the concepts.

---

# Outcome for the Reader

By the end of this document, readers should be able to:

* Select the appropriate execution environment for their OpenSees workflow
* Submit and monitor jobs confidently across platforms
* Understand how Tapis and SLURM interact
* Execute parallel OpenSees simulations correctly
* Automate large parameter studies
* Debug issues with architectural awareness

Most importantly, readers should understand not just how to run OpenSees on DesignSafe — but how the system itself operates.

---

### Introductory Webinar

On September 17, 2025 we held a webinar introducing this training document. This webinar introduced DesignSafe as a unified platform for advancing natural hazards research, offering integrated tools for data management, interactive modeling, and high-performance computing. Using OpenSees as the primary case study, participants explored how to design and scale computational workflows — from small exploratory runs to automated HPC pipelines. The session emphasized the complete scientific workflow lifecycle, including model setup, job submission, monitoring, and results management. While focused on earthquake engineering, the strategies presented are broadly transferable to other domains such as CFD, climate modeling, and structural simulation.

[Access the recording of this webinar.](https://youtu.be/hexvyWy6G20?si=bo-n58AZ3loR0VuF)

:::{dropdown} Presentation Slides

<div id="slideShow_WebinarSlides">
<script>
    addSlides("slideShow_WebinarSlides","../shared/images/Webinar/WebinarSlides/Slide","JPG",1,29)
</script>

:::
