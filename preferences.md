## Notes for Problem Design

This project should use OOP principles for all solutions.

1. **Practical context**: Use real-world scenarios (parsing data, formatting output, validation)
2. **Combination problems**: Problems can use multiple methods to achieve a solution.
3. **Edge cases**: Include empty strings, special characters, boundary conditions
4. **Progressive difficulty**: Difficulty/challenged should be availed to students via OOP, e.g. simple methods for a class 
can be written by less advanced students, and then highly complex objects and methods can be written by top students.
5. **Doctest quality**: Each doctest should illustrate a distinct use case or edge case
6. **Doctest language**: Keep doctests simple for a high school student to understand with straightforward language.

---

## Networking Simulation Project - Student Context

### Student Proficiency Levels
- **Strong with**: Dictionaries/hashmaps, basic OOP concepts
- **New to**: Inheritance and composition (will need scaffolding)
- **Advanced students**: Can implement inheritance/composition relatively easily with guidance
- **Expectation**: Not all students will complete advanced components, and that's acceptable

### Project Format
- **Output**: Text-based (terminal/console output, logging)
- **Testing**: Pre-written doctests for all methods
- **Duration**: 2 days (55-minute sessions)

### Differentiation Strategy
- **Basic tier**: All students should be able to implement `IPAddress` validation, create simple `Packet` objects
- **Intermediate tier**: Build `Host` class, send/receive packets, understand message passing
- **Advanced tier**: Implement `Router` class with routing tables, path-finding algorithms
- **Goal**: Basic students gain core networking knowledge; advanced students tackle algorithmic challenges

### Core Class Structure (Progressive)

1. **`IPAddress`** (Beginner)
   - Validate IPv4 addresses
   - Parse dotted decimal notation
   - Check valid ranges (0-255 per octet)

2. **`Packet`** (Beginner-Intermediate)
   - Store source/destination IP
   - Carry payload data
   - Track packet metadata (TTL, sequence number)

3. **`Device`** (Intermediate - Base Class)
   - Abstract base for network devices
   - Has an IP address
   - Can receive packets

4. **`Host`** (Intermediate - Inherits from Device)
   - Send packets to destinations
   - Receive and process packets
   - Maintain simple message queue

5. **`Router`** (Advanced - Inherits from Device)
   - Multiple network interfaces
   - Routing table implementation
   - Forward packets based on destination IP
   - Implement routing algorithms (static, dynamic)

6. **`Network`** (Advanced)
   - Simulation environment
   - Manages device registry
   - Routes packets between devices
   - Tracks network statistics

### Key AP CSP Concepts Embedded
- **Protocols**: IP addressing, packet structure, routing protocols
- **Abstraction**: Layered architecture, encapsulation of network operations
- **Data Representation**: Binary/decimal conversion, packet headers
- **Algorithms**: Routing algorithms, shortest path
- **Internet**: Fault tolerance, scalability, packet-switching

### Extension Opportunities (Time Permitting)
- DNS-like name resolution (hostname -> IP mapping)
- Subnet masks and subnetting
- Packet fragmentation
- Simple congestion control
- Network topology visualization (ASCII art)

---

## Implementation Design Decisions

### Routing Architecture: Delegated Approach (Option B)
- **Network class**: Device registry only - registers devices by IP, provides lookup
- **Router class**: Makes forwarding decisions using routing table with device object references
- **Host class**: Endpoint devices that store received packets in message queue
- **Key design**: `Router.add_route(destination_ip, next_hop_device)` stores actual device objects
- **Packet flow**: Router.receive_packet() -> Router.forward_packet() -> next_device.receive_packet()
- **Benefit**: Each class has single responsibility, mirrors real networking, demonstrates polymorphism

### Simplification Decisions (Extensions Available)
- **No subnetting**: Use exact IP matching or simple prefix strings (e.g., "192.168.1") for routing tables
- **No exception handling**: Return None or False for invalid operations, use selection statements
- **No topology validation**: Trust that devices are connected correctly, Network class doesn't enforce/validate connections
- **Simple queue**: Use Python list with .append() and .pop(0) for message queues

### Helper Methods Philosophy
- Include practical helper methods wherever useful (e.g., `IPAddress.get_octets()`, `IPAddress.to_string()`)
- Helpers should simplify other class implementations and provide useful building blocks
- Each helper should have clear doctests demonstrating its utility