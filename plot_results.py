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

	# Define x axis to be the list of sequential durations
	X = np.array(task_duration_vals).astype(int)
	
	# For each value in the max tasks in flight, open corresponding file (for WS=0 or WS=1), create y axis by computing average and std (based on ntrials), then plot

	for tasks_in_flight in max_tasks_in_flight_vals:
		Y0 = np.full((len(task_duration_vals), 2), np.inf)
		Y1 = np.full((len(task_duration_vals), 2), np.inf)
		
		work_stealing = 0
		data_filepath = "{}/data-{}-WS-{}-MTIF.txt".format(data_folder, work_stealing, tasks_in_flight)
		print("Opening input_file: {}".format(data_filepath))
		assert(os.path.isfile(data_filepath))
		with open(data_filepath, 'r') as input_file:
			lines = input_file.readlines()
			line_index = 0
			for x in range(len(X)):
				assert(int(lines[line_index].strip().split()[0]) == X[x])
				line_index += 1
				temp = np.full(ntrials, np.inf)
				for trial in range(ntrials):
					temp[trial] = float(lines[line_index].strip().split()[0])
					line_index += 1
				#print(temp)
				Y0[x,0] = np.mean(temp)
				Y0[x,1] = np.std(temp)

		work_stealing = 1
		data_filepath = "{}/data-{}-WS-{}-MTIF.txt".format(data_folder, work_stealing, tasks_in_flight)
		assert(os.path.isfile(data_filepath))
		print("Opening input_file: {}".format(data_filepath))
		with open(data_filepath, 'r') as input_file:
			lines = input_file.readlines()
			line_index = 0
			for x in range(len(X)):
				assert(int(lines[line_index].strip().split()[0]) == X[x])
				line_index += 1
				temp = np.full(ntrials, np.inf)
				for trial in range(ntrials):
					temp[trial] = float(lines[line_index].strip().split()[0])
					line_index += 1
				#print(temp)
				Y1[x,0] = np.mean(temp)
				Y1[x,1] = np.std(temp)

		Y0 = Y0.astype(int)
		Y1 = Y1.astype(int)


		plt.figure()
		plt.errorbar(X, Y0[:,0], yerr=Y0[:,1])
		plt.errorbar(X, Y1[:,0], yerr=Y1[:,1])

		plt.title("Parallel execution time vs task duration \n Total Seq duration={}, Max tasks in flight={}".format(seq_duration, tasks_in_flight))
		plt.xticks(X)
		plt.xlabel("Individual task duration (ms)")
		plt.ylabel("Total parallel execution time")
		plt.legend(("Baseline", "Work stealing enabled"))
		plot_filepath = "{}/plots/plot-{}-MTIF.png".format(data_folder, tasks_in_flight)
		plt.savefig(plot_filepath)
		plt.show()
