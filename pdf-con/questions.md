Assessment 1: Linux Fundamentals

MCQ 1

Which command is used to display the files and directories in the current directory?

A. cd
B. ls
C. pwd
D. mkdir

Answer: B. ls

⸻

MCQ 2

What does the pwd command show?

A. Current user’s password
B. Running processes
C. Current working directory
D. Previous directory

Answer: C. Current working directory

⸻

MCQ 3

Which command is used to change file permissions?

A. chmod
B. chdir
C. passwd
D. chown

Answer: A. chmod

⸻

MCQ 4

Which command can be used to view running processes?

A. ls
B. ps
C. mkdir
D. touch

Answer: B. ps

⸻

Lab 1: File & Directory Operations

Create the following structure:

devops/
├── linux/
│   ├── notes.txt
│   └── commands.txt
└── scripts/
    └── test.sh

Students should:

1. Create the directories.
2. Create the files.
3. Add some text to notes.txt.
4. Display the contents.
5. Show the complete directory structure.
6. Delete test.sh.

Expected commands may include:

mkdir -p devops/linux devops/scripts
touch devops/linux/notes.txt
touch devops/linux/commands.txt
touch devops/scripts/test.sh
echo "Linux Fundamentals" > devops/linux/notes.txt
cat devops/linux/notes.txt
ls -R devops
rm devops/scripts/test.sh

⸻

Lab 2: Permissions

Create a file called:

student.txt

Give the owner read and write permission, while giving the group and others only read permission.

Then verify the permission.

Expected permission:

-rw-r--r--

Possible command:

chmod 644 student.txt
ls -l student.txt

⸻

Assessment 2: Networking Fundamentals

MCQ 1

Which protocol is mainly used to translate domain names such as google.com into IP addresses?

A. HTTP
B. DNS
C. FTP
D. SSH

Answer: B. DNS

⸻

MCQ 2

Which of the following is a private IP address?

A. 8.8.8.8
B. 1.1.1.1
C. 192.168.1.10
D. 142.250.183.14

Answer: C. 192.168.1.10

⸻

MCQ 3

Which protocol provides reliable, connection-oriented communication?

A. UDP
B. TCP
C. DNS
D. ICMP

Answer: B. TCP

⸻

MCQ 4

A web application is running on port 8080. What does 8080 represent?

A. IP address
B. MAC address
C. Port number
D. DNS server

Answer: C. Port number

⸻

Lab 1: Network Investigation

Run the following commands:

ip addr
ip route
ping google.com

Students should identify:

1. Their machine’s IP address.
2. The default gateway.
3. Whether the machine can reach google.com.
4. The IP address resolved for google.com.

⸻

Lab 2: Port Investigation

Start a simple web server:

python3 -m http.server 8000

Then open:

http://localhost:8000

Students should explain:

* What is localhost?
* What is 8000?
* Which application is listening on the port?
* How can they check the listening port?

For example:

ss -lntp

⸻

Assessment 3: Shell Scripting

MCQ 1

Which symbol is used to access the value of a shell variable?

A. #
B. $
C. @
D. %

Answer: B. $

⸻

MCQ 2

What does $1 represent in a shell script?

A. Script name
B. First command
C. First command-line argument
D. First variable

Answer: C. First command-line argument

⸻

MCQ 3

Which symbol is commonly used to redirect command output to a file?

A. >
B. <
C. |
D. &&

Answer: A. >

⸻

MCQ 4

What is the purpose of a loop in a shell script?

A. To delete files
B. To repeat a set of commands
C. To create users
D. To change permissions

Answer: B. To repeat a set of commands

⸻

Lab 1: Simple Shell Script

Create a script called:

system_info.sh

The script should display:

Hello DevOps Student!
Current User:
Current Directory:
Hostname:
Date:

Students should use appropriate Linux commands to generate the information.

Example:

#!/bin/bash
echo "Hello DevOps Student!"
echo "Current User: $(whoami)"
echo "Current Directory: $(pwd)"
echo "Hostname: $(hostname)"
echo "Date: $(date)"

⸻

Lab 2: Number Checker

Create a script:

check_number.sh

The script should accept a number as an argument.

Example:

./check_number.sh 10

Output:

10 is a positive number

If the user provides:

./check_number.sh -5

Output:

-5 is a negative number

This checks their understanding of arguments + variables + conditions.

Bash supports variables, arguments, conditions, loops, functions, and redirection as core shell-scripting features.  

⸻

Assessment 4: Git & GitHub

MCQ 1

Which command initializes a new Git repository?

A. git start
B. git init
C. git create
D. git repo

Answer: B. git init

⸻

MCQ 2

Which command shows the current Git repository status?

A. git check
B. git status
C. git show-status
D. git current

Answer: B. git status

⸻

MCQ 3

What is the purpose of a Git branch?

A. To delete the repository
B. To create an independent line of development
C. To upload files to Linux
D. To install Git

Answer: B. To create an independent line of development

⸻

MCQ 4

Which command downloads a remote repository to your local machine?

A. git clone
B. git download
C. git pull-only
D. git copy

Answer: A. git clone

⸻

Lab 1: Basic Git Workflow

Create a Git repository and perform the following:

mkdir student-project
cd student-project
git init

Create:

README.md

Then:

1. Add some content.
2. Check Git status.
3. Stage the file.
4. Create a commit.
5. Check the commit history.

Expected workflow:

git status
git add README.md
git commit -m "Add README"
git log --oneline

⸻

Lab 2: Branching

Starting from the previous repository:

