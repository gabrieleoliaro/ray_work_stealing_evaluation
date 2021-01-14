import os, time, sys
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
	# Check that the number of tasks is passed as an argument
	if len(sys.argv) != 5:
		print("Usage: plot_results.py <ntrials> <n_task_duration_vals> <input_file> <output_file>")
		exit()

	# Validity check of the ntrials param
	try: ntrials = int(sys.argv[1])
	except:
		print("Number of trials parameter is not a valid integer")
		exit()
	if ntrials < 1 or ntrials > 20:
		print("Number of trials must be in the [1, 20] range")
		exit()
	print("Number of trials: {}".format(ntrials))

	# Validity check of the n_task_duration_vals param
	try: n_task_duration_vals = int(sys.argv[2])
	except:
		print("Number of task duration values parameter is not a valid integer")
		exit()
	if n_task_duration_vals < 1 or n_task_duration_vals > 20:
		print("Number of task duration values must be in the [1, 20] range")
		exit()
	print("Number of task duration values: {}".format(n_task_duration_vals))

	input_filename = sys.argv[3]
	assert(os.path.isfile(input_filename)) 
	output_filename = sys.argv[4]
	print("input_file: {}".format(input_filename))
	print("output_file: {}".format(output_filename))

	x0 = np.full(n_task_duration_vals, np.inf)
	x1 = np.full(n_task_duration_vals, np.inf)
	x2 = np.full(n_task_duration_vals, np.inf)
	y0 = np.full((n_task_duration_vals, 2), np.inf)
	y1 = np.full((n_task_duration_vals, 2), np.inf)
	y2 = np.full((n_task_duration_vals, 2), np.inf)
	with open(input_filename, 'r') as input_file:
		lines = input_file.readlines()
		line_index = 0
		# Work stealing not enabled
		for n in range(n_task_duration_vals):
			x0[n] = int(lines[line_index].strip().split()[0])
			line_index += 1
			temp = np.full(ntrials, np.inf)
			for trial in range(ntrials):
				temp[trial] = float(lines[line_index].strip().split()[0])
				line_index += 1
			#print(temp)
			y0[n,0] = np.mean(temp)
			y0[n,1] = np.std(temp)
		# Work stealing enabled
		for n in range(n_task_duration_vals):
			x1[n] = int(lines[line_index].strip().split()[0])
			line_index += 1
			temp = np.full(ntrials, np.inf)
			for trial in range(ntrials):
				temp[trial] = float(lines[line_index].strip().split()[0])
				line_index += 1
			#print(temp)
			y1[n,0] = np.mean(temp)
			y1[n,1] = np.std(temp)
		# Work stealing and eager workers requesting enabled
		for n in range(n_task_duration_vals):
			x2[n] = int(lines[line_index].strip().split()[0])
			line_index += 1
			temp = np.full(ntrials, np.inf)
			for trial in range(ntrials):
				temp[trial] = float(lines[line_index].strip().split()[0])
				line_index += 1
			#print(temp)
			y2[n,0] = np.mean(temp)
			y2[n,1] = np.std(temp)
	x0 = x0.astype(int)
	x1 = x1.astype(int)
	x2 = x2.astype(int)

	assert(np.all(x0 == x1))
	assert(np.all(x0 == x2))
	assert(np.all(x1 == x2))


	plt.figure()
	plt.errorbar(x0, y0[:,0], yerr=y0[:,1])
	plt.errorbar(x1, y1[:,0], yerr=y1[:,1])
	plt.errorbar(x2, y2[:,0], yerr=y2[:,1])

	plt.title("Parallel execution time vs task duration")
	plt.xticks(x0)
	plt.xlabel("Individual task duration (ms)")
	plt.ylabel("Total parallel execution time")
	plt.legend(("Baseline", "Work stealing enabled", "Work stealing + eager workers' requesting enabled"))
	plt.savefig(output_filename)
	plt.show()
