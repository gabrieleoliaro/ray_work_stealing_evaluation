## Parameters of the experiment
# Fixed parameters (same for all jobs):
ncpus=64
ntrials=5
total_sequential_duration=10 #Expressed in seconds
# Variable parameters (different for different jobs)
max_tasks_in_flight_vals=(1 2 5 10 15 20 25 30 50 64 80 100 150)
individual_task_durations=(1 10 50 100 500 1000) #Expressed in milliseconds.

# Create a new folder for the data
timestamp=$(date +%Y-%m-%d-%T)
output_path="output/${timestamp}"
mkdir -p $output_path
# Save experiment info in experiment.info file
exp_info_file="${output_path}/experiment.info"
echo "Experiment parameters:" > $exp_info_file
echo "ncpus=$ncpus" >> $exp_info_file
echo "ntrials=$ntrials" >> $exp_info_file
echo "total_sequential_duration=$total_sequential_duration" >> $exp_info_file
echo "max_tasks_in_flight_vals=(${max_tasks_in_flight_vals[*]})" >> $exp_info_file
echo "individual_task_durations=(${individual_task_durations[*]})" >> $exp_info_file
echo "" >> $exp_info_file
echo "Experiment files:" >> $exp_info_file
echo "each file represents a job and it is named as follows: data-<number1>-MTIF-<number2>-ITD-<number3>-WS.txt, where <number1> indicates the Maximum Number of Tasks In Flight (MTIF), <number2> indicates the Individual Task Duration (ITD) and <number3> (which can only be 1 or 0) indicates whether Work Stealing (WS) was enabled." >> $exp_info_file


# Work stealing not enabled
work_stealing_options=(0 1)
for work_stealing in ${work_stealing_options[@]}; do
	for max_tasks_in_flight in ${max_tasks_in_flight_vals[@]}; do
		for task_duration in ${individual_task_durations[@]}; do
			output_file="${output_path}/data-${max_tasks_in_flight}-MTIF-${task_duration}-ITD-${work_stealing}-WS.txt"
			for (( i=0; i<$ntrials; ++i)); do
				python execute_tasks.py -s ${total_sequential_duration} -i ${task_duration} -c ${ncpus} -p ${max_tasks_in_flight} -w ${work_stealing} -o ${output_file}
				ray stop -f
			done
		done
	done
done


#python plot_variable.py $ntrials ${#task_duration_vals[@]} $results_file $plot_file
