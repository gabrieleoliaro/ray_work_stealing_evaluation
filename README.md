# Evaluation of the new work pipelining and work stealing functionality for Ray

This repository contains a set of scripts to evaluate the performance of Ray under the new task pipelining and work stealing functionalities. Additional scripts in the `utils` folder can be used to launch a Ray AWS cluster and synch the contents with a folder on a local machine. The repo also contains the data and plots from the most recent experiments (will be updated every time we introduce a major change to the code). 

The **task pipelining functionalities** have already been merged to the [ray-project/ray](https://github.com/ray-project/ray) master branch (see [PR here](https://github.com/ray-project/ray/commit/026c0090865373c87065fa0fe9972afc1a769514)). 

**Work stealing**, on the other hand is in the final stages of development in [this branch](https://github.com/gabrieleoliaro/ray/tree/atomic_work_stealing), although two PRs related to work stealing (see [here](https://github.com/ray-project/ray/pull/10225), and [here](https://github.com/ray-project/ray/pull/11051)) have already been merged to the [ray-project/ray](https://github.com/ray-project/ray) master branch.


## Scripts

This repository contains the following scripts:

1. `run_pipelining_eval.sh`: with this script you can evaluate the task pipelining functionality of Ray. The script takes one argument: a binary integer that specifies the **mode**. `./run_pipelining_eval.sh 0` will use "instantaneous" tasks to evaluate the best case scenario for task pipelining, whereas `./run_pipelining_eval.sh 1` will use "long" tasks (each one takes 1000ms) to evaluate the worst case scenario.  
Relevant parameters for the experiment can be found in the file; their values can be customized for one's needs. The experiment will run multiple jobs, where each job is completed by running either the `instantaneous_tasks.py` script (for mode=0) or the `variable_length_tasks.py` script (for mode=1) with the proper arguments. All the data for the experiment will be saved in text files in a subfolder (named with the timestamp when the experiment started) of the output folder. At the end of the data collection, the script will run `plot_pipelining.py` to plot the results. 
2. `run_work_stealing_eval.sh`: with this script you can evaluate the work stealing functionality of Ray. The script does not take arguments.  Relevant parameters for the experiment can be found in the file; their values can be customized for one's needs. The experiment will run multiple jobs, where each job is completed by running the `variable_length_tasks.py` script with the proper arguments. Just like for the `run_pipelining_eval.sh`script, all the data for the experiment will be saved in text files in a subfolder (named with the timestamp when the experiment started) of the output folder. At the end of the data collection, the script will run `plot_work_stealing.py` to plot the results. 


## Results
The [output folder](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/tree/main/output) contains the most recent experiment results. Each subfolder (whose name is the date/time when the experiment was run) contains an automatically generated `experiment.info` file with the information about the experiment, the text files with the raw data, and a `plots` folder with the corresponding plots.


Some relevant results are the following:

* **For work stealing:** The Apr 23 experiments were executed using the code in the new work stealing PR: https://github.com/ray-project/ray/pull/15475 . The two Apr 23 folders differ only in the values for the max_tasks_in_flight params used. The Jan 19 experiments were executed using the code in the branch: https://github.com/gabrieleoliaro/ray/tree/work_stealing
* **For task pipelining:** The following task pipelining experiments also used the PR: https://github.com/ray-project/ray/pull/15475. For the instantaneous-tasks evaluation of Ray with Eager Work Stealing enabled check out the May 17 experiments. For the instantaneous-tasks evaluation of Ray without Eager Work Stealing enabled check out the May 18 experiments. For the long-tasks evaluation of Ray, check out the May 22 experiments.


### A recent task pipelining experiment with long tasks

The experiment ran on a AWS `m4.16xlarge` machine with 64 cores. The experiment consisted of running several jobs under different values of the `max_tasks_in_flight_per_worker` parameter, while keeping the number of tasks and the number of cores constant and equal to 64 (for both parameters). 

We varied the following parameters:
* `max_tasks_in_flight_per_worker` parameter, which governs the size of the owner-to-worker pipelines, determining how many tasks can be in flight to each worker.
* the Ray `work_stealing` boolean parameter, determining whether work stealing is enabled or not.

Each combination of the aforementioned parameters defines a unique job. Each unique job is repeated for a number of times, depending on the value of the `ntrials` parameter in the `run_pipelining_eval.sh` script. In this experiment, we let `ntrials` = 3. Each data point on the plots corresponds to a unique job, and it is computed by averaging the measurements obtained over the several trials (in our case, 3). The plots also show vertical bars that represent the standard deviation of the measurements (the bars are not visible in the plots below because the standard deviation is very small).

#### Plots
For each experiment, we obtained one plot, with the max_tasks_in_flight_per_worker parameter on the x-axis. One curve on the plot shows the baseline throughput (with work stealing not enabled), the other one shows the behavior with work stealing. 

##### Plot with Eager Work Stealing
![Plot0](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-22-02:05:23_pipelining/plots/plot_task_throughput-long_tasks-11-x_ticks.png)

##### Plot without Eager Work Stealing 
![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-22-01:32:32_pipelining_eager-worker-requesting-OFF/plots/plot_task_throughput-long_tasks-11-x_ticks.png)


#### Data files
Each data file in the output folder is named using the template `data-long_tasks-<number1>-WS`, where `<number1>` (which can only be 1 or 0) indicates whether Work Stealing (WS) was enabled.

Each raw data file is divided into blocks, where each block corresponds to a specific value for the max_tasks_in_flight parameter. Each block contains a first line with an integer that records the max_tasks_in_flight (in number of tasks), followed by one line for each trial. Each such line contains a decimal number, which is the parallel execution time (in seconds) for the workload.

### A recent task pipelining experiment with short tasks
The experiment ran on a AWS `m4.16xlarge` machine with 64 cores. The experiment consisted of running several jobs under different values of the `max_tasks_in_flight_per_worker` parameter, while keeping the number of tasks constant and equal to 64. 

We varied the following parameters:
* `max_tasks_in_flight_per_worker` parameter, which governs the size of the owner-to-worker pipelines, determining how many tasks can be in flight to each worker.
* The number of cores used
* the Ray `work_stealing` boolean parameter, determining whether work stealing is enabled or not.

Each combination of the aforementioned parameters defines a unique job. Each unique job is repeated for a number of times, depending on the value of the `ntrials` parameter in the `run_pipelining_eval.sh` script. In this experiment, we let `ntrials` = 3. Each data point on the plots corresponds to a unique job, and it is computed by averaging the measurements obtained over the several trials (in our case, 3). The plots also show vertical bars that represent the standard deviation of the measurements (the bars are sometimes not visible in the plots below because the standard deviation is very small).

#### Plots
For each experiment, we obtain one plot with a curve corresponding to each number of cores setting. The plots have the max_tasks_in_flight values on the x-axis, and the throughput on the y-axis. We have three distinct plots, corresponding to three experiments of interest. The first plot shows the baseline scenario, without work stealing. The second plot shows the scenario where work stealing is enabled. Finally, the third plot shows the scenario with work stealing as well as the Eager Worker Requesting mode. Because the part of the plots with low values for the max_tasks_in_flight parameter is usually the more useful one, we also provide figures obtained by "zooming in" on that section of the plots.

##### Plots without Work Stealing
![Plot0](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-17-19:37:53_pipelining/plots/plot_task_throughput-0-WS-11-x_ticks.png)

Zooming in:

![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-17-19:37:53_pipelining/plots/plot_task_throughput-0-WS-9-x_ticks.png)

and:

![Plot0](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-17-19:37:53_pipelining/plots/plot_task_throughput-0-WS-5-x_ticks.png)


##### Plot with Eager Work Stealing

![Plot0](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-17-19:37:53_pipelining/plots/plot_task_throughput-1-WS-11-x_ticks.png)

Zooming in:

![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-17-19:37:53_pipelining/plots/plot_task_throughput-1-WS-9-x_ticks.png)

and:

![Plot0](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-17-19:37:53_pipelining/plots/plot_task_throughput-1-WS-5-x_ticks.png)


##### Plot without Eager Work Stealing

![Plot0](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-18-04:47:38_pipelining_eager-worker-requesting-OFF/plots/plot_task_throughput-1-WS-11-x_ticks.png)

Zooming in:

![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-18-04:47:38_pipelining_eager-worker-requesting-OFF/plots/plot_task_throughput-1-WS-9-x_ticks.png)

and:

![Plot0](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-05-18-04:47:38_pipelining_eager-worker-requesting-OFF/plots/plot_task_throughput-1-WS-5-x_ticks.png)


#### Data files
Each data file in the output folder is named using the template `data-<number1>-WS-<number2>-CPUS.txt`, where `<number1>` (which can only be 1 or 0) indicates whether Work Stealing (WS) was enabled, and `<number2>` indicates the number of CPUS used.

Each raw data file is divided into blocks, where each block corresponds to a specific value for the `max_tasks_in_flight` parameter. Each block contains a first line with an integer that records the `max_tasks_in_flight` (in number of tasks), followed by one line for each trial. Each such line contains a decimal number, which is the parallel execution time (in seconds) for the workload.


### A recent work stealing experiment

The experiment ran on a AWS `m4.16xlarge` machine with 64 cores. The experiment consisted of running several jobs under different settings, while keeping the total sequential execution time (i.e. the time it would take to run the job on a machine with only 1 core) constant and equal to 100s. 

We varied the following parameters:
* `max_tasks_in_flight_per_worker` parameter, which governs the size of the owner-to-worker pipelines, determining how many tasks can be in flight to each worker.
* the individual task duration, determining the duration of each task in the workload, as well as the total number of tasks. In particular, the number of tasks was determined by: ![formula](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/formula.png)
* the Ray `work_stealing` boolean parameter, determining whether work stealing is enabled or not.

Each combination of the aforementioned parameters defines a unique job. For example, a unique job could be one where the `max_tasks_in_flight_per_worker` is set to 64, the individual task duration is set to 500ms, and work stealing is enabled. Each unique job is repeated for a number of times, depending on the value of the `ntrials` parameter in the `run_work_stealing_eval.sh ` script. In this experiment, we let `ntrials` = 3. Each data point on the plots corresponds to a unique job, and it is computed by averaging the measurements obtained over the several trials (in our case, 3). The plots also show vertical bars that represent the standard deviation of the measurements (the bars are not visible in the plots below because the standard deviation is very small).

#### Plots
For each experiment, we provide two sets of plots. One has the individual task duration on the x-axis, the other has the max_tasks_in_flight_per_worker parameter on the x-axis. Both sets of plots are obtained from the same experiment.

##### Plos with the individual task duration on the x-axis
Each plot corresponds to a different setting for the `max_tasks_in_flight_per_worker` parameter. The values we used were: 1, 5, 20, 64, and 150. When `max_tasks_in_flight_per_worker`=1, task pipelining is not enabled, so the owner can only send one task at a time to each worker. In that case, work stealing is also not enabled.

The plots have two curves: a baseline curve (in blue), showing the performance of Ray when work stealing is not enabled and a second curve (in orange), showing the performance of Ray when work stealing is enabled. Each curve shows the parallel execution time of a workload as a function of the individual task duration. In particular, we used the following values for the individual task duration: 10ms, 50ms, 100ms, 500ms or 1000ms. 


![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-1-MTIF.png)

![Plot5](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-5-MTIF.png)

![Plot20](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-20-MTIF.png)

![Plot64](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-64-MTIF.png)

![Plot150](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/task_dur_x_axis/plot-150-MTIF.png)

##### Plos with the max_tasks_in_flight_per_worker on the x-axis
Each plot corresponds to a different setting for the duration of each task in the workload. The values used are: 10ms, 50ms, 100ms, 500ms or 1000ms.

The plots have two curves: a baseline curve (in blue), showing the performance of Ray when work stealing is not enabled and a second curve (in orange), showing the performance of Ray when work stealing is enabled. Each curve shows the parallel execution time of a workload as a function of the max tasks in flight. In particular, we used the following values for the individual task duration: 1, 5, 20, 64, and 150. 


![Plot1](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-10-ITD.png)

![Plot5](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-50-ITD.png)

![Plot100](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-100-ITD.png)

![Plot500](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-500-ITD.png)

![Plot1000](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/plots/max_tasks_in_flight_x_axis/plot-1000-ITD.png)

#### Data files
As described in the [experiment.info](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/experiment.info) file, each data file in the output folder is named using the template `data-<number1>-WS-<number2>-MTIF.txt`, where `<number1>` (which can only be 1 or 0) indicates whether Work Stealing (WS) was enabled and `<number2>` indicates the Maximum Number of Tasks (MTIF). For instance, the file [data-0-WS-150-MTIF.txt](https://github.com/gabrieleoliaro/ray_work_stealing_evaluation/blob/main/output/2021-04-23-03:08:34/data-0-WS-150-MTIF.txt) contains the data from the experiment where work stealing was not enabled (`<number1>`=0), and the `max_tasks_in_flight_per_worker` param was set to 150 tasks (`<number2>`=150).

Each raw data file is divided into blocks, where each block corresponds to a specific value for the individual task duration. Each block contains a first line with an integer that records the individual task duration (in milliseconds), followed by one line for each trial. Each such line contains a decimal number, which is the parallel execution time (in seconds) for the workload.
 
