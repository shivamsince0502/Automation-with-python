import boto3
import os
import datetime
import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init()
aws_mag_conf = boto3.session.Session(aws_access_key_id='your access key', aws_secret_access_key='your key')
user_acc = boto3.resource('ec2',aws_access_key_id='your access key', aws_secret_access_key='your key')

def speak(audio):
    engine.say(audio) 
    engine.runAndWait() 
def takeCommand() :
    r=sr.Recognizer()
    with sr.Microphone() as source :
        print("Listening..")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(query)
    except Exception as e :
        print(e)
        speak("Say that again please")
        return "None"

def date() :
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)

def wishme() :
    speak("Hey there , Welcome back !!")
    hour = datetime.datetime.now().hour
    if hour>=6 and hour<12 :
        speak("Good morning")
    elif hour>=12 and hour<18 :
        speak("Good afternoon")
    elif hour>=18 and hour<24 :
        speak("Good evening")
    else :
        speak("Good night")
    speak("THOORS at your service , please tell me how can i help you")


def create_inst():
    os.system('aws ec2 run-instances --image-id ami-052c08d70def0ac62 --count 1 --instance-type t2.micro --key-name shivamarthwinkey --security-group-id sg-01d325649bfb179fc')
def vols():
    speak('Showing volumes')
    vol_info = aws_mag_conf.resource('ec2')
    for each_vol in vol_info.volumes.all():
        print(each_vol)
def snaps():
    speak('showing snapshots')
    snap_shts = aws_mag_conf.resource('ec2')
    for each_snap in snap_shts.snapshots.all():
        print(each_snap)
def all_images():
    speak('showing images')
    images_name = aws_mag_conf.resource('ec2')
    for each_image in images_name.images.all():
        print(each_image)
def iam():
    speak('showing list of iam users')
    iam_con = aws_mag_conf.resource('iam')
    for each_user in iam_con.users.all():
        print(each_user.name)
def instances():
    speak('showing instances you have launched')
    instances = aws_mag_conf.resource('ec2')
    for each_inst in instances.instances.all():
        id=each_inst
        print(each_inst," image id:",aws_mag_conf.Image(id))
def docker_start():
  print('starting docker services\n')
  speak('staring docker services')
  os.system('systemctl start docker')
def docker_cont_run():
  print('give os type of the container')
  speak('give os type of the container')
  print('say 1 for Centos:7 or 2 for Ubuntu:14.04')
  speak('Give the name os ')
  os_type = takeCommand()
  int(os_type)
  speak('give name of the container')
  name_cont = takeCommand()
  if os_type == 1:
    os.system(f"docker run -it --name {name_cont} Centos:7")
  else:
    os.system(f"docker run -it --name {name_cont} Ubuntu:14.04")
    os.system('docker run -it ')
def attach_dock():
  print('speak name of the os you want to use for the server service')
  name = takeCommand()
  os.system(f"docker attach {name}")
def runni_os():
  print('running the docker services\n')
  os.system('docker ps -a')
def start_server():
  print('starting the web services\n')
  os.system('systemctl start httpd')
  os.system('systemctl stop firewalld')
def start_nnode():
  print('starting namenode services\n')
  os.system('hadoop daemon.sh start namenode')
  print('namenode service started\n')
def start_node():
  print('staritng datanode services\n')
  os.system('hadoop-daemon.sh start datanode')
  print('datanode service started\n')
def stop_docker():
  print('stopping docker services\n')
  os.system('systemctl stop docker')
  print('stopping docker services\n')
def stop_httpd():
  print('stopping web server services\n')
  os.system('systemctl stop httpd')
  print('web server services stopped')
def install_docker():
  speak('installing docker-ce')
  print('installing docker-ce\n')
  os.system('yum install docker-ce --nobest')

def lvm(name_of_vg,count):
  count = count
  way = input("""
Press 1 to create LVM partition
Press 2 to resize the partition
Your choice: """)
way = int(way)
	if count==0:
		alphabet = "b"
	elif count==1:
		alphabet = "c"

	os.system("pvcreate  /dev/sd{}".format(alphabet))
	os.system("pvdisplay  /dev/sd{}".format(alphabet))
	os.system("vgcreate  {} /dev/sd{}".format(name_of_vg,alphabet))
	os.system("vgdisplay  {}".format(name_of_vg))
#3 steps you have  to do to use any storage
def creating_partition(name_of_vg, name_of_partition):
	number=input("Logical volume number : ")	
	print("creating logical volume")
	os.system("lvcreate  --size {}G --name {} {}".format(ch,name_of_partition,name_of_vg))
	os.system("mkfs.ext4 /dev/{}/{}".format(name_of_vg,name_of_partition))
	os.system("mkdir logical_volume{}".format(number))
	os.system("mount /dev/{}/{} 			logical_volume{}".format(name_of_vg,name_of_partition,number))
	#os.system("df  -h")
	os.system("clear")

if way==1:
	#Specify name to volume group 
	vg = input("Write the name of Volume group to be created: ")
		
	# system already has hard disk we have to just create physical volume of it
	count_of_phy_vol=input("How many external hard disk you have attached: ")	
	count = 0
	#Calling the function to make physical volume and volume group
	while count < int(count_of_phy_vol):	
		#count stores the times function is called		
		lvm(vg,count)
		os.system('clear')
		count += 1 
	partition_name = input("Write the name of logical volume: ")
	ch=input("Storage required (in GB): ")
	ch = int(ch)
	# calling function
	creating_partition(vg,partition_name)
	#info
	print("Logical volume of size {}G created".format(ch))
	#displaying lv
	#os.system("lvdisplay {}/{}".format(vg,partition_name))

elif way==2:
	vg = input("Enter the volume group name:" )
	partition_name=input("Enter the logical volume name: ")			
	# on the fly you want to  increase the storage
	volume=input("Storage required (in GB): ")
	os.system("lvextend  --size +{}G /dev/{}/{}".format(volume,vg,partition_name))
	# will format the storage part that is added to the existing partition 
	os.system("resize2fs /dev/{}/{}".format(vg,partition_name))
	os.system("clear")
  
if __name__ == "__main__":
   while True:
     wishme()
     speak('i am Torss give what can i do for you master')

     print('''
     1.Docker Commands
     2. web server Commands
     3. Hadoop Commands
     4. AWS services Commands
     5. logical volume group''')
     to_do = takeCommand().lower()
     if 'create' in to_do and 'instance' in to_do:
       create_inst()
     elif 'volumes' in to_do:
       vols()
     elif 'snapshots' in to_do:
       snaps()
     elif 'docker' in to_do and 'start' in to_do and 'service' in to_do:
       docker_start()
     elif 'docker' in to_do and 'stop' in to_do:
       stop_docker()
     elif 'web server' in to_do and 'start' in to_do:
       start_server()
     elif 'docker' in to_do and 'run' in to_do and 'start' in to_do and 'container' in to_do:
       docker_cont_run()
     else:
       print('again run command\n')
       speak('speak again ')
