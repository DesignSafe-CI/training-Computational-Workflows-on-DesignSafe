# 2 Submit OpenSees-Express
***Submit Input File to Web Portal -- OpenSees-Express***


## Summary of Form Input Parameters

| Parameter             | Description |
|-----------------------|-------------|
| -- Job Parameters -- |
| **Max Runtime**       | Maximum wall-clock runtime for the job. |
| **Job Name**          | Descriptive name for the job (for tracking/logging). |
| -- OpenSees-Analysis Parameters -- |
| **Input Directory**   | Folder with scripts and input files. |
| **Main Script**       | Main input script passed to the application at runtime. |



## Demo
1. **Navigate to the OpenSees-Express App** in the Web Portal  from the [DesignSafe Web Portal](https://www.designsafe-ci.org/)<br>
    `Tools & Applications → Simulation Tools → OpenSees`,<br>
    **Read** all documentation, <br>
    and click **Get Started** button.
  
2. Select Input Directory
3. Navigate to folder that contains your input file and copy the input filename to the clipboard
4. Click the select button next to the foldername.
5. Once the path has been accepted click Continue. Look at the tapis filepath for future reference when learning tapis.
6. Navigate to your Main Script and select it. Or paste the name you had copied.
7. Make sure the main program selected is "OpenSees"
8. Make sure the maximum runtime exceeds your estimated analysis time. Or just use the maximum allowed value.
9. Leave Outputs parameters at default, maybe add a personalization to the Job name.<br>
Review all input<br>
Click Submit Job
10. Make sure you see a confirmation that the job has been submitted.

<div id="slideShow">
<script>
    addSlides("slideShow","../../../shared/imagesWebPortal_Express/Slide","JPG",1,10)
</script>
