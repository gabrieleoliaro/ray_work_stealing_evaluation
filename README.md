# Evaluation of the new work stealing functionality for Ray

This repository contains a set of scripts that allow one to launch a Ray cluster on AWS and benchmark the task pipelining / work stealing functionalities, which are currently under development. The repo also contains the data and plots from the most recent experiments (will be updated every time we introduce a change to the code). 

The **task pipelining functionalities** have already been merged to the [ray-project/ray](https://github.com/ray-project/ray) master branch (see [PR here](https://github.com/ray-project/ray/commit/026c0090865373c87065fa0fe9972afc1a769514)). 

**Work stealing**, on the other hand is in the final stages of development in [this branch](https://github.com/gabrieleoliaro/ray/tree/atomic_work_stealing), although two PRs related to work stealing (see [here](https://github.com/ray-project/ray/pull/10225), and [here](https://github.com/ray-project/ray/pull/11051)) have already been merged to the [ray-project/ray](https://github.com/ray-project/ray) master branch.


## Scripts

This repository contains the following scripts:

1. `execute_tasks.py`: This script allows you to run a workload that consists of the execution of a series of Ray tasks. The script's arguments allow you to customize **the total sequential duration** of the experiment (i.e. the time a single-core Ray worker should take to execute all tasks in a sequential fashion), **the individual task duration** (i.e. the length of each task, taken individually), **the number of cores** to use in the experiment, the **maximum number of tasks in flight to any worker**, whether **work stealing** is to be enabled, and the **path to the output file**, where the raw data will be placed
2. `run_experiment.sh`: This script allows you to run an experiment that consists of multiple jobs, where each job is completed by running the `execute_tasks.py` script with the proper arguments. All the parameters for the experiment are defined at the top of the files. Edit those values to customize your experiment. In particular, the script allows you to choose: the **number of trials** to use for each job in the experiment, the set of values to test for the **maximum number of tasks in flight to any worker** (one per job), the **the total sequential duration** (same for all the jobs) and the **the individual task duration** (one for each job). The script will run one job for each combination of the parameters, and repeat the experiment with **work stealing** enabled and without.
3. `plot_results.py`: This is a Python script that allows one to plot the data obtained from a `run_experiment.sh` experiment


## Results
The [output folder](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/tree/main/output) contains the most recent experiment results. Each subfolder (whose name is the date/time when the experiment was run) contains an automatically generated `experiment.info` file with the information about the experiment, the text files with the raw data, and a `plots` folder with the corresponding plots.

The Apr 23 experiments were executed using the code in the new work stealing PR: https://github.com/ray-project/ray/pull/15475 . The Jan 19 experiments were executed using the code in the branch: https://github.com/gabrieleoliaro/ray/tree/work_stealing

### The latest experiment

The latest experiment (described here) ran on a AWS `m4.16xlarge` machine with 64 cores. The experiment consisted of running several jobs under different settings, while keeping the total sequential execution time (i.e. the time it would take to run the job on a machine with only 1 core) constant and equal to 100s. 

We varied the following parameters:
* `max_tasks_in_flight_per_worker` parameter, which governs the size of the owner-to-worker pipelines, determining how many tasks can be in flight to each worker.
* the individual task duration, determining the duration of each task in the workload, as well as the total number of tasks. In particular, the number of tasks was determined by: ![formula](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/formula.png)
* the Ray `work_stealing` boolean parameter, determining whether work stealing is enabled or not.

Each combination of the aforementioned parameters defines a unique job. For example, a unique job could be one where the `max_tasks_in_flight_per_worker` is set to 64, the individual task duration is set to 500ms, and work stealing is enabled. Each unique job is repeated for a number of times, depending on the value of the `ntrials` parameter in the `run_experiment.sh` script. In this experiment, we let `ntrials` = 3. Each data point on the plots corresponds to a unique job, and it is computed by averaging the measurements obtained over the several trials (in our case, 3). The plots also show vertical bars that represent the standard deviation of the measurements (the bars are not visible in the plots below because the standard deviation is very small).

#### Plots
For each experiment, we provide two sets of plots. One has the individual task duration on the x-axis, the other has the max_tasks_in_flight_per_worker parameter on the x-axis. Both sets of plots are obtained from the same experiment.

##### Plos with the individual task duration on the x-axis
Each plot corresponds to a different setting for the `max_tasks_in_flight_per_worker` parameter. The values we used were: 1, 5, 20, 64, and 150. When `max_tasks_in_flight_per_worker`=1, task pipelining is not enabled, so the owner can only send one task at a time to each worker. In that case, work stealing is also not enabled.

The plots have two curves: a baseline curve (in blue), showing the performance of Ray when work stealing is not enabled and a second curve (in orange), showing the performance of Ray when work stealing is enabled. Each curve shows the parallel execution time of a workload as a function of the individual task duration. In particular, we used the following values for the individual task duration: 10ms, 50ms, 100ms, 500ms or 1000ms. 


![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-1-MTIF.png)

![Plot5](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-5-MTIF.png)

![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-20-MTIF.png)

![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-64-MTIF.png)

![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-150-MTIF.png)

##### Plos with the max_tasks_in_flight_per_worker on the x-axis
Each plot corresponds to a different setting for the duration of each task in the workload. The values used are: 10ms, 50ms, 100ms, 500ms or 1000ms.

The plots have two curves: a baseline curve (in blue), showing the performance of Ray when work stealing is not enabled and a second curve (in orange), showing the performance of Ray when work stealing is enabled. Each curve shows the parallel execution time of a workload as a function of the max tasks in flight. In particular, we used the following values for the individual task duration: 1, 5, 20, 64, and 150. 


![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-10-ITD.png)

![Plot5](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-50-ITD.png)

![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-100-ITD.png)

![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-500-ITD.png)

![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-1000-ITD.png)

#### Data files
As described in the [experiment.info](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/experiment.info) file, each data file in the output folder is named using the template `data-<number1>-WS-<number2>-MTIF.txt`, where `<number1>` (which can only be 1 or 0) indicates whether Work Stealing (WS) was enabled and `<number2>` indicates the Maximum Number of Tasks (MTIF). For instance, the file [data-0-WS-150-MTIF.txt](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/data-0-WS-150-MTIF.txt) contains the data from the experiment where work stealing was not enabled (`<number1>`=0), and the `max_tasks_in_flight_per_worker` param was set to 150 tasks (`<number2>`=150).

Each raw data file is divided into blocks, where each block corresponds to a specific value for the individual task duration. Each block contains a first line with an integer that records the individual task duration (in milliseconds), followed by one line for each trial. Each such line contains a decimal number, which is the parallel execution time (in seconds) for the workload.


