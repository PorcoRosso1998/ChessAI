# Parallel Alpha-Beta Pruning
## Group Members
* Chase Zimmerman
* Patrick Griffin Morris
* Mailani Gelles

## Platform Requirements
Both the Cython and Python version can be run on any system with MPI.

## Installation
This program requires the following follow python packages:
* numpy
* chess
* mpi4py
* cython

## Compiling
To compile the Cython implementation, perform the following commands:
```
cd ./FastABP
```
Compile.
```
python3 setup.py build_ext --inplace
```
Move shared object file. **This step is important as the shared object file must be in the same directory as AlphaBetaPruning.py**
```
mv <shared object file> ..
```

## Running
There are two options. In the USC HPC environment, you can submit a SLURM task using the provided `.sl` file, adjusting the number of cores accordingly.
```
sbatch submit_job.sl
```
The output is stored in `mpijob.out`.
Alternatively, the code can be executed on another machine with MPI. A command similar to the following should work:
```
mpiexec -n <tasks> python3 AlphaBetaPruning.py
```

## Configuration
There are two parameters to configure, both are global variables in `AlphaBetaPruning.py`. The first variable is the game tree depth and the second is the random seed used to determine the "human" player's moves. Default configuration is:
```
SEED = 5
DEPTH = 2
```