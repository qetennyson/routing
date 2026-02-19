"""
Router class for forwarding packets between networks.

Routers use routing tables to determine where to send packets based
on their destination IP addresses. They handle TTL and drop expired packets.
"""

from device import Device
from packet import Packet
from ip_address import IPAddress


class Router(Device):
    """
    A network router that forwards packets based on routing tables.
    
    Routers sit between networks and make forwarding decisions:
    - Maintain routing table (destination -> next hop device)
    - Decrement TTL on each forwarded packet
    - Drop packets when TTL expires
    - Support exact match, prefix match, and default routes
    """
    
    def __init__(self, ip_string, network):
        """
        Initialize a router device.
        
        The router maintains a routing table (dictionary) that maps
        destination IPs or prefixes to next-hop device objects.
        
        Args:
            ip_string (str): IP address for this router
            network (Network): The network this router belongs to
        
        >>> from network import Network
        >>> net = Network()
        >>> router = Router("192.168.1.1", net)
        >>> str(router.ip_address)
        '192.168.1.1'
        
        >>> router.routing_table
        {}
        """
        self.ip_address = IPAddress(ip_string)
        self.network = network
        self.routing_table = {}
    
    def add_route(self, destination_ip, next_hop_device):
        """
        Add a route to the routing table.
        
        Routes can be:
        - Exact IP: "192.168.1.10" -> specific host
        - Prefix: "192.168.1" -> all IPs starting with prefix
        - Default: "*" -> catch-all for unmatched destinations
        
        Args:
            destination_ip (str): Destination IP or prefix or "*"
            next_hop_device (Device): Device to forward matching packets to
        
        >>> from network import Network
        >>> net = Network()
        >>> router = Router("192.168.1.1", net)
        
        >>> class MockDevice:
        ...     pass
        >>> mock_host = MockDevice()
        
        >>> router.add_route("192.168.1.10", mock_host)
        >>> "192.168.1.10" in router.routing_table
        True
        
        >>> router.add_route("10.0.0", mock_host)
        >>> "10.0.0" in router.routing_table
        True
        
        >>> router.add_route("*", mock_host)
        >>> "*" in router.routing_table
        True
        """
        self.routing_table[destination_ip] = next_hop_device
    
    def receive_packet(self, packet):
        """
        NOTE: Comprehensive doctests for this method will be added once
        Network class is implemented, as they require full routing setup.

        Receive a packet and forward it.
        
        This overrides Device.receive_packet(). Routers don't keep packets;
        they forward them to the next hop using forward_packet().
        
        Args:
            packet (Packet): The packet being received
        
        """
        pass
    
    def forward_packet(self, packet):
        """
        Forward a packet to the next hop based on routing table.

        NOTE: Comprehensive doctests for this method will be added once
        Network class is implemented, as they require realistic packet routing.
        See example_simulation.py for integration testing once complete.
        
        LOOKUP ORDER (important for routing):
        1. Check for exact IP match: "192.168.2.20"
        2. Check for prefix matches: "192.168.2", "192.168", "192"
        3. Check for default route: "*"
        4. If no match, drop the packet
        
        Before forwarding:
        - Decrement the packet's TTL
        - If TTL reaches 0, drop the packet (don't forward)
        
        Args:
            packet (Packet): The packet to forward
        

        """
        pass
    
    def __str__(self):
        """
        Return string representation of router.
        
        Returns:
            str: Router type and IP address
        
        >>> from network import Network
        >>> net = Network()
        >>> router = Router("192.168.1.1", net)
        >>> print(router)
        Router @ 192.168.1.1
        """
        return f'Router @ {self.ip_address}'
