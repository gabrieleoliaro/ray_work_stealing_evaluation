## Parameters of the experiment
# Fixed parameters (same for all jobs):
ncpus=64
ntrials=3
total_sequential_duration=100 #Expressed in seconds
#Variable parameters (different for different jobs)
max_tasks_in_flight_vals=(1 5 20 64 150)
individual_task_durations=(10 50 100 500 1000) #Expressed in milliseconds.


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
echo "each file represents a job and it is named as follows: data-<number1>-WS-<number2>-MTIF.txt, where <number1> (which can only be 1 or 0) indicates whether Work Stealing (WS) was enabled and <number2> indicates the Maximum Number of Tasks (MTIF)" >> $exp_info_file


#export RAY_BACKEND_LOG_LEVEL=debug

work_stealing_options=(0 1)
for work_stealing in ${work_stealing_options[@]}; do
	for max_tasks_in_flight in ${max_tasks_in_flight_vals[@]}; do
		output_file="${output_path}/data-${work_stealing}-WS-${max_tasks_in_flight}-MTIF.txt"
		for task_duration in ${individual_task_durations[@]}; do
			echo ${task_duration} >> ${output_file}
			for (( i=0; i<$ntrials; ++i)); do
				timeout 200s python execute_tasks.py -s ${total_sequential_duration} -i ${task_duration} -c ${ncpus} -p ${max_tasks_in_flight} -w ${work_stealing} -o ${output_file} -d 1
				ray stop --force
			done
		done
	done
done


cd ${output_path} && mkdir plots && cd ../..
python plot_results.py -t ${ntrials} -p "${max_tasks_in_flight_vals[*]}" -s ${total_sequential_duration} -i "${individual_task_durations[*]}" -o ${output_path}