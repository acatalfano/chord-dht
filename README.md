# chord-dht

Implementation of a Chord DHT. 2nd assignment for course on distributed system principles

## Installation and Setup

TODO: installation and setup instructions


## Note about Python version for \*nix Systems

\*nix refers to Unix (Mac), Linux, etc.
You may have a different version of Python 3 installed. If it works, great! If not, you'll want to follow these instructions to
get set up with Python 3.9

If you're able to work with a different version of Python 3, you'll use a different command than `python3.9` in the provided code snippets.
Your command may likely be `python3` or `python3.x` (where `x` is the minor version), so adjust accordingly. The code snippets for *nix systems
are written with the assumption of running version 3.9 and the python interpretter is registered with the system as `python3.9`.

### Installing Python 3.9 on *nix Systems

TODO: installation instructions for python3.9 on *nix

## Tasks

### Notes on running the code

Each task (when relevant) has a code snippet of command line execution, showing how each test-file can be run and what sample output
looks like. A Windows environment using Powershell is assumed except for the Mininet tasks, in which I assume an Ubuntu VM
(or directly installed Ubuntu system).

The instructions will be the same for a \*nix environment except for what your system may alias the python command to.
Often in \*nix, the `py` will be replaced with `python3.9` or `python3`.

For example, the following command in Powershell:

```powershell
> py .\src\test\hash_function.py hashme!
[output]
```

will be this, in an Ubuntu environment where python is aliased to `python3.9`:

```bash
$ python3.9 ./src/test/hash_function.py hashme!
[output]
```

### Notes about Random Sample

For more fidelity in the the test environment, Python's `random` library was used, but for the sake of reproducibility,
a seed is always set before any random calls are made. If you run this code following the provided instructions,
your output is not expected to vary.

### Finish Chord Worksheet - 20 pts

See [chord-worksheet.docx](./chord-worksheet.docx)

### Write a hashing function - 5 pts

Implemented with the MD5 algorithm. implemented in [hash_function.py](./src/app/hash_function.py)

Run the manual test with the command from the root of this repository:

```powershell
> py .\src\test\hash_function.py hashme!
the hash of hashme! is 229
```

### Implement mod-N load balancing - 10 pts

Random selection is used for the hashed strings.
The test prints the assignment of 10 random keys each to 1 of 50 "server nodes".
Then, after adding a 51st node, the new key assignment is printed out.

During a sample run, `8` out of the `10` keys were assigned to a new node during the second run.

```powershell
> py .\src\test\mod_n_load_balancing.py

--------------------------------
initial configuration
--------------------------------

keys in server server_72:
        cached_data_80
keys in server server_9:
        cached_data_0
keys in server server_97:
        cached_data_78
keys in server server_90:
        cached_data_63
keys in server server_69:
        cached_data_42
keys in server server_40:
        cached_data_31
keys in server server_50:
        cached_data_93
keys in server server_61:
        cached_data_41
keys in server server_45:
        cached_data_90
keys in server server_71:
        cached_data_8

--------------------------------
after adding 1 new server
--------------------------------

keys in server server_58:
        cached_data_80
keys in server server_18:
        cached_data_0
keys in server server_49:
        cached_data_78
keys in server server_56:
        cached_data_63
keys in server server_69:
        cached_data_42
keys in server server_89:
        cached_data_31
keys in server server_25:
        cached_data_93
keys in server server_65:
        cached_data_41
keys in server server_61:
        cached_data_90
keys in server server_71:
        cached_data_8
```

### Implement consistent ring load balancing - 10 pts

This is the same manual test as mod-n load balancing except that consistent hashing is used
as the key-assignment algorithm instead of mod-n.

When the 51st server was added, `3` keys had to be reassigned to a new server.

```powershell
> py .\src\test\consistent_hashing_load_balancing.py

--------------------------------
initial configuration
--------------------------------

keys in server server_71:
        cached_data_80
        cached_data_93
keys in server server_74:
        cached_data_0
keys in server server_36:
        cached_data_78
        cached_data_90
keys in server server_27:
        cached_data_63
keys in server server_92:
        cached_data_42
keys in server server_89:
        cached_data_31
keys in server server_25:
        cached_data_41
keys in server server_68:
        cached_data_8

--------------------------------
after adding 1 new server
--------------------------------

keys in server server_71:
        cached_data_80
        cached_data_93
keys in server server_40:
        cached_data_0
keys in server server_36:
        cached_data_78
        cached_data_42
        cached_data_90
keys in server server_27:
        cached_data_63
keys in server server_89:
        cached_data_31
keys in server server_25:
        cached_data_41
keys in server server_12:
        cached_data_8
```

### Implement Naïve Chord Routing - 10 pts

