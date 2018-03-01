import argparse
import subprocess

#processing arguments
parser = argparse.ArgumentParser()
parser.add_argument('-n', metavar='i', default=50, type=int, help='Number of processes to spawn')
args = parser.parse_args()

command = "node wallet.js --debug > log{}.txt"

numProcess = args.n

bash = ""
for i in range(numProcess - 1):
    bash += "{} &\n".format(command.format(i))

bash += command.format(numProcess - 1) #final line shouldn't have & at end

with open("spawn.sh", "w") as file:
    file.write(bash) #writing that list of commands to a file

subprocess.run(["chmod", "+x", "spawn.sh"]) #make that file executable

#subprocess.call("./spawn.sh", shell=True) #run and wait
