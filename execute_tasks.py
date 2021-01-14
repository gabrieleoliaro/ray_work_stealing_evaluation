import os, time, sys, json, argparse
import ray



@ray.remote
def f(individual_task_duration):
    time.sleep(individual_task_duration)
    return 1


def int_type_seq_dur(l):
	# Validity check of the total sequential duration param
	try: seq_duration = int(l)
	except: raise argparse.ArgumentTypeError("Total sequential duration parameter is not a valid integer")
	
	if seq_duration < 1 or seq_duration > 1000:
		raise argparse.ArgumentTypeError("Sequential duration must be in the [1, 1000] range")
	return seq_duration

def int_type_task_dur_ms(l):
	# Validity check of the individual task duration param
	try: task_duration_ms = int(l)
	except: raise argparse.ArgumentTypeError("Individual task duration parameter is not a valid integer")
	
	if task_duration_ms < 1 or task_duration_ms > 10000:
		raise argparse.ArgumentTypeError("Individual task duration must be in the [1, 10000] range")
	return task_duration_ms

def int_type_ncpus(l):
	# Validity check of the ncpus param
	try: ncpus = int(l)
	except: raise argparse.ArgumentTypeError("Number of cpus parameter is not a valid integer")
	
	if ncpus < 1 or ncpus > 100:
		raise argparse.ArgumentTypeError("Number of cpus must be in the [1, 100] range")
	return ncpus

def int_type_max_tasks_in_flight(l):
	# Validity check of the max_tasks_in_flight param
	try: max_tasks_in_flight = int(l)
	except: raise argparse.ArgumentTypeError("max_tasks_in_flight parameter is not a valid integer")
	
	if max_tasks_in_flight < 1 or max_tasks_in_flight > 1000:
		raise argparse.ArgumentTypeError("max_tasks_in_flight must be in the [1, 1000] range")
	return max_tasks_in_flight

def int_type_work_stealing_enabled(l):
	# Validity check of the max_tasks_in_flight param
	try: work_stealing_enabled = int(l)
	except: raise argparse.ArgumentTypeError("work_stealing_enabled parameter is not a valid integer")
	
	if work_stealing_enabled != 1 and work_stealing_enabled != 0:
		raise argparse.ArgumentTypeError("work_stealing_enabled must be either 0 or 1")
	return work_stealing_enabled



if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--total_sequential_duration', type=int_type_seq_dur, default=100, help="the total sequential duration in seconds")
	parser.add_argument('-i', '--individual_task_duration', type=int_type_task_dur_ms, required=True, help="the individual task duration in milliseconds")
	parser.add_argument('-c', '--ncpus', type=int_type_ncpus, required=True, help="the number of cores to use in the experiment")
	parser.add_argument('-p', '--max_tasks_in_flight', type=int_type_max_tasks_in_flight, required=True, help="the maximum number of tasks that can be in flight to a worker")
	parser.add_argument('-w', '--work_stealing_enabled', type=int_type_work_stealing_enabled, required=True, help="whether work stealing should be enabled")
	parser.add_argument('-o', '--output_filename', required=True, help="the filepath to the output filename")

	args = parser.parse_args()

	print("Total sequential duration: {}".format(args.total_sequential_duration))
	print("Individual task duration: {}".format(args.individual_task_duration))
	print("Number of cpus: {}".format(args.ncpus))
	print("max_tasks_in_flight: {}".format(args.max_tasks_in_flight))
	print("work_stealing_enabled: {}".format(args.work_stealing_enabled))

	# # Check if we are logging the debug info or not
	# if "RAY_BACKEND_LOG_LEVEL" not in os.environ:
	# 	print("RAY_BACKEND_LOG_LEVEL not set!")
	# else:
	# 	print("RAY_BACKEND_LOG_LEVEL set to {}".format(os.environ['RAY_BACKEND_LOG_LEVEL']))


	task_duration = args.individual_task_duration / 1000.0
	
	# Compute total number of tasks
	ntasks = int(args.total_sequential_duration / task_duration)
	print("Number of tasks: {}".format(ntasks))

	# Create config
	# config = json.dumps({
	# 	"max_tasks_in_flight_per_worker":args.max_tasks_in_flight,
	# 	"work_stealing_enabled":args.work_stealing_enabled
	# })

	config = {}
	config["max_tasks_in_flight_per_worker"] = args.max_tasks_in_flight
	config["work_stealing"] = args.work_stealing_enabled

	ray.init(num_cpus=args.ncpus,_system_config=config)
	#ray.init(_system_config=config)
	time.sleep(1.0)

	start = time.time()
	futures = [f.remote(task_duration) for i in range(ntasks)]
	res = ray.get(futures)
	end = time.time()
	
	time_taken = end-start
	
	with open(args.output_filename, "a") as output_file:
    		output_file.write("{}\n".format(time_taken))
	
	ray.shutdown()