1. Create a branch called feature.
2. Switch to the branch.
3. Create feature.txt.
4. Commit the file.
5. Switch back to the main branch.
6. Merge the feature branch.

Example:

git branch feature
git switch feature
touch feature.txt
git add feature.txt
git commit -m "Add feature"
git switch main
git merge feature

Bonus question: Ask students to explain what happened to feature.txt after the merge.

⸻

Assessment 5: Docker Fundamentals

MCQ 1

What is the main purpose of Docker?

A. To replace Git
B. To package and run applications in containers
C. To create virtual machines only
D. To manage Linux users

Answer: B. To package and run applications in containers

⸻

MCQ 2

Which component manages Docker objects such as containers, images, networks, and volumes?

A. Docker daemon
B. Git daemon
C. Linux kernel only
D. Docker Hub

Answer: A. Docker daemon

⸻

MCQ 3

Which command displays currently running containers?

A. docker images
B. docker ps
C. docker list
D. docker running

Answer: B. docker ps

⸻

MCQ 4

What is Docker Hub primarily used for?

A. Storing and sharing container images
B. Managing Linux permissions
C. Creating Git branches
D. Monitoring CPU usage

Answer: A. Storing and sharing container images

Docker describes the Docker client, daemon, registries, images, containers, networks, and volumes as core parts of its platform.  

⸻

Lab 1: Run Your First Container

Run an Nginx container:

docker run -d --name my-nginx nginx

Students should:

1. Check the running container.
2. View the container.
3. Stop it.
4. Start it again.
5. Remove it.

Commands:

docker ps
docker ps -a
docker stop my-nginx
docker start my-nginx
docker rm my-nginx

⸻

Lab 2: Run an Interactive Container

Run an Ubuntu container:

docker run -it ubuntu bash

Inside the container, execute:

whoami
pwd
ls

Then exit:

exit

Ask students:

What happened to the container after you exited?

This is a very good confidence-building question because students get to see the difference between a running container and a stopped container.

⸻

Assessment 6: Docker Images & Containers

MCQ 1

What is a Docker image?

A. A running application
B. A read-only template used to create containers
C. A network
D. A volume

Answer: B. A read-only template used to create containers

⸻

MCQ 2

Which command lists Docker images available locally?

A. docker image ls
B. docker container ls
C. docker image show
D. docker list-images-only

Answer: A. docker image ls

⸻

MCQ 3

Which file is commonly used to define instructions for building a Docker image?

A. docker.yaml
B. Dockerfile
C. container.txt
D. image.conf

Answer: B. Dockerfile

⸻

MCQ 4

What is the relationship between an image and a container?

A. Container creates the image automatically every time
B. Image is a running version of the container
C. Container is a runnable instance of an image
D. They are exactly the same thing

Answer: C. Container is a runnable instance of an image

Docker images are immutable packages containing the files, binaries, libraries, and configuration needed to run an application, while a container is a runnable instance of that image.  

⸻

Lab 1: Build Your Own Image

Create a simple HTML application.

Create:

index.html
Dockerfile

index.html:

<h1>Hello from My Docker Application!</h1>

Create a Dockerfile using Nginx as the base image.

Build the image:

docker build -t my-web-app .

Check:

docker images

Run it:

docker run -d -p 8080:80 --name web-app my-web-app

Open:

http://localhost:8080

⸻

Lab 2: Image & Container Investigation

Ask students to run:

docker images
docker ps
docker ps -a

Then answer:

1. Which image was used to create your container?
2. What is the container name?
3. What is the container ID?
4. What happens to the container when you run docker stop?
5. Can you start the same container again?

This tests understanding rather than command memorization.

⸻

Assessment 7: Docker Networking & Volumes

MCQ 1

Which option publishes a container port to the host?

A. -v
B. -p
C. -n
D. -h

Answer: B. -p

⸻

MCQ 2

Why would we use a Docker volume?

A. To increase CPU
B. To persist data outside the container’s writable layer
C. To create an image
D. To expose a port

Answer: B. To persist data outside the container

⸻

MCQ 3

Which command creates a Docker network?

A. docker network create mynet
B. docker create network mynet
C. docker network start mynet
D. docker net new mynet

Answer: A. docker network create mynet

⸻

MCQ 4

Two containers are connected to the same user-defined Docker network. What is a simple way for one container to communicate with the other?

A. Using the container name
B. Using only localhost
C. Using the host’s username
D. Using the Dockerfile name

Answer: A. Using the container name

Docker user-defined networks allow containers on the same network to communicate using container names, and published ports such as -p make container services accessible from the host.  

⸻

Lab 1: Container-to-Container Communication

Create a network:

docker network create my-network

Run two containers:

docker run -d --name container1 --network my-network nginx
docker run -it --name container2 --network my-network alpine sh

Inside container2, try to reach container1.

For example, install curl:

apk add curl

Then:

curl http://container1

Students should explain why container2 can communicate with container1.

⸻

Lab 2: Docker Volume

Create a volume:

docker volume create student-data

Run a container using the volume:

docker run -it --name volume-test \
  -v student-data:/data \
  ubuntu bash

Inside the container:

echo "Docker Persistent Data" > /data/test.txt
cat /data/test.txt
exit

Remove the container:

docker rm volume-test

Create another container using the same volume:

docker run -it \
  -v student-data:/data \
  ubuntu bash

Check:

cat /data/test.txt

Expected output:

Docker Persistent Data

Then ask:

The container was deleted. Why is the file still there?

Expected concept: The data was stored in the Docker volume, not only inside the container’s writable layer. Docker volumes are specifically designed for persistent container data.  

