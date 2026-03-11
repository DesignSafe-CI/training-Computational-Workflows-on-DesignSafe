# Run OpenSees Script at the CLI


Most OpenSees analyses are run in **non-interactive mode**, where you execute a full input script all at once. Even if you’re in an interactive environment like Jupyter, running a script this way means the entire sequence of commands executes without waiting for further input. Jupyter Hub has an integrated editor to make things easy.

You can run therefore, run either OpenSees(Tcl) and OpenSeesPy (Python) in non-interactive batch mode at the terminal's CLI by specifying the input script to execute. In both cases, the first argument provided after the executable is interpreted as the **main script file** to run.

Most OpenSees Analyses require that you work with an input script that you can edit as needed to fix errors and add features.
Being able to work with this script in an interactive environment allows to have immediate feedback on your changes.

This is your starting place. Develop your script for a few test cases.

The following images show how to run OpenSees Tcl and OpenSeesPy at the terminal for both **sequential** and **parallel** analyses, for both Tcl and Python interpreters.

<div id="slideShow">
<script>
    addSlides("slideShow","../../../shared/imagesTerminalRun/Slide","JPG",4,13)
</script>

## **Sequential Execution**

| Language   | Command                                            |
| ---------- | -------------------------------------------------- |
| Tcl        | *OpenSees inputfile.tcl*                           |
| OpenSeesPy | *python inputfile.py* (*import OpenSeesPy inside inputfile.py*)        

::::{dropdown} **OpenSees-Tcl**

:::{dropdown} 1. At the Command-line
Type the following command at the command-line prompt:

     OpenSees Ex1a.Canti2D.Push.tcl

