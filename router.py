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
        pass
    
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
        >>> from host import Host
        >>> net = Network()
        >>> router = Router("192.168.1.1", net)
        >>> host = Host("192.168.1.10", net)
        
        >>> router.add_route("192.168.1.10", host)
        >>> "192.168.1.10" in router.routing_table
        True
        
        >>> router.add_route("10.0.0", host)
        >>> "10.0.0" in router.routing_table
        True
        
        >>> router.add_route("*", host)
        >>> "*" in router.routing_table
        True
        """
        pass
    
    def receive_packet(self, packet):
        """
        Receive a packet and forward it.
        
        This overrides Device.receive_packet(). Routers don't keep packets;
        they forward them to the next hop using forward_packet().
        
        Args:
            packet (Packet): The packet being received
        
        >>> from network import Network
        >>> from host import Host
        >>> net = Network()
        >>> router = Router("192.168.1.1", net)
        >>> host_a = Host("192.168.1.10", net)
        >>> host_b = Host("192.168.2.20", net)
        >>> net.register_device(router)
        >>> net.register_device(host_a)
        >>> net.register_device(host_b)
        
        >>> router.add_route("192.168.2.20", host_b)
        >>> src = IPAddress("192.168.1.10")
        >>> dst = IPAddress("192.168.2.20")
        >>> pkt = Packet(src, dst, "Test", ttl=10)
        
        >>> router.receive_packet(pkt)
        >>> len(host_b.inbox)
        1
        """
        pass
    
    def forward_packet(self, packet):
        """
        Forward a packet to the next hop based on routing table.
        
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
        
        >>> from network import Network
        >>> from host import Host
        >>> net = Network()
        >>> router = Router("192.168.1.1", net)
        >>> host_a = Host("192.168.1.10", net)
        >>> host_b = Host("192.168.2.20", net)
        >>> net.register_device(router)
        >>> net.register_device(host_a)
        >>> net.register_device(host_b)
        
        # Test exact match
        >>> router.add_route("192.168.2.20", host_b)
        >>> src = IPAddress("192.168.1.10")
        >>> dst = IPAddress("192.168.2.20")
        >>> pkt = Packet(src, dst, "Exact match", ttl=5)
        >>> router.forward_packet(pkt)
        >>> len(host_b.inbox)
        1
        >>> pkt.ttl
        4
        
        # Test prefix match
        >>> router2 = Router("10.0.0.1", net)
        >>> host_c = Host("10.0.1.50", net)
        >>> net.register_device(router2)
        >>> net.register_device(host_c)
        >>> router2.add_route("10.0.1", host_c)
        >>> src2 = IPAddress("192.168.1.10")
        >>> dst2 = IPAddress("10.0.1.50")
        >>> pkt2 = Packet(src2, dst2, "Prefix match", ttl=5)
        >>> router2.forward_packet(pkt2)
        >>> len(host_c.inbox)
        1
        
        # Test TTL expiration (packet should be dropped)
        >>> src3 = IPAddress("192.168.1.10")
        >>> dst3 = IPAddress("192.168.2.20")
        >>> pkt3 = Packet(src3, dst3, "Expired", ttl=1)
        >>> initial_count = len(host_b.inbox)
        >>> router.forward_packet(pkt3)
        >>> len(host_b.inbox) == initial_count
        True
        
        # Test default route
        >>> router3 = Router("172.16.0.1", net)
        >>> default_host = Host("172.16.0.100", net)
        >>> net.register_device(router3)
        >>> net.register_device(default_host)
        >>> router3.add_route("*", default_host)
        >>> src4 = IPAddress("1.1.1.1")
        >>> dst4 = IPAddress("8.8.8.8")
        >>> pkt4 = Packet(src4, dst4, "Default route", ttl=5)
        >>> router3.forward_packet(pkt4)
        >>> len(default_host.inbox)
        1
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
        pass
