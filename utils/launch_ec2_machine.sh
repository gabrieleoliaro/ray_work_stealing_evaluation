if [ $1 -eq 1 ]; then
	ray up ./utils/ray_autoscaling.yaml ; 
	./utils/sync_ec2_with_local_folder.sh;
	ray attach ./utils/ray_autoscaling.yaml
elif [ $1 -eq 0 ]; then
	ray down ./utils/ray_autoscaling.yaml
else
	echo "type 1 to start the cluster, 0 to shut it down"
fi