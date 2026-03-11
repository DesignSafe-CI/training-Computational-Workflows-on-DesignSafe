# Executable File

***Interactive Mode:** Running the program without a script for live, one-command-at-a-time execution*

The **first part** of any OpenSees or OpenSeesPy command is the name of the **executable file**.
If you run the executable **by itself** — without providing a script or additional arguments — the program launches in **Interactive Mode**.

In this mode, the program gives you its own prompt and waits for you to type **one command at a time**, immediately executing it and displaying results before waiting for the next one.

Running an interactive session of OpenSees allows you to test the program and make sure you have set up the right environment. This is ideal for:

* Testing syntax or exploring commands in real time
* Building a small model step-by-step
* Debugging specific lines of code without running an entire script


**Important:**

* Interactive Mode is **always single-process** — it cannot run in parallel across multiple processors: OpenSees can run interactively only for sequential analyses or methods that do not require mpi management.
* This is because parallel execution (MPI) requires all processes to read and execute a script in sync, which is not possible when commands are entered manually.

:::{note}
If the executable is not in your system’s `PATH`, you’ll need to specify its **full file path** (e.g., `/path/to/OpenSees`) when calling it.
:::

| Application         | Command                             | Prompt         |
| ------------------- | ----------------------------------- | -------------- |
| OpenSees-Tcl        | `OpenSees`                          | `OpenSees >`   |
| OpenSeesPy (Python) | `python` *(then import OpenSeesPy)* | `>>>` (Python) |

---

### When to Use Interactive Mode

* Learning or **prototyping**
* Inspecting or debugging model elements
* Quick, single-threaded testing of parameters

## Demo Examples
:::{dropdown} OpenSees-Tcl Interactive

    
**1. At the Command-line prompt**.<br>
Start OpenSees-Tcl interactively by simply typing at the terminal:

    OpenSees

    
You’ll see a prompt like:



        OpenSees -- Open System For Earthquake Engineering Simulation
                Pacific Earthquake Engineering Research Center
                        Version xx.xx.xx 64-Bit

    (c) Copyright 1999-20xx The Regents of the University of California
                            All Rights Reserved
    (Copyright and Disclaimer @ http://www.berkeley.edu/OpenSees/copyright.html)


    OpenSees > 


  
You can now enter your commands at the prompt, one at a time, as shown below:
  

    OpenSees > wipe
    OpenSees > model BasicBuilder -ndm 2 -ndf 3
    OpenSees > exit

<!-- <div id="slideShowTCL">
<script>
    addSlides("slideShowTCL","../../../shared/imagesInteractive_Tcl/Slide","JPG",1,7)
</script>

 -->

:::

:::{dropdown} OpenSeesPy Interactive

**1. At the Command-line prompt**.<br>
Start python interactively by simply typing at the terminal:

       python
    

The command-line command will start an interactive session. 

    Python 3.10.6 | packaged by conda-forge | (main, Aug 22 2022, 20:35:26) [GCC 10.4.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 

You can now enter your commands at the prompt, one at a time, as shown below. You need to import OpenSeesPy before you can run OpenSees commands:

    >>> import openseespy.opensees as ops
    >>> ops.wipe()
    >>> ops.model('BasicBuilder','-ndm',2,'-ndf',3)
    >>> exit()
    Process 0 Terminating

<!-- <div id="slideShowPY">
<script>
    addSlides("slideShowPY","../../../shared/imagesInteractive_Py/Slide","JPG",1,8)
</script>
 -->
**2. In a Jupyter Notebook**<br>
You can also run OpenSeesPy interactive by importing it into your Jupyter notebook:

    import openseespy.opensees as ops
    ops.wipe()
    ops.model('BasicBuilder','-ndm',2,'-ndf',3)

You do not need to exit.

:::
    

