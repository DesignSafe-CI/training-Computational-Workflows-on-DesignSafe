# 2 Submit OpenSeesMP
***Submit Input File to Web Portal -- OpenSees-Express***


## Summary of Form Input Parameters

| Parameter             | Description |
|-----------------------|-------------|
| -- Job Parameters -- |
| **Allocation**        | Select which TACC allocation/account to charge. |
| **Queue**             | HPC queue to run in (e.g., `skx`,`skx-dev`). |
| **Max Runtime**       | Maximum wall-clock runtime for the job. |
| **Node Count***        | Number of compute nodes to request. |
| **Cores per Node**    | Number of processors per node. |
| **Job Name**          | Descriptive name for the job (for tracking/logging). |
| -- OpenSees-Analysis Parameters -- |
| **Input Directory**   | Folder with scripts and input files. |
| **Main Script**       | Main input script passed to the application at runtime. |

* Your allocation is charged by Node hours, so use the least number of nodes



## Demo

1. **Navigate to the OpenSeesMP** in the Web Portal  from the [DesignSafe Web Portal](https://www.designsafe-ci.org/)<br>
    `Tools & Applications → Simulation Tools → OpenSees`,<br>
    **Read** all documentation, <br>
    and click **Get Started** button.
  
2. Select Input Directory
3. Navigate to folder that contains your input file and copy the input filename to the clipboard.<br>
   Click the select button next to the foldername.
4. Once the path has been accepted click Continue. Look at the tapis filepath for future reference when learning tapis.
5. Navigate to your Main Script and select it. Or paste the name you had copied.
6. Leave the default **allocation**, or select your favorite. Select the **queue** -- the dev queue has a shorter wait because it has a 2-hour limit.
7. Make sure the maximum runtime exceeds your estimated analysis time. the more time you request, the longer the wait.<br>
Make sure you set the number of nodes to the least number you need -- you are charged for your node hours. Select the number of cores per node.
8. Leave Outputs parameters at default, maybe add a personalization to the Job name.<br>
Review all input<br>
Click Submit Job
9. Make sure you see a confirmation that the job has been submitted.

<div id="slideShow">
<script>
    addSlides("slideShow","../../../shared/images/WebPortal_MP/Slide","JPG",1,9)
</script>

