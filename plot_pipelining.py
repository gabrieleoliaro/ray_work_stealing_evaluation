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

def int_type_total_n_tasks(l):
	# Validity check of the total number of tasks param
	try: seq_duration = int(l)
	except: raise argparse.ArgumentTypeError("Total number of tasks parameter is not a valid integer")
	
	if seq_duration < 1 or seq_duration > 1000000:
		raise argparse.ArgumentTypeError("Sequential duration must be in the [1, 1000000] range")
	return seq_duration


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--ntrials', type=int_type_ntrials, required=True, help="the number of trials used in the experiment")
	parser.add_argument('-p', '--max_tasks_in_flight', type=str, required=True, help="the max tasks in flight values (delimited list input)")
	parser.add_argument('-n', '--total_n_tasks', type=int_type_total_n_tasks, required=True, help="the total number of instantaneous tasks to execute")
	parser.add_argument('-c', '--ncpus', type=str, required=True, help="the number of cores used (delimited list input)")
	parser.add_argument('-o', '--data_folder', required=True, help="the path to the data folder")
	args = parser.parse_args()

	ntrials = args.ntrials
	max_tasks_in_flight_vals = [int(item) for item in args.max_tasks_in_flight.split()]
	total_n_tasks = args.total_n_tasks
	ncpus = [int(item) for item in args.ncpus.split()]
	data_folder = args.data_folder
	
	print("Number of trials: {}".format(ntrials))
	print("Max tasks in flight: ", max_tasks_in_flight_vals)
	print("Total Number of Tasks: {}".format(total_n_tasks))
	print("Number of cores values: ", ncpus)
	print("Data folder path: ", data_folder)

	# Define x axis to be the list of max_tasks_in_flight_vals considered in the experiments 
	X = np.array(max_tasks_in_flight_vals).astype(int)
	print("X: ", X)

	P = len(max_tasks_in_flight_vals)
	assert(P==len(X))
	C = len(ncpus)

	Y0 = np.full((C,P, 2), np.inf)
	Y1 = np.full((C,P, 2), np.inf)
	print(np.shape(Y0), np.shape(Y1))

	for a in range(C):
		work_stealing = 0
		data_filepath = "{}/data-{}-WS-{}-CPUS.txt".format(data_folder, work_stealing, ncpus[a])
		print("Opening input file: {}".format(input_filename))
		assert(os.path.isfile(input_filename))
		with open(input_filename, 'r') as input_file:
			lines = input_file.readlines()
			line_index = 0
			for b in range(P):
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
		data_filepath = "{}/data-{}-WS-{}-CPUS.txt".format(data_folder, work_stealing, ncpus[a])
		print("Opening input file: {}".format(input_filename))
		assert(os.path.isfile(input_filename))
		with open(input_filename, 'r') as input_file:
			lines = input_file.readlines()
			line_index = 0
			for b in range(P):
				assert(int(lines[line_index].strip().split()[0]) == X[b])
				line_index += 1
				temp = np.full(ntrials, np.inf)
				for trial in range(ntrials):
					temp[trial] = float(lines[line_index].strip().split()[0])
					if (temp[trial] == -1):
						temp[trial] = np.nan
					line_index += 1
				#print(temp)
				Y1[a,b,0] = np.mean(temp)
				Y1[a,b,1] = np.std(temp)



	# Generate Work Stealing = false plot
	plt.figure()
	for a in range(C):
		plt.errorbar(X, Y0[a,:,0], yerr=Y0[a,:,1])

	plt.title("Task throughput vs max_tasks_in_flight \n NTasks={}, Task duration: instantaneous".format(total_n_tasks))
	plt.xticks(X)
	plt.xlabel("Max Tasks in Flight to workers")
	plt.ylabel("Task throughput (task/second)")
	plt.legend(ncpus)
	plot_filepath = "{}/plots/plot_task_throughput-0-WS.png".format(data_folder)
	plt.savefig(plot_filepath)
	print("Saving {}".format(plot_filepath))
	plt.show()
	


	# Generate Work Stealing = true plot
	plt.figure()
	for a in range(C):
		plt.errorbar(X, Y1[a,:,0], yerr=Y1[a,:,1])

	plt.title("Task throughput vs max_tasks_in_flight \n NTasks={}, Task duration: instantaneous".format(total_n_tasks))
	plt.xticks(X)
	plt.xlabel("Max Tasks in Flight to workers")
	plt.ylabel("Task throughput (task/second)")
	plt.legend(ncpus)
	plot_filepath = "{}/plots/plot_task_throughput-1-WS.png".format(data_folder)
	plt.savefig(plot_filepath)
	print("Saving {}".format(plot_filepath))
	plt.show()


	