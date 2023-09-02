# Port Sniffer 

A lightning fast port scanner written in Python. 

## Features

- Multithreaded for speed 
- Scans full 1-65535 port range by default
- Specify custom port range 
- Option for common ports only
- Adjustable threads and timeout
- Prints open/closed/filtered ports
- Handles keyboard interrupt 

## Usage

```
usage: main.py [-h] [-d ADDRESS] [-p PORTS] [-t THREADS_COUNT] [-o TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -d ADDRESS, --destination ADDRESS
                        Destination IP or hostname
  -p PORTS, --port PORTS
                        Port range, e.g. 80:100 or reserved
  -t THREADS_COUNT, --threads THREADS_COUNT
                        Number of threads 
  -o TIMEOUT, --ttl TIMEOUT  
                        Timeout in ms per port
```

Scan a host:

```
python main.py -d 192.168.1.1
```

Scan a range:

``` 
python main.py -d 192.168.1.1 -p 1:1024
```

## How it Works

The portsniffer creates a pool of threads to scan ports concurrently. This allows it to scan ports very quickly compared to a serial scanner. 

Each thread calls connect() on the target IP and port. Based on the response it determines if the port is open, closed, or filtered.

The output is printed with thread locks to avoid mingled output.

## Improvements

- [ ] Configurable output format 
- [ ] CSV/JSON output
- [ ] Service version detection
- [ ] Randomize order of ports
- [ ] Exclude certain ports

Let me know if you would like me to explain any part of the README in more detail!
