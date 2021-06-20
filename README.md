# chord-dht

Implementation of a Chord DHT. 2nd assignment for course on distributed system principles

## Installation and Setup

TODO: installation and setup instructions


## Note about Python version for *nix Systems

*nix refers to Unix (Mac), Linux, etc.
You may have a different version of Python 3 installed. If it works, great! If not, you'll want to follow these instructions to
get set up with Python 3.9

If you're able to work with a different version of Python 3, you'll use a different command than `python3.9` in the provided code snippets.
Your command may likely be `python3` or `python3.x` (where `x` is the minor version), so adjust accordingly. The code snippets for *nix systems
are written with the assumption of running version 3.9 and the python interpretter is registered with the system as `python3.9`.

### Installing Python 3.9 on *nix Systems

TODO: installation instructions for python3.9 on *nix

## Tasks

### Finish Chord Worksheet - 20 pts

See [chord-worksheet.docx](./chord-worksheet.docx)

### Write a hashing function - 5 pts

Implemented with the MD5 algorithm. implemented in [hash_function.py](./src/app/hash_function.py)

Run the manual test with the command from the root of this repository:

Windows:

```powershell
> py .\src\test\hash_function.py [value-to-hash]
the hash of [value-to-hash] is [hashed-value]
```

*nix:

```bash
$ python3.9 ./src/test/hash_function.py [value-to-hash]
the hash of [value-to-hash] is [hashed-value]
```

### Implement mod-N load balancing - 10 pts

Random selection is used for the hashed strings, so output varies each time.
The test prints the assignment of 10 random keys each to 1 of 50 "server nodes".
Then, after adding a 51st node, the new key assignment is printed out.

During a sample run, `9` out of the `10` keys were assigned to a new node during the second run.

```powershell
> py .\src\test\mod_n_load_balancing.py

--------------------------------
initial configuration
--------------------------------

keys in server server_17:
        cached_data_38
        cached_data_92
keys in server server_26:
        cached_data_16
        cached_data_88
keys in server server_47:
        cached_data_23
keys in server server_84:
        cached_data_15
keys in server server_89:
        cached_data_59
keys in server server_73:
        cached_data_74
keys in server server_69:
        cached_data_75
keys in server server_4:
        cached_data_12

--------------------------------
after adding 1 new server
--------------------------------

keys in server server_79:
        cached_data_38
keys in server server_65:
        cached_data_16
        cached_data_88
keys in server server_74:
        cached_data_23
keys in server server_75:
        cached_data_15
keys in server server_17:
        cached_data_92
keys in server server_44:
        cached_data_59
keys in server server_70:
        cached_data_74
keys in server server_54:
        cached_data_75
keys in server server_51:
        cached_data_12
```

### Implement consistent ring load balancing - 10 pts

This is the same manual test as mod-n load balancing except that consistent hashing is used
as the key-assignment algorithm instead of mod-n.

When the 51st server was added, 0 keys had to be reassigned to a new server.

```powershell
> py .\src\test\consistent_hashing_load_balancing.py

--------------------------------
initial configuration
--------------------------------

keys in server server_10:
        cached_data_53
keys in server server_79:
        cached_data_61
        cached_data_33
keys in server server_30:
        cached_data_29
        cached_data_95
keys in server server_17:
        cached_data_20
keys in server server_39:
        cached_data_50
        cached_data_35
keys in server server_98:
        cached_data_39
keys in server server_4:
        cached_data_64

--------------------------------
after adding 1 new server
--------------------------------

keys in server server_10:
        cached_data_53
keys in server server_79:
        cached_data_61
        cached_data_33
keys in server server_30:
        cached_data_29
        cached_data_95
keys in server server_17:
        cached_data_20
keys in server server_39:
        cached_data_50
        cached_data_35
keys in server server_98:
        cached_data_39
keys in server server_4:
        cached_data_64
```
