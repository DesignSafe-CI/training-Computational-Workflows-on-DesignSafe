# 3 Monitor OpenSeesMP
***Monitor the Job and, Once Finished, Check output***

1. ## Monitor Job Status

    Once submitted, you’ll be redirected to the **"My Jobs" dashboard**.
    
    Here you can:
    
    * **Track status** (Queued → Running → Finished)
    * **View output directory**
    * **Access logs** (see below)

1. ## Wait until the job reaches the status *FINISHED*
 
1. ## Check Output Files

    After the job completes, examine two key files in your output folder:
    
    | File                 | Description                                                               |
    | -------------------- | ------------------------------------------------------------------------- |
    | *output.<jobid>.out* | Standard output: printed messages, progress, custom script output         |
    | *output.<jobid>.err* | Standard error: errors like missing files, module issues, syntax problems |
    
    These are the **first files to check** if the job failed or didn't produce expected results.
    
    Your full output (including *.out*, *.err*, result files, and any OpenSees output) will be **automatically archived** to:
    
    ```
    $WORK/tapis-jobs-archive/<date>/<jobname>-<uuid>/
    ```
    
    This ensures long-term storage on TACC’s system and web access from DesignSafe.


## Demo
*(slide numbering is continued from the submit-job demo)*

10. Click on Job Status
11. Click on View Details. This option is very useful to check on the job while it is running, before it is finished.
12. You have the option to view the files in the "Execution Directory" in **real-time**<br>
You can see that you are in the scratch directory of stampede.<br>
Select the tapisjob.out file.
13. Make sure that the echo output make sense. you can see the run-OpenSees call, the version of OpenSees, and your script's screen output. You can see that you have many processors running concurrently.
14. Once finished, click "View Output"
15. You can see that the files have been moved to your MyData folder, in 'tapis-jobs-archive' folder. you can now access it from anywhere.
16. Check the tapisjob.out file for messages at the bottom of the output to see if OpenSees exited cleanly or had an error.
17. ... you can now check the output content and then view it in Jupyter Hub.


<div id="slideShow">
<script>
    addSlides("slideShow","../../../shared/imagesWebPortal_MP/Slide","JPG",10,23)
</script>


