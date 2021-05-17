import os, time, sys, json, argparse
import ray

# Instantaneous task
@ray.remote
def f():
    return 1


def int_type_total_n_tasks(l):
	# Validity check of the total number of tasks param
	try: seq_duration = int(l)
	except: raise argparse.ArgumentTypeError("Total number of tasks parameter is not a valid integer")
	
	if seq_duration < 1 or seq_duration > 1000000:
		raise argparse.ArgumentTypeError("Sequential duration must be in the [1, 1000000] range")
	return seq_duration


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

def int_type_debug_logging_mode(l):
	try: debug_logging_mode = int(l)
	except: raise argparse.ArgumentTypeError("debug_logging_mode parameter is not a valid integer ")
	
	if debug_logging_mode != 1 and debug_logging_mode != 0:
		raise argparse.ArgumentTypeError("debug_logging_mode must be either 0 or 1")
	return debug_logging_mode



if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--total_n_tasks', type=int_type_total_n_tasks, default=10000, help="the total number of instantaneous tasks to execute")
	parser.add_argument('-c', '--ncpus', type=int_type_ncpus, required=True, help="the number of cores to use in the experiment")
	parser.add_argument('-p', '--max_tasks_in_flight', type=int_type_max_tasks_in_flight, required=True, help="the maximum number of tasks that can be in flight to a worker")
	parser.add_argument('-w', '--work_stealing_enabled', type=int_type_work_stealing_enabled, required=True, help="whether work stealing should be enabled")
	parser.add_argument('-o', '--output_filename', required=True, help="the filepath to the output filename")
	parser.add_argument('-d', '--debug_logging_mode', default=0, type=int_type_debug_logging_mode, help="request that Ray logs additional debugging information")
	args = parser.parse_args()

	print("Total number of tasks: {}".format(args.total_n_tasks))
	print("Number of cpus: {}".format(args.ncpus))
	print("max_tasks_in_flight: {}".format(args.max_tasks_in_flight))
	print("work_stealing_enabled: {}".format(args.work_stealing_enabled))
	print("debug_logging_mode: {}".format(args.debug_logging_mode))

	if args.debug_logging_mode == 1:
		os.environ['RAY_BACKEND_LOG_LEVEL'] = 'debug'
	else:
		if "RAY_BACKEND_LOG_LEVEL" in os.environ:
			del os.environ['RAY_BACKEND_LOG_LEVEL']

	# Check if we are logging the debug info or not
	if "RAY_BACKEND_LOG_LEVEL" not in os.environ:
		print("RAY_BACKEND_LOG_LEVEL not set!")
	else:
		print("RAY_BACKEND_LOG_LEVEL set to {}".format(os.environ['RAY_BACKEND_LOG_LEVEL']))


	config = {}
	config["max_tasks_in_flight_per_worker"] = args.max_tasks_in_flight
	config["work_stealing"] = args.work_stealing_enabled

	ray.init(num_cpus=args.ncpus,_system_config=config)
	#ray.init(_system_config=config)
	time.sleep(1.0)

	ntasks = args.total_n_tasks

	start = time.time()
	futures = [f.remote() for i in range(ntasks)]
	res = ray.get(futures)
	end = time.time()
	
	time_taken = end-start
	
	with open(args.output_filename, "a") as output_file:
    		output_file.write("{}\n".format((float(ntasks))/time_taken))
	
	ray.shutdown()