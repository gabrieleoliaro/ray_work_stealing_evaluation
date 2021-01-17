# Get IP and username of remote EC2 instance
read -p 'Type username@ip_address to connect to the EC2 machine and sync the main folder: ' user_and_ip

mkdir -p ec2/main ec2/tmp

# Synchronize main folder
sudo sshfs $user_and_ip:/home/ubuntu ./ec2/main -o IdentityFile=~/.ssh/ray-autoscaler_1_us-east-2.pem -o allow_other

# Synchronize tmp folder
sudo sshfs $user_and_ip:/tmp/ray ./ec2/tmp -o IdentityFile=~/.ssh/ray-autoscaler_1_us-east-2.pem -o allow_other

# Open SSH connection
sudo ssh $user_and_ip