Naïve Chord Routing is a ring of servers, each given an id (hash value) in an address space.
Each server knows about its successor and nothing else. You can search for a key in the address space
only by recursively checking the next server.

The manual test harness calculates the average hop-count to find a random key from a random server.
This average is calculated for a ring of 50 nodes, as well as a ring of 100 nodes.

Run the test as follows:

```powershell
> py .\src\test\naive_chord.py
for 50 nodes, the average hop size is: 24.5
for 100 nodes, the average hop size is: 49.5
```

The average hop size was found to be 24.5 for a 50-node network and 49.5 for a 100-node network.
This is a naïve algorithm, and the results are just as intuitive as the algorithm's approach.
The average number of hops for the naïve algorithm is similar to asking what the average arc-length
between any 2 points in a circle happens to be. It's going to be half the circumference (or half the number of nodes).
In the case of 50, we expect 25 (I got 24.5) and in the case of 100, we expect 50 (I got 49.5).
This algorithm is expected to scale the number of hops linearly.

### Build Finger Tables - 10 pts

Run the test harness for the finger-table builder using the indicated command.
You should get the following output as well.

You will see a printout of the configuration of the server ring (node name and hashed id),
followed by a printout of the nodes in a specific server's finger table.
Under the current configuration, this server will be named "server_65", which is hashed to address 170.

```powershell
> py .\src\test\finger_table.py
--------------------------------
node configuration (name: id)
--------------------------------
server_62: 16
server_33: 31
server_97: 54
server_5: 69
server_51: 98
server_53: 131
server_65: 170
server_49: 171
server_61: 172
server_38: 221
--------------------------------
node (id)
    server_65: 170

finger table (k-value -- id)
1 -- 171
2 -- 172
3 -- 221
4 -- 221
5 -- 221
6 -- 221
7 -- 16
8 -- 54
--------------------------------
```

### Implement Chord Routing - 10 Pts

Run the following command to see the test harness result of the Chord Routing algorithm.
It is the same ring "network" as was used in Naïve Chord Routing and the same form of output,
but with the Chord algorithm instead of the Naïve Chord algorithm.

```powershell
> py .\src\test\chord_routing.py
for 50 nodes, the average hop size is: 2.7608
for 100 nodes, the average hop size is: 3.1345
```

First, most notably, the average hop size is much smaller than that of the Naïve algorithm.
Secondly, more subtly, you can note that the hop size increased on average as the number of nodes increased.
This result can be verified by Stoica et al. in their theoretical results on the Chord algorithm.

![Chord hop size vs node count graph](./assets/chord_hop_size_and_node_count.png "title my title")

Stoica et al. show a similar trend and posited that the trend is that a path length is about
_(1/2)log<sub>2</sub>N_, where _N_ is the number of nodes.

### Implement Synchronization Protocol - 10 pts

Run the following command to see the test harness result of synchronization protocol.
The synchronization protocol is driven by threads that periodically execute to update the
successor, predecessor, and finger-table information on each node.

```powershell
> py .\src\test\synchronization.py
press ENTER to start
then let the activity settle down then press ENTER
to see the effects on one node joining the network
then press ENTER to end




Start a ring with node 155
set predecessor of 155 to 155
... [logging omitted]



Node 115 join ring with successor node 153
set predecessor of 153 to 115
set successor of 86 to 115
set predecessor of 115 to 86

... [logging omitted]
```

The script waits for you to press enter before beginning, then it create a ring with 11 nodes
and wait for you to press enter again. At this point the intent is for the user to wait
for output to stop being reported (i.e. the threads will have all finished fixing the network)
And you can then press enter to view the activity of a single node joining the established ring.
You can then press enter again to end the program and to get a printout of all current finger tables
and (predecessor, node, successor) tuples.

The last node will have ID 115 and will join the network on node 153.

