import os, time, sys,argparse
import numpy as np
import matplotlib.pyplot as plt

def int_type_ntrials(l):
	# Validity check of the ntrials param
	try: ntrials = int(l)
	except: raise argparse.ArgumentTypeError("Number of trials parameter is not a valid integer")
	
	if ntrials < 1 or ntrials > 20:
		raise argparse.ArgumentTypeError("Number of trials must be in the [1, 20] range")
	return ntrials

def int_type_seq_dur(l):
	# Validity check of the total sequential duration param
	try: seq_duration = int(l)
	except: raise argparse.ArgumentTypeError("Total sequential duration parameter is not a valid integer")
	
	if seq_duration < 1 or seq_duration > 1000:
		raise argparse.ArgumentTypeError("Sequential duration must be in the [1, 1000] range")
	return seq_duration


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--ntrials', type=int_type_ntrials, required=True, help="the number of trials used in the experiment")
	parser.add_argument('-p', '--max_tasks_in_flight', type=str, required=True, help="the max tasks in flight values (delimited list input)")
	parser.add_argument('-s', '--total_sequential_duration', type=int_type_seq_dur, required=True, help="the total sequential duration in seconds")
	parser.add_argument('-i', '--individual_task_duration', type=str, required=True, help="the individual task duration in milliseconds (delimited list input)")
	parser.add_argument('-o', '--data_folder', required=True, help="the path to the data folder")
	args = parser.parse_args()

	ntrials = args.ntrials
	max_tasks_in_flight_vals = [int(item) for item in args.max_tasks_in_flight.split()]
	seq_duration = args.total_sequential_duration
	task_duration_vals = [int(item) for item in args.individual_task_duration.split()]
	data_folder = args.data_folder
	
	print("Number of trials: {}".format(ntrials))
	print("Max tasks in flight: ", max_tasks_in_flight_vals)
	print("Sequential duration: {}".format(seq_duration))
	print("Task duration values: ", task_duration_vals)
	print("Data folder path: ", data_folder)

	# Define x axis to be the list of individual task durations considered in the experiments 
	# (i.e. the time taken to execute each task on its own).
	X = np.array(task_duration_vals).astype(int)
	
	# Each cell of the Y arrays is 2-dimensional and it contains the (mean, stdv) of the parallel
	# execution time across the various trials of a given experiment. The first dimension of Y
	# corresponds to the max_tasks_in_flight value used for a certain experiment. The second dimension
	# of Y corresponds to the duration each task, taken individually, in a certain experiment. Finally,
	# the third dimension is used to store the (mean,stdv) of the results of a given experiment, as described above.

	# Y0 contains the values corresponding to an execution with work stealing not enabled. In Y1, on the
	# other hand, work stealing is enabled.
	Y0 = np.full((len(max_tasks_in_flight_vals), len(task_duration_vals), 2), np.inf)
	Y1 = np.full((len(max_tasks_in_flight_vals), len(task_duration_vals), 2), np.inf)

	
	# We fill the Y array by iterating over the max_tasks_in_flight (first dimension of Y) because
	# values for different max_tasks_in_flight are in different files
	a=0
	for tasks_in_flight in max_tasks_in_flight_vals:
		
		work_stealing = 0
		data_filepath = "{}/data-{}-WS-{}-MTIF.txt".format(data_folder, work_stealing, tasks_in_flight)
		print("Opening input_file: {}".format(data_filepath))
		assert(os.path.isfile(data_filepath))
		with open(data_filepath, 'r') as input_file:
			lines = input_file.readlines()
			line_index = 0
			for b in range(len(X)):
				assert(int(lines[line_index].strip().split()[0]) == X[b])
				line_index += 1
				temp = np.full(ntrials, np.inf)
				for trial in range(ntrials):
					temp[trial] = float(lines[line_index].strip().split()[0])
					if (temp[trial] == -1):
						temp[trial] = np.nan
					line_index += 1
				#print(temp)
				Y0[a,b,0] = np.mean(temp)
				Y0[a,b,1] = np.std(temp)

		work_stealing = 1
		data_filepath = "{}/data-{}-WS-{}-MTIF.txt".format(data_folder, work_stealing, tasks_in_flight)
		assert(os.path.isfile(data_filepath))
		print("Opening input_file: {}".format(data_filepath))
		with open(data_filepath, 'r') as input_file:
			lines = input_file.readlines()
			line_index = 0
			for b in range(len(X)):
				assert(int(lines[line_index].strip().split()[0]) == X[b])
				line_index += 1
				temp = np.full(ntrials, np.inf)
				for trial in range(ntrials):
					temp[trial] = float(lines[line_index].strip().split()[0])
					line_index += 1
				#print(temp)
				Y1[a,b,0] = np.mean(temp)
				Y1[a,b,1] = np.std(temp)


		a+=1
	assert(a == len(max_tasks_in_flight_vals))
	
	######### Plots with individual task duration on X-axis #########
	a=0
	for tasks_in_flight in max_tasks_in_flight_vals:
		plt.figure()
		plt.errorbar(X, Y0[a,:,0], yerr=Y0[a,:,1])
		plt.errorbar(X, Y1[a,:,0], yerr=Y1[a,:,1])

		plt.title("Parallel execution time vs task duration \n Total Seq duration={}s, Max tasks in flight={}".format(seq_duration, tasks_in_flight))
		plt.xticks(X)
		plt.xlabel("Individual task duration (ms)")
		plt.ylabel("Total parallel execution time")
		plt.legend(("Baseline", "Work stealing enabled"))
		plot_filepath = "{}/plots/task_dur_x_axis/plot-{}-MTIF.png".format(data_folder, tasks_in_flight)
		plt.savefig(plot_filepath)
		plt.show()
		a+=1
	assert(a == len(max_tasks_in_flight_vals))

	X = np.array(max_tasks_in_flight_vals).astype(int)
	######### Plots with max_tasks_in_flight  on X-axis #########
	for b in range(len(X)):
		plt.figure()
		plt.errorbar(X, Y0[:,b,0], yerr=Y0[:,b,1])
		plt.errorbar(X, Y1[:,b,0], yerr=Y1[:,b,1])

		plt.title("Parallel execution time vs max_tasks_in_flight \n Total Seq duration={}s, Individual task duration={}ms".format(seq_duration, X[b]))
		plt.xticks(X)
		plt.xlabel("Max Tasks in Flight")
		plt.ylabel("Total parallel execution time")
		plt.legend(("Baseline", "Work stealing enabled"))
		plot_filepath = "{}/plots/max_tasks_in_flight_x_axis/plot-{}-ITD.png".format(data_folder, X[b])
		plt.savefig(plot_filepath)
		plt.show()


	