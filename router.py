"""
Router class for forwarding packets between networks.

Routers use routing tables to determine where to send packets based
on their destination IP addresses. They handle TTL and drop expired packets.
"""
from simple_device import SimpleDevice # testing purposes only.
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

    def _is_exact_route_host_match(self, route):
        """
        Check if there's an exact route match in the routing table.
        
        Args:
            route (str): The destination IP string to look up exactly
        
        Returns:
            Device: The next-hop device if exact match found, None otherwise
        
        >>> router = Router("192.168.1.1", None)
        >>> class MockDevice:
        ...     pass
        >>> dev_a = MockDevice()
        >>> dev_b = MockDevice()
        
        # Add exact routes
        >>> router.add_route("192.168.2.20", dev_a)
        >>> router.add_route("10.0.0.50", dev_b)
        
        # Test exact match found
        >>> result = router._is_exact_route_host_match("192.168.2.20")
        >>> result is dev_a
        True
        
        >>> result = router._is_exact_route_host_match("10.0.0.50")
        >>> result is dev_b
        True
        
        # Test exact match not found
        >>> result = router._is_exact_route_host_match("192.168.2.21")
        >>> result is None
        True
        
        >>> result = router._is_exact_route_host_match("8.8.8.8")
        >>> result is None
        True
        """
        possible_host = self.routing_table.get(route)
        if possible_host:
            return possible_host
        
    def _is_prefix_route_host_match(self, packet):
        """
        Check for prefix matches in the routing table.
        
        Tries progressively shorter prefixes: 3 octets, 2 octets, 1 octet.
        Returns the first matching device or None if no match found.
        
        Args:
            packet (Packet): The packet whose destination IP will be checked
        
        Returns:
            Device: The next-hop device if prefix match found, None otherwise
        
        >>> router = Router("192.168.1.1", None)
        >>> class MockDevice:
        ...     pass
        >>> dev_3octet = MockDevice()
        >>> dev_2octet = MockDevice()
        >>> dev_1octet = MockDevice()
        
        # Add prefix routes
        >>> router.add_route("10.0.1", dev_3octet)
        >>> router.add_route("172.16", dev_2octet)
        >>> router.add_route("192", dev_1octet)
        
        # Test 3-octet prefix match
        >>> pkt1 = Packet(IPAddress("192.168.1.10"), IPAddress("10.0.1.50"), "test", ttl=5)
        >>> result = router._is_prefix_route_host_match(pkt1)
        >>> result is dev_3octet
        True
        
        # Test 2-octet prefix match (when 3-octet doesn't exist)
        >>> pkt2 = Packet(IPAddress("192.168.1.10"), IPAddress("172.16.50.100"), "test", ttl=5)
        >>> result = router._is_prefix_route_host_match(pkt2)
        >>> result is dev_2octet
        True
        
        # Test 1-octet prefix match (when 3 and 2 octets don't exist)
        >>> pkt3 = Packet(IPAddress("192.168.1.10"), IPAddress("192.0.0.1"), "test", ttl=5)
        >>> result = router._is_prefix_route_host_match(pkt3)
        >>> result is dev_1octet
        True
        
        # Test no prefix match found
        >>> pkt4 = Packet(IPAddress("192.168.1.10"), IPAddress("8.8.8.8"), "test", ttl=5)
        >>> result = router._is_prefix_route_host_match(pkt4)
        >>> result is None
        True
        """
        destination_octets = packet.dest.get_octets()
        last_octet_to_check = 3
        while last_octet_to_check >= 0:
            prefix = destination_octets[:last_octet_to_check]
            prefix_as_string = '.'.join((str(octet) for octet in prefix))

            possible_match = self.routing_table.get(prefix_as_string)
            if not possible_match:
                last_octet_to_check -= 1
                continue
            
            else:
                return possible_match
        

    
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
    
    def receive_packet(self, packet: Packet):
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

        LOOKUP ORDER (important for routing):
        1. Check for exact IP match: "192.168.2.20"
        2. Check for prefix matches: "192.168.2", "192.168", "192"
        3. Check for default route: "*"
        4. If no match, drop the packet
        
        Before forwarding:
        - Decrement the packet's TTL by 1
        - If TTL reaches 0, drop the packet (don't forward)
        
        Args:
            packet (Packet): The packet to forward
        
        ALGORITHM:
        1. Decrement TTL first
        2. Check if TTL is now 0 - if so, return (drop packet)
        3. Try to find a route for the destination IP:
           - First check exact IP match in routing_table
           - If not found, try progressively shorter prefixes
           - If still not found, check for default route "*"
        4. If route found, call next_hop_device.receive_packet(packet)
        
        >>> router = Router("192.168.1.1", None)
        >>> dev_b = SimpleDevice()
        >>> router.add_route("192.168.2.20", dev_b)
        >>> pkt = Packet(IPAddress("192.168.1.10"), IPAddress("192.168.2.20"), "test", ttl=5)
        >>> router.forward_packet(pkt)
        >>> len(dev_b.inbox)
        1
        >>> pkt.ttl
        4
        
        # Test prefix matching
        >>> router2 = Router("10.0.0.1", None)
        >>> dev_c = SimpleDevice()
        >>> router2.add_route("10.0.1", dev_c)
        >>> pkt2 = Packet(IPAddress("192.168.1.10"), IPAddress("10.0.1.50"), "prefix match", ttl=5)
        >>> router2.forward_packet(pkt2)
        >>> len(dev_c.inbox)
        1
        
        # Test TTL expiration (packet should be dropped)
        >>> router3 = Router("172.16.0.1", None)
        >>> dev_d = SimpleDevice()
        >>> router3.add_route("192.168.2.20", dev_d)
        >>> pkt3 = Packet(IPAddress("192.168.1.10"), IPAddress("192.168.2.20"), "will expire", ttl=1)
        >>> initial_count = len(dev_d.inbox)
        >>> router3.forward_packet(pkt3)
        >>> len(dev_d.inbox) == initial_count
        True
        >>> pkt3.ttl
        0
        
        # Test default route
        >>> router4 = Router("1.1.1.1", None)
        >>> default_dev = SimpleDevice()
        >>> router4.add_route("*", default_dev)
        >>> pkt4 = Packet(IPAddress("192.168.1.10"), IPAddress("8.8.8.8"), "default route", ttl=5)
        >>> router4.forward_packet(pkt4)
        >>> len(default_dev.inbox)
        1
        
        # Test no route (packet dropped)
        >>> router5 = Router("1.1.1.1", None)
        >>> dev_e = SimpleDevice()
        >>> router5.add_route("192.168.0", dev_e)
        >>> pkt5 = Packet(IPAddress("10.0.0.1"), IPAddress("8.8.8.8"), "no route", ttl=5)
        >>> router5.forward_packet(pkt5)
        >>> len(dev_e.inbox)
        0
        """
        packet.ttl -= 1
        if packet.ttl == 0:
            return
        
        exact_host = self._is_exact_route_host_match(str(packet.dest))
        if exact_host:
            exact_host.receive_packet(packet)
            return
            
        prefix_host = self._is_prefix_route_host_match(packet)
        if prefix_host:
            prefix_host.receive_packet(packet)
            return
       
        default_route = self.routing_table.get('*')
        if default_route:
            default_route.receive_packet(packet)

        

    
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