* The first step is to assign 153 to be 115's successor
* 115 then notifies 153 that it (115) may be 153's new predecessor
* 153 agrees and sets 115 as its own predecessor
* 86's `stabilize` thread eventually picks up that 115 is its new successor. This is because 153 was 86's stored successor, but 86's successor's predecessor (153's predecessor, which is 115) is not 86, so 86 updates its successor to be 115.
* Since the successor has been updated for 86, it notifies 115 that it (86) may be 115's new predecessor.
* 115 agrees and updates its predecessor to be 86.
* 115 is now successfully integrated into the ring.

If you're interested in seeing the finger table updates as well, you can run the same script with the `-v` flag for verbose mode.

### Improve Load Balancing with Virtual Nodes - 10 pts

The test harness creates a 20-node physical network and a 200-node virtual network (with 20 physical nodes).
The standard deviation of the nodes' responsible load is measured for both networks.
Assuming more or less comparable hardware comprising the nodes, a lower standard deviation is the goal.
By adding the virtual nodes into the mix, the standard deviation of the load distribution jumped from
`12.4` down to `0.8`.

Run the following command to execute the test harness locally.

```powershell
> py .\src\test\virtual_nodes.py
standard deviation for physical 20-ring: 12.436237373096414
standard deviation for virtual 200-ring: 0.7947326594522217
```

Virtual nodes address load balancing issues related to non-uniform distribution of nodes across the ring.
The load balancing issue they don't address is the case where a handful of specific keys garner
unproportionately high volumes of traffic. To address this load-balancing problem, you would need
to implement an ensemble of servers that are load balanced, together functioning as a single node in
the ring (a node responsible for the keys that receive the high amount of traffic).

### Run Chord on Mininet - 10 pts

To run Chord on Mininet, you will first need to setup the Mininet VM (or local installation), Python 3.9,
the proper version of Pip to go with Python 3.9, and (recommended) a venv.

#### Setup/Installation

##### Mininet Setup

You will need to first have a system compatible with running mininet, follow Mininet's [instructions](http://mininet.org/download/) to do so.

Either setup the VM image outlined in option 1 or follow these steps taken from options 2:

Clone the mininet repository and checkout the 2.3.0 branch. There are other more
recent releases of mininet (e.g. `2.3.0d6`), but they had some quirks with packages
not lining up. `2.3.0` is the happy path. You need to install like this because the
latency tests depend on controllers as well as the actual mininet library.

```bash
$ git clone git://github.com/mininet/mininet
$ cd mininet
$ git checkout -b mininet-2.3.0 2.3.0
$ cd ..
```

Now run the installation script:

```bash
$ mininet/util/install.sh -nfv
```

##### Install Python 3.9

Before beginning, update and ensure `software-properties-common` is installed:

```bash
$ sudo apt update
$ sudo apt install software-properties-common
```

Now add the PPA:

```bash
$ sudo add-apt-repository ppa:deadsnakes/ppa
```

Install Python3.9:

```bash
$ sudo apt install python3.9
```

Alternatively, you may want to install `python3.9-full`, which you can always do later if necessary.

You can now run Python 3.9 with the command `python3.9`. For sanity, check the version with `python3.9 --version`.

##### Install Pip for Python 3.9

Retrieve and run the `get-pip.py` script:

```bash
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ sudo python3.9 ./get-pip.py
```

Cleanup the script if you want; it served its purpose.

```bash
$ rm ./get-pip.py
```

##### Setup a Virtual Environment

Your python installation probably includes `venv`, but if not you'll have to get a Python 3.9 distribution that does.
If you have the option at installation, this means selecting the "full" version.

Open up a terminal in the root directory of this repository and run the following command.

```bash
$ python3.9 -m venv --upgrade-deps ./env
```

Activate the venv

```bash
$ source ./env/bin/activate
```

If you close the terminal, you'll have to activate the venv again.

##### Install the project dependencies

This will install all of the dependencies except for mininet,
that will be built from source.
Run the following command (all systems)

```bash
$ pip install -e ./src
```

You will now have to copy over the mininet package that was setup for you.
Locate it, likely in `~/.local/lib/python3.9/site-packages`. The `mininet` directory is what you want to copy.
Copy it over to `/PATH/TO/REPOSITORY/env/lib/python3.9/site-packages`

#### Run the Test Harness

Be sure the venv is activated if you're using the recommended venv setup.
If you named your venv `env`, then you should see `(env)` before the current working directory in your command prompt.

From the root of this repository, you can run the test harness with the following command (within the mininet VM if you don't have it installed locally):

For venv users who followed the installation instructions:

```bash
(env) User@Machine:~/Repo$ sudo ./env/bin/python ./src/test/mininet/topology.py
```

For venv users who chose the venv to be located somewhere else:

```bash
(CUSTOM-VENV-NAME) User@Machine:~/Repo$ sudo PATH/TO/YOUR/VENV/bin/python ./src/test/mininet/topology.py
```

If you installed the dependencies globally as super-user (not using a venv):

```bash
User@Machine:~/Repo$ sudo python3.9 ./src/test/mininet/topology.py
```

(your python command may differ from `python3.9`, but ensure that you are running python version 3.9)

If you installed as a normal non-elevated user, it will not run. Mininet requires super-user privileges
and the dependencies must be installed somewhere the super-user knows about.

#### Results

Each node in the network will output results to `*.txt` files located under `./src/test/mininet/nodes`

Originally additional activity-logging was intended, but
currently the extent of the functionality is error logging.
No errors are currently being output.

## References

Stoica, I., et al. “Chord: A Scalable Peer-To-Peer Lookup Protocol for Internet Applications.” IEEE/ACM Transactions on Networking, vol. 11, no. 1, Feb. 2003, pp. 17–32, 10.1109/tnet.2002.808407.
