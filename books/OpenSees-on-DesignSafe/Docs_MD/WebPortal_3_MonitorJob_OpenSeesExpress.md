# 3 Monitor OpenSees-Express
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
    | `output.<jobid>.out` | Standard output: printed messages, progress, custom script output         |
    | `output.<jobid>.err` | Standard error: errors like missing files, module issues, syntax problems |
    
    These are the **first files to check** if the job failed or didn't produce expected results.
    
    Your full output (including `.out`, `.err`, result files, and any OpenSees output) will be **automatically archived** to:
    
    ```
    $WORK/tapis-jobs-archive/<date>/<jobname>-<uuid>/
    ```
    
    This ensures long-term storage on TACC’s system and web access from DesignSafe.


## Demo

*(slide numbering is continued from the submit-job demo)*

10. Click on Job Status
11. Find your job and click "View Ouputs" once the job is "Finished"
12. Study the path of the output folder, you will be looking for it in post-processing. <br>
Open the .env file to check for errors
13. The TapisJob.env info will be useful to understand Tapis
14. Click on tapisjob.out
15. This file echoes the app's and your script's print to screen (echo and puts) (make sure you have the right input filename and opensees version)<br>
Look for errors in the echo data or for the exit code.
16. Open the input directory you had "uploaded"
17. Open the output directory created by your script
18. Make sure the files are as expected
19. Verify your recorder output.
20. -25 .... view your files in JupyterHub.

<div id="slideShow">
<script>
    addSlides("slideShow","../../../shared/imagesWebPortal_Express/Slide","JPG",10,25)
</script>

