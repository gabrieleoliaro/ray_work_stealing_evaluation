if [ $1 -eq 0 ]; then
	echo "Running the pipelining evaluation with instantaneous tasks"

	## Parameters of the experiment
	# Fixed parameters (same for all jobs):
	ntrials=3
	total_n_tasks=50000
	#Variable parameters (different for different jobs)
	max_tasks_in_flight_vals=(1 2 3 4 5 10 15 20 25 50 100)
	ncpus=(1 2 5 10 15 20 35 50 64) #Expressed in milliseconds.


	# Create a new folder for the data
	timestamp=$(date +%Y-%m-%d-%T)
	output_path="output/${timestamp}_pipelining"
	mkdir -p $output_path
	# Save experiment info in experiment.info file
	exp_info_file="${output_path}/experiment.info"
	echo "Experiment parameters:" > $exp_info_file
	echo "ntrials=$ntrials" >> $exp_info_file
	echo "total_n_tasks=$total_n_tasks" >> $exp_info_file
	echo "max_tasks_in_flight_vals=(${max_tasks_in_flight_vals[*]})" >> $exp_info_file
	echo "ncpus=(${ncpus[*]})" >> $exp_info_file
	echo "" >> $exp_info_file
	echo "Experiment files:" >> $exp_info_file
	echo "each file represents a job and it is named as follows: data-<number1>-WS-<number2>-CPUS.txt, where <number1> (which can only be 1 or 0) indicates whether Work Stealing (WS) was enabled and <number2> indicates the number of CPUS used" >> $exp_info_file


	#export RAY_BACKEND_LOG_LEVEL=debug

	work_stealing_options=(1 0)
	for work_stealing in ${work_stealing_options[@]}; do
		for cpus in ${ncpus[@]}; do
			output_file="${output_path}/data-${work_stealing}-WS-${cpus}-CPUS.txt"
			for max_tasks_in_flight in ${max_tasks_in_flight_vals[@]}; do
				echo ${max_tasks_in_flight} >> ${output_file}
				for (( i=0; i<$ntrials; ++i)); do
					timeout 200s python instantaneous_tasks.py -n ${total_n_tasks} -c ${cpus} -p ${max_tasks_in_flight} -w ${work_stealing} -o ${output_file} -d 0
					ray stop --force
				done
			done
		done
	done


	cd ${output_path} && mkdir -p plots && cd ../..
	python plot_pipelining.py -t ${ntrials} -p "${max_tasks_in_flight_vals[*]}" -n ${total_n_tasks} -c "${ncpus[*]}" -x 9 -o ${output_path}

elif [ $1 -eq 1 ]; then
	echo "Running the pipelining evaluation with long tasks (duration=1000ms)"

	## Parameters of the experiment
	# Fixed parameters (same for all jobs):
	ntrials=3
	total_n_tasks=64
	#Variable parameters (different for different jobs)
	max_tasks_in_flight_vals=(1 2 3 4 5 10 15 20 25 50 100)
	ncpus=64 #Expressed in milliseconds.

	# Create a new folder for the data
	timestamp=$(date +%Y-%m-%d-%T)
	output_path="output/${timestamp}_pipelining"
	mkdir -p $output_path
	# Save experiment info in experiment.info file
	exp_info_file="${output_path}/experiment.info"
	echo "Experiment parameters:" > $exp_info_file
	echo "ntrials=$ntrials" >> $exp_info_file
	echo "total_n_tasks=${total_n_tasks}" >> $exp_info_file
	echo "max_tasks_in_flight_vals=(${max_tasks_in_flight_vals[*]})" >> $exp_info_file
	echo "ncpus=${total_n_tasks}" >> $exp_info_file
	echo "" >> $exp_info_file
	echo "Experiment files:" >> $exp_info_file
	echo "each file represents a job and it is named as follows: data-long_tasks-<number1>-WS.txt, where <number1> (which can only be 1 or 0) indicates whether Work Stealing (WS) was enabled." >> $exp_info_file


	work_stealing_options=(1 0)
	for work_stealing in ${work_stealing_options[@]}; do
		output_file="${output_path}/data-long_tasks-${work_stealing}-WS.txt"
		for max_tasks_in_flight in ${max_tasks_in_flight_vals[@]}; do
			echo ${max_tasks_in_flight} >> ${output_file}
			for (( i=0; i<$ntrials; ++i)); do
				timeout 200s python variable_length_tasks.py -s ${total_n_tasks} -i 1000 -c ${total_n_tasks} -p ${max_tasks_in_flight} -w ${work_stealing} -o ${output_file} -d 0
				ray stop --force
			done
		done
	done
else
	echo "Usage ./run_pipelining_eval.sh <mode>"
	exit
fi