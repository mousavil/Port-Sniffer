import pyfiglet
import sys, getopt
import threading
import socket
import re
import argparse
from threading import  Lock

ascii_banner = pyfiglet.figlet_format("Port Sniffer")
print(ascii_banner)

print_lock = Lock()
address =''
flag =0
minPort =1
maxPort=65353
ports= list(range(minPort, maxPort + 1))
threads_count = 100
timeout = 10
threads=[]

def main(argv):

    try:
        global address
        global minPort
        global maxPort
        global ports
        global threads_count
        global timeout
        global threads
        global flag
        parser = argparse.ArgumentParser()
        parser.add_argument("--destination", "-d", dest="address", help="Destination Address. Required!")
        parser.add_argument("--port", "-p", dest="ports", default="1:65535", help="Specify Port Range Between 1 To 65535. Default All Range")
        parser.add_argument("--threads", "-t", dest="threads_count", default="100", help="Default 100")
        parser.add_argument("--ttl", "-o", dest="timeout", default="100", help="Default 100ms")

        args = parser.parse_args()
        address, ports ,threads_count,timeout= args.address, args.ports,args.threads_count,args.timeout


        if threads_count == 'max':
            threads_count =1000
        else:
            try:
                if int(threads_count)>=1000:
                    threads_count=1000

                threads_count = int(threads_count)
            except:
                print("Wrong Thread Input")


        try:
            if int(timeout)<=0 or int(timeout)>5000:
                print("Bad Timeout(max=5000ms and min=1ms)")
            timeout = int(timeout)
        except:
            print("Wrong Thread Input")

        try:
            if ':' in str(ports):
                minPort=int(str(ports).split(":")[0])
                maxPort=int(str(ports).split(":")[1])
                ports=list(range(minPort, maxPort+1) )
            elif 'reserved' in str(ports):

                ports=[21,22,23,80,110,143,443,2222]
        except:
            print("Bad Range Input( 80:100 or reserved or don't write input for default range)")

        try:
            match = re.search('\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b', str(address))
            if match is None:
                match = re.search("(([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])\\.){3}"\
            "([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])", str(address))
            if match is None:
                return 0
            address=str(address)
            flag =1
        except:
            print("Wrong Address Input")
            return 0

    except KeyboardInterrupt:
        print("Exiting...")

    if flag ==1:
        return 1
    else: return 0

done = 1
current = -1



def thread_function(host):
    global current
    global ports
    global done

    current += 1
    if(current < len(ports)):
        scan(host, ports[current])
        done += 1
        if done != len(ports):
            thread_function(host)




def scan(host, port):
    global timeout
    global print_lock
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((host, port))
        if result == 0:
            with print_lock:
                print("Port " + str(port) + " Is Open")
            s.close()
        else:
            with print_lock:
                print("Port " + str(port) + " Is Closed")
            s.close()
    except KeyboardInterrupt:
        print("\n Exitting")
        sys.exit()
    except socket.gaierror:
        print("\n Hostname Cannot Be Resolved")
        sys.exit()
    except socket.error:
        print("Port "+ str(port) + " Probably Filtered")
        sys.exit()

def printOutput(res):
    global threads_count
    global address
    global threads
    if res ==1 :
        for t in range(threads_count):
            threads.append(threading.Thread(target=thread_function, args=(address,)))
            threads[t].start()

        for t in range(threads_count):
            threads[t].join()
    else:
        print("\nWrong Input. Please Use -h Or --help For The Correct One!")


res=main(sys.argv[1:])

printOutput(res)