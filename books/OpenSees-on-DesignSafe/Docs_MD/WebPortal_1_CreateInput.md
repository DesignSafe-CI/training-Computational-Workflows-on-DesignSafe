# 1 Create Input
***Create Input Files in JupyterHub***

Here you can edit your script as well as test it interactively.

Edit you model and test it for a limited number of input parameters. Final edit: add the full set of input parameters.

Remember the location of your file.

## Demo
1. Access DesignSafe Tools & Apps
2. Launch JupyterHub & navigate to your file folder
**Tcl**
3. Ex1a.Canti2D.Push.tcl -- OpenSees-Tcl Sequential
4. Ex1a.Canti2D.Push.mp.tcl -- OpenSeesMP
5. Compare OpenSees and OpenSeesMP files
6. Ex1a_many.Canti2D.Push.mp.tcl -- OpenSeesMP, the number of input parameters is variable so we can test a large dataset (the file is split into two views)
**OpenSeesPy**
7. Ex1a.Canti2D.Push.py -- OpenSeesPy Sequential
8. Ex1a.Canti2D.Push.mpi.py -- OpenSeesPy, native mpi. The native mpi does not work with mpiexec (used in JupyterHub), but it does work with ibrun (used in Stampede3). 
9. Ex1a.Canti2D.Push.mpi4py.py -- OpenSeesPy using mpi4py. Use this only if running in JupyterHub.
10. Comparison of the two OpenSeesPy MPI options


<div id="slideShow">
<script>
    addSlides("slideShow","../../../shared/imagesCreateInput/Slide","JPG",1,10)
</script>



## Example Files Used in this demo
You can find these files in Community Data:

### Tcl

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
```{dropdown} Ex1a_many.Canti2D.Push.mp.tcl
:icon: file-code
```{literalinclude} ../../../shared/Examples/OpenSees/Ex1a_many.Canti2D.Push.mp.tcl
:language: none
```

### OpenSeesPy


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