You will see the following response:

             OpenSees -- Open System For Earthquake Engineering Simulation
                     Pacific Earthquake Engineering Research Center
                            Version 3.7.1 64-Bit
    
          (c) Copyright 1999-2016 The Regents of the University of California
                                  All Rights Reserved
      (Copyright and Disclaimer @ http://www.berkeley.edu/OpenSees/copyright.html)
    
    
    Analysis-0 execution done
    Analysis-1 execution done
    Analysis-2 execution done
    Analysis-3 execution done
    Analysis-4 execution done
    Analysis-5 execution done
    Analysis-6 execution done
    Analysis-7 execution done
    ALL DONE!!!
    
The program exits and you are returned to the prompt:

    (base) jovyan@3cd0f33abec1:~/BasicExamples$

:::

:::{dropdown} 2. From a Jupyter Notebook -- shell command

Type the following command in a notebook cell:

     import os
     os.system('OpenSees Ex1a.Canti2D.Push.tcl')
        
You will see the following response in the output:
    
         OpenSees -- Open System For Earthquake Engineering Simulation
                 Pacific Earthquake Engineering Research Center
                        Version 3.7.1 64-Bit

      (c) Copyright 1999-2016 The Regents of the University of California
                              All Rights Reserved
    (Copyright and Disclaimer @ http://www.berkeley.edu/OpenSees/copyright.html)


    Analysis-0 execution done
    Analysis-1 execution done
    Analysis-2 execution done
    Analysis-3 execution done
    Analysis-4 execution done
    Analysis-5 execution done
    Analysis-6 execution done
    Analysis-7 execution done
    ALL DONE!!!

:::
::::

::::{dropdown} **OpenSeesPy**

:::{dropdown} 1. At the Command-line
Type the following command at the command-line prompt:

     python Ex1a.Canti2D.Push.py
     
You will see the following response:

    Analysis-0 execution done
    Analysis-1 execution done
    Analysis-2 execution done
    Analysis-3 execution done
    Analysis-4 execution done
    Analysis-5 execution done
    Analysis-6 execution done
    Analysis-7 execution done
    ALL DONE!!!
    Process 0 Terminating
    
The program exits and you are returned to the prompt:

    (base) jovyan@3cd0f33abec1:~/BasicExamples$

:::

:::{dropdown} 2. From a Jupyter Notebook -- shell command
Type the following command in a notebook cell:

     import os
     os.system('python Ex1a.Canti2D.Push.py')
        
You will see the following response:

    Analysis-0 execution done
    Analysis-1 execution done
    Analysis-2 execution done
    Analysis-3 execution done
    Analysis-4 execution done
    Analysis-5 execution done
    Analysis-6 execution done
    Analysis-7 execution done
    ALL DONE!!!
    Process 0 Terminating

:::

:::{dropdown} 3. Within a Jupyter Notebook
Type the following command in a notebook cell:

     %run 'Ex1a.Canti2D.Push.py'
        
You will see the following response:

    Analysis-0 execution done
    Analysis-1 execution done
    Analysis-2 execution done
    Analysis-3 execution done
    Analysis-4 execution done
    Analysis-5 execution done
    Analysis-6 execution done
    Analysis-7 execution done
    ALL DONE!!!
The script was run in the kernel, so now you can continue with OpenSees commands or any python command.
In the next cell type:

    print(LColList)
You will see the following response:

    [100, 120, 200, 240, 300, 360, 400, 480]

Type in the next cell:

    ops.getNodeTags()
You will see the following response:

    [1, 2]
    
:::
::::

##  **Parallel Execution (N cores)**

Use **mpiexec**, **mpirun**, or **ibrun** to launch distributed memory jobs:

| Language         | Command                                                                   |
| ---------------- | ------------------------------------------------------------------------- |
| Tcl (MP)         | **mpiexec -np N OpenSeesMP inputfileMP.tcl**                                |
| Tcl (SP)         | **mpiexec -np N OpenSeesSP inputfileSP.tcl**                                |
| OpenSeesPy (MPI) | **mpiexec -np N python inputfile.py** *                                     |

* *(import OpenSeesPy inside. And script must use mpi4py or similar)*
* N is the number of concurrent processors
* Use **mpiexec** in JupyterHub
* Use **ibrun** in the HPC system, such as Stampede3


::::{dropdown} OpenSeesMP 

:::{dropdown} 1. At the Command-line prompt
Type the following command at the command-line prompt:

     mpiexec -np 3 OpenSeesMP Ex1a.Canti2D.Push.mp.tcl

You will see the following response:

             OpenSees -- Open System For Earthquake Engineering Simulation
                     Pacific Earthquake Engineering Research Center
                            Version 3.7.1 64-Bit
    
          (c) Copyright 1999-2016 The Regents of the University of California
                                  All Rights Reserved
      (Copyright and Disclaimer @ http://www.berkeley.edu/OpenSees/copyright.html)
    
    
    pid 1 of np=3  started
    pid 0 of np=3  started
    pid 2 of np=3  started
    pid 2 of 3 Analysis-2 execution done
    pid 1 of 3 Analysis-1 execution done
    pid 0 of 3 Analysis-0 execution done
    pid 2 of 3 Analysis-5 execution done
    pid 2 ALL DONE!!!
    Process Terminating 2
    pid 1 of 3 Analysis-4 execution done
    pid 0 of 3 Analysis-3 execution done
    pid 1 of 3 Analysis-7 execution done
    pid 1 ALL DONE!!!
    Process Terminating 1
    pid 0 of 3 Analysis-6 execution done
    pid 0 ALL DONE!!!
    Process Terminating 0


The program exits and you are returned to the prompt:

    (base) jovyan@3cd0f33abec1:~/BasicExamples$

:::

:::{dropdown} 2. In a Jupyter Notebook, as a shell command

Type the following command in a notebook cell:

     import os
     os.system('mpiexec -np 3 OpenSeesMP Ex1a.Canti2D.Push.mp.tcl')

    
You will see the following response:


             OpenSees -- Open System For Earthquake Engineering Simulation
                     Pacific Earthquake Engineering Research Center
                            Version 3.7.1 64-Bit
    
          (c) Copyright 1999-2016 The Regents of the University of California
                                  All Rights Reserved
      (Copyright and Disclaimer @ http://www.berkeley.edu/OpenSees/copyright.html)
    
    
    pid 2 of np=3  started
    pid 0 of np=3  started
    pid 1 of np=3  started
    pid 2 of 3 Analysis-2 execution done
    pid 1 of 3 Analysis-1 execution done
    pid 0 of 3 Analysis-0 execution done
    pid 2 of 3 Analysis-5 execution done
    pid 2 ALL DONE!!!
    Process Terminating 2
    pid 1 of 3 Analysis-4 execution done
    pid 0 of 3 Analysis-3 execution done
    pid 1 of 3 Analysis-7 execution done
    pid 1 ALL DONE!!!
    Process Terminating 1
    pid 0 of 3 Analysis-6 execution done
    pid 0 ALL DONE!!!
    Process Terminating 0
:::
::::

::::{dropdown} OpenSeesPy Parallel



:::{dropdown} 1a. At the Command-line prompt, OpenSeesPy mpi.<br>

Type the following command at the command-line prompt:

     mpiexec -np 3 python Ex1a.Canti2D.Push.mpi.py
You will see the following response:

    pid 0 of 1 started
    pid 0 of 1 started
    pid 0 of 1 started
    pid 0 of np=1 Analysis-0 execution done
    pid 0 of np=1 Analysis-0 execution done
    pid 0 of np=1 Analysis-0 execution done
    pid 0 of np=1 Analysis-1 execution done
    pid 0 of np=1 Analysis-2 execution done
    pid 0 of np=1 Analysis-1 execution done
    pid 0 of np=1 Analysis-1 execution done
    pid 0 of np=1 Analysis-3 execution done
    pid 0 of np=1 Analysis-2 execution done
    pid 0 of np=1 Analysis-2 execution done
    pid 0 of np=1 Analysis-4 execution done
    pid 0 of np=1 Analysis-3 execution done
    pid 0 of np=1 Analysis-3 execution done
    pid 0 of np=1 Analysis-5 execution done
    pid 0 of np=1 Analysis-4 execution done
    pid 0 of np=1 Analysis-4 execution done
    pid 0 of np=1 Analysis-6 execution done
    pid 0 of np=1 Analysis-5 execution done
    pid 0 of np=1 Analysis-5 execution done
    pid 0 of np=1 Analysis-7 execution done
    pid 0 of np=1 ALL DONE!!!
    pid 0 of np=1 Analysis-6 execution done
    pid 0 of np=1 Analysis-6 execution done
    pid 0 of np=1 Analysis-7 execution done
    pid 0 of np=1 ALL DONE!!!
    pid 0 of np=1 Analysis-7 execution done
    pid 0 of np=1 ALL DONE!!!
    Process 0 Terminating
    Process 0 Terminating
    Process 0 Terminating

The program exits and you are returned to the prompt:

    (base) jovyan@3cd0f33abec1:~/BasicExamples$
    
You may run into the problem that the OpenSeesPy MPI does not work properly -- it does run 3 instances of OpenSeesPy, but each instance is not aware of the others and identifies as pid=0 out of one instead of pid=0,1,or 2 out of 3. --> All three processors ran all the analyses!

:::

:::{dropdown} 1b. At the Command-line prompt, use mpi4py.<br>
Type the following command in a notebook cell:

     mpiexec -np 3 python Ex1a.Canti2D.Push.mpi4py.py
You will see the following response:

    mpi4py -- python pid 0 of 3 started
    mpi4py -- python pid 1 of 3 started
    mpi4py -- python pid 2 of 3 started
    pid 2 of np=3 Analysis-2 execution done
    pid 0 of np=3 Analysis-0 execution done
    pid 1 of np=3 Analysis-1 execution done
    pid 2 of np=3 Analysis-5 execution done
    pid 2 of np=3 ALL DONE!!!
    pid 1 of np=3 Analysis-4 execution done
    pid 0 of np=3 Analysis-3 execution done
    pid 1 of np=3 Analysis-7 execution done
    pid 1 of np=3 ALL DONE!!!
    pid 0 of np=3 Analysis-6 execution done
    pid 0 of np=3 ALL DONE!!!
    Process 0 Terminating
    Process 0 Terminating
    Process 0 Terminating

The program exits and you are returned to the prompt:

    (base) jovyan@3cd0f33abec1:~/BasicExamples$
    
You now see the three pids out of 3, and each processor ran only the analysis it was assigned.

:::

:::{dropdown} 2a. In a Jupyter Notebook -- shell command, OpenSeesPy-MPI<br>
Type the following command in a notebook cell:

     import os
     os.system('mpiexec -np 3 python Ex1a.Canti2D.Push.mpi.py')
     
You will see the following response. Note that the program exits once the analysis has been run:

    pid 0 of 1 started
    pid 0 of 1 started
    pid 0 of np=1 Analysis-0 execution done
    pid 0 of 1 started
    pid 0 of np=1 Analysis-0 execution done
    pid 0 of np=1 Analysis-1 execution done
    pid 0 of np=1 Analysis-0 execution done
    pid 0 of np=1 Analysis-1 execution done
    pid 0 of np=1 Analysis-2 execution done
    pid 0 of np=1 Analysis-1 execution done
    pid 0 of np=1 Analysis-2 execution done
    pid 0 of np=1 Analysis-3 execution done
    pid 0 of np=1 Analysis-2 execution done
    pid 0 of np=1 Analysis-3 execution done
    pid 0 of np=1 Analysis-4 execution done
    pid 0 of np=1 Analysis-3 execution done
    pid 0 of np=1 Analysis-4 execution done
    pid 0 of np=1 Analysis-5 execution done
    pid 0 of np=1 Analysis-4 execution done
    pid 0 of np=1 Analysis-6 execution done
    pid 0 of np=1 Analysis-5 execution done
    pid 0 of np=1 Analysis-5 execution done
    pid 0 of np=1 Analysis-7 execution done
    pid 0 of np=1 ALL DONE!!!
    pid 0 of np=1 Analysis-6 execution done
    pid 0 of np=1 Analysis-6 execution done
    pid 0 of np=1 Analysis-7 execution done
    pid 0 of np=1 ALL DONE!!!
    pid 0 of np=1 Analysis-7 execution done
    pid 0 of np=1 ALL DONE!!!
    Process 0 Terminating
    Process 0 Terminating
    Process 0 Terminating

As expected, you have the same problem as you had at the command line.
:::

:::{dropdown} 2. In a Jupyter Notebook -- shell command, mpi4py<br>
Type the following command in a notebook cell:

     import os
     os.system('mpiexec -np 3 python Ex1a.Canti2D.Push.mpi4py.py')
     
You will see the following response. Note that the program exits once the analysis has been run:

    mpi4py -- python pid 0 of 3 started
    mpi4py -- python pid 2 of 3 started
    mpi4py -- python pid 1 of 3 started
    pid 1 of np=3 Analysis-1 execution done
    pid 0 of np=3 Analysis-0 execution done
    pid 2 of np=3 Analysis-2 execution done
    pid 1 of np=3 Analysis-4 execution done
    pid 0 of np=3 Analysis-3 execution done
    pid 2 of np=3 Analysis-5 execution done
    pid 2 of np=3 ALL DONE!!!
    pid 1 of np=3 Analysis-7 execution done
    pid 1 of np=3 ALL DONE!!!
    pid 0 of np=3 Analysis-6 execution done
    pid 0 of np=3 ALL DONE!!!
    Process Process 0 Terminating
    0 Terminating
    Process 0 Terminating

As expected, using mpi4pi has resolved the issue.
:::


::::




## Example Files Used in this demo
You can find these files in Community Data:

:::{dropdown} OpenSees-Tcl

```{dropdown}  Ex1a.Canti2D.Push.tcl
:icon: file-code
```{literalinclude} ../../../shared/Examples/OpenSees/Ex1a.Canti2D.Push.tcl
:language: none
```
```{dropdown} Ex1a.Canti2D.Push.mp.tcl
:icon: file-code
```{literalinclude} ../../../shared/Examples/OpenSees/Ex1a.Canti2D.Push.mp.tcl
:language: none
```

:::

:::{dropdown} OpenSeesPy


```{dropdown} Ex1a.Canti2D.Push.py
:icon: file-code
```{literalinclude} ../../../shared/Examples/OpenSees/Ex1a.Canti2D.Push.py
:language: none
```
```{dropdown} Ex1a.Canti2D.Push.mpi.py
:icon: file-code
```{literalinclude} ../../../shared/Examples/OpenSees/Ex1a.Canti2D.Push.mpi.py
:language: none
```
```{dropdown} Ex1a.Canti2D.Push.mpi4py.py
:icon: file-code
```{literalinclude} ../../../shared/Examples/OpenSees/Ex1a.Canti2D.Push.mpi4py.py
:language: none
```
:::