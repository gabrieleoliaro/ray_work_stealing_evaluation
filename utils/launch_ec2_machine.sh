if [ $1 -eq 1 ]; then
	ray up ./utils/ray_autoscaling.yaml ; 
	ray attach ./utils/ray_autoscaling.yaml 
	#&& ./utils/syncronizer.sh && 
elif [ $1 -eq 0 ]; then
	ray down ./utils/ray_autoscaling.yaml
else
	echo "type 1 to start the cluster, 0 to shut it down"
fi