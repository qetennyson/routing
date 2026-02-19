# Network Simulation Project

## Overview
Build an object-oriented network simulation that demonstrates core Internet protocols and concepts from AP Computer Science Principles. You'll implement classes that represent IP addresses, packets, network devices (hosts and routers), and a network simulation environment.

## Learning Objectives
- **Protocols**: Understanding IP addressing, packet structure, and routing
- **Abstraction**: Using inheritance to model different types of network devices
- **Algorithms**: Implementing routing table lookups and packet forwarding
- **Data Representation**: Parsing and validating IP addresses
- **Internet Fundamentals**: Packet switching, TTL, and multi-hop routing

## Completion Order

Work through the files in this order. Each builds on the previous:

1. **ip_address.py** (~15 minutes) 
   - Validate and represent IPv4 addresses
   - Parse dotted-decimal notation
   - Check valid octet ranges (0-255)

2. **packet.py** (~15 minutes) 
   - Create packet data structures
   - Manage packet metadata (TTL, sequence)
   - Track packet expiration

3. **device.py** (~10 minutes) 
   - Build abstract base class for network devices
   - Understand inheritance foundations
   - Set up polymorphic receive_packet method

4. **host.py** (~25 minutes)
   - Implement end-user devices
   - Send and receive packets
   - Manage message inbox queue

5. **router.py** (~35 minutes)
   - Build routing table with multiple lookup strategies
   - Forward packets based on destination
   - Handle TTL expiration and packet drops

6. **network.py** (~15 minutes)
   - Create device registry service
   - Enable device lookups by IP address
   - Coordinate simulation environment

7. **example_simulation.py**
   - See how all classes work together
   - 2-hop routing demonstration
   - Test your complete implementation

## Running Tests

### Test Individual Files
Run doctests for a specific file:
```bash
python -m doctest ip_address.py -v
```

The `-v` flag shows verbose output with all tests. Omit it to only see failures.

### Test All Files
Use the test runner to check your progress across all files:
```bash
python test_runner.py
```

This will show you which files are complete and which need work.

## Tips for Success

1. **Read the doctests carefully** - They show exactly what each method should do
2. **Work in order** - Later files depend on earlier ones
3. **Test frequently** - Run doctests after implementing each method
4. **Use helper methods** - Break complex problems into smaller pieces
5. **Ask for help** - If you're stuck on advanced sections, that's expected!

Not completing everything is OK! Each level teaches important CS concepts.
