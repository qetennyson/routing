"""
Network class for managing network devices and simulation.

The Network acts as a registry service that tracks all devices
by their IP addresses and allows devices to look up each other.
"""


class Network:
    """
    A network that manages and coordinates devices.
    
    The network provides:
    - Device registration by IP address
    - Device lookup service
    - Central coordination for the simulation
    
    Devices explicitly register themselves with the network.
    """
    
    def __init__(self):
        """
        Initialize an empty network.
        
        The network maintains a dictionary mapping IP addresses (strings)
        to device objects.
        
        >>> net = Network()
        >>> net.devices
        {}
        """
        self.devices = {}
    
    def register_device(self, device):
        """
        Register a device with the network.
        
        Adds the device to the network's registry using its IP address
        as the key. Devices must be explicitly registered to be found.
        
        Args:
            device (Device): The device to register
        
        >>> from host import Host
        >>> net = Network()
        >>> host = Host("192.168.1.10", net)
        
        >>> net.register_device(host)
        >>> "192.168.1.10" in net.devices
        True
        
        >>> net.devices["192.168.1.10"] == host
        True
        """
        self.devices[str(device.ip_address)] = device
    
    def get_device(self, ip_string):
        """
        Look up a device by IP address.
        
        Returns the device object if found, None if not registered.
        
        Args:
            ip_string (str): IP address to look up
        
        Returns:
            Device: The device with that IP, or None if not found
        
        >>> from host import Host
        >>> from router import Router
        >>> net = Network()
        >>> host_a = Host("192.168.1.10", net)
        >>> host_b = Host("192.168.1.20", net)
        >>> router = Router("192.168.1.1", net)
        
        >>> net.register_device(host_a)
        >>> net.register_device(router)
        
        >>> device = net.get_device("192.168.1.10")
        >>> device == host_a
        True
        
        >>> device = net.get_device("192.168.1.1")
        >>> device == router
        True
        
        >>> device = net.get_device("192.168.1.20")
        >>> device is None
        True
        
        >>> device = net.get_device("10.0.0.1")
        >>> device is None
        True
        """
        return self.devices.get(ip_string)
    
    def deliver_packet(self, packet):
        """
        Deliver a packet through the network to its destination.
        
        The network looks up the destination IP in the device registry
        and delivers the packet by calling receive_packet() on that device.
        If the destination is not in the registry, the packet is dropped.
        
        This is the central coordination point: packets from hosts get routed
        through routers via this method, which then uses the routing table.
        
        Args:
            packet (Packet): The packet to deliver
        
        BEHAVIOR:
        1. Look up the destination IP address in the network registry
        2. If found, call receive_packet() on that device (Host or Router)
        3. If not found, packet is dropped (method returns silently)
        
        Test Case 1: Direct delivery from Host A to Host B
        Both hosts on same network, direct routing
        >>> from host import Host
        >>> from packet import Packet
        >>> from ip_address import IPAddress
        >>> net = Network()
        >>> host_a = Host("192.168.1.10", net)
        >>> host_b = Host("192.168.1.20", net)
        >>> net.register_device(host_a)
        >>> net.register_device(host_b)
        
        >>> pkt1 = Packet(IPAddress("192.168.1.10"), IPAddress("192.168.1.20"), "Direct msg", ttl=5)
        >>> net.deliver_packet(pkt1)
        >>> len(host_b.inbox)
        1
        >>> host_b.inbox[0].payload
        'Direct msg'
        
        Test Case 2: Delivery through a router
        Host A -> Router -> Host B across network boundaries
        >>> from router import Router
        >>> net2 = Network()
        >>> host_a2 = Host("192.168.1.10", net2)
        >>> router = Router("192.168.1.1", net2)
        >>> host_b2 = Host("192.168.2.20", net2)
        >>> net2.register_device(host_a2)
        >>> net2.register_device(router)
        >>> net2.register_device(host_b2)
        
        # Configure router to know how to reach Host B
        >>> router.add_route("192.168.2.20", host_b2)
        
        # Send packet to router (not directly to Host B)
        >>> pkt2 = Packet(IPAddress("192.168.1.10"), IPAddress("192.168.2.20"), "Via router", ttl=5)
        >>> net2.deliver_packet(pkt2)
        
        # Router receives and forwards to Host B
        >>> len(host_b2.inbox)
        1
        >>> host_b2.inbox[0].payload
        'Via router'
        >>> pkt2.ttl
        4
        
        Test Case 3: Unregistered destination (packet dropped)
        Destination IP not in network registry
        >>> net3 = Network()
        >>> host_a3 = Host("192.168.1.10", net3)
        >>> host_b3 = Host("192.168.1.20", net3)
        >>> net3.register_device(host_a3)
        >>> net3.register_device(host_b3)
        
        # Try to send to unregistered IP
        >>> pkt3 = Packet(IPAddress("192.168.1.10"), IPAddress("8.8.8.8"), "Nowhere", ttl=5)
        >>> initial_inbox_count = len(host_b3.inbox)
        >>> net3.deliver_packet(pkt3)
        >>> len(host_b3.inbox) == initial_inbox_count
        True
        
        Test Case 4: Multiple sequential packets
        Verify sequence numbers are preserved through delivery
        >>> net4 = Network()
        >>> sender = Host("192.168.1.5", net4)
        >>> receiver = Host("192.168.1.15", net4)
        >>> net4.register_device(sender)
        >>> net4.register_device(receiver)
        
        >>> pkt_a = Packet(IPAddress("192.168.1.5"), IPAddress("192.168.1.15"), "First", ttl=10, sequence=1)
        >>> pkt_b = Packet(IPAddress("192.168.1.5"), IPAddress("192.168.1.15"), "Second", ttl=10, sequence=2)
        >>> pkt_c = Packet(IPAddress("192.168.1.5"), IPAddress("192.168.1.15"), "Third", ttl=10, sequence=3)
        
        >>> net4.deliver_packet(pkt_a)
        >>> net4.deliver_packet(pkt_b)
        >>> net4.deliver_packet(pkt_c)
        
        >>> len(receiver.inbox)
        3
        >>> receiver.inbox[0].sequence
        1
        >>> receiver.inbox[1].sequence
        2
        >>> receiver.inbox[2].sequence
        3
        """
        pass

    def __str__(self):
        """
        Return string representation of network.
        
        Returns:
            str: Network info with device count
        
        >>> from host import Host
        >>> net = Network()
        >>> host_a = Host("192.168.1.10", net)
        >>> host_b = Host("192.168.1.20", net)
        >>> net.register_device(host_a)
        >>> net.register_device(host_b)
        >>> print(net)
        Network with 2 devices
        """
        return f'Network with {len(self.devices)} devices'