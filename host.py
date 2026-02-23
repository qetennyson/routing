"""
Host class representing end-user devices on the network.

Hosts can send and receive packets. They maintain an inbox of received
messages and automatically track packet sequence numbers.
"""

from device import Device
from packet import Packet
from ip_address import IPAddress


class Host(Device):
    """
    An end-user device that sends and receives packets.
    
    Hosts are computers, phones, or other devices that communicate
    over the network. They:
    - Send packets to other devices
    - Receive packets and store them in an inbox
    - Automatically manage sequence numbers for sent packets
    """
    
    def __init__(self, ip_string, network, gateway=None):
        """
        Initialize a host device.
        
        The host maintains an inbox (list) for received packets and
        a sequence counter that starts at 1 and auto-increments.
        
        The gateway is the default router IP that this host sends packets
        to when communicating with devices on different networks.
        
        Args:
            ip_string (str): IP address for this host
            network (Network): The network this host belongs to
            gateway (str): Optional default gateway IP address (router)
        
        >>> from network import Network
        >>> net = Network()
        >>> host = Host("192.168.1.10", net)
        >>> str(host.ip_address)
        '192.168.1.10'
        
        >>> host.inbox
        []
        
        >>> host.gateway is None
        True
        
        >>> host2 = Host("192.168.1.20", net, gateway="192.168.1.1")
        >>> host2.gateway
        '192.168.1.1'
        """
        super().__init__(ip_string, network)
        self.inbox = []
        self.sequence = 1
        self.gateway = gateway
    
    def create_packet(self, destination_ip_string, payload):
        """        
        Creates a new packet using the destination IP string and payload
        along with auto-incrementing sequence number, and returns it.
        
        The packet is returned for the network to deliver via routing.
        
        Args:
            destination_ip_string (str): Destination IP address
            payload (str): Message to send

        Returns:
            Packet: A Packet object with source=self, destination from string, 
                   payload, and auto-incremented sequence number.
        
        >>> from network import Network
        >>> net = Network()
        >>> host = Host("192.168.1.10", net)
        
        >>> pkt1 = host.send_packet("192.168.1.20", "Hello!")
        >>> pkt1.payload
        'Hello!'
        
        >>> pkt1.sequence
        1
        
        >>> pkt2 = host.send_packet("192.168.2.30", "Second message")
        >>> pkt2.sequence
        2
        
        >>> pkt3 = host.send_packet("10.0.0.1", "Third")
        >>> pkt3.sequence
        3
        """
        new_packet = Packet(self.ip_address, IPAddress(destination_ip_string), payload, sequence=self.sequence)

        self.sequence += 1

        return new_packet
    
    def send_packet(self, destination_ip_string, payload):
        """
        Send a packet to a destination through the network.
        
        KEY NETWORKING CONCEPT:
        The packet's destination IP is the FINAL destination, but the
        host must determine the NEXT HOP for physical delivery:
        - Same network (/24) -> send directly to destination
        - Different network -> send to gateway (router)
        
        Steps:
        1. Create packet using create_packet()
        2. Determine next hop using _determine_next_hop()
        3. Ask network to deliver to next hop (not destination!)
        4. Return the packet (for testing)
        
        Args:
            destination_ip_string (str): Final destination IP address
            payload (str): Message to send
        
        Returns:
            Packet: The created packet
        
        >>> from network import Network
        >>> from router import Router
        >>> net = Network()
        >>> router = Router(\"192.168.1.1\", net)
        >>> host_a = Host(\"192.168.1.10\", net, gateway=\"192.168.1.1\")
        >>> host_b = Host(\"192.168.1.20\", net, gateway=\"192.168.1.1\")
        >>> host_c = Host(\"192.168.2.20\", net, gateway=\"192.168.1.1\")
        >>> net.register_device(router)
        >>> net.register_device(host_a)
        >>> net.register_device(host_b)
        >>> net.register_device(host_c)
        
        # Test 1: Same network - direct delivery
        >>> pkt1 = host_a.send_packet(\"192.168.1.20\", \"Direct message\")
        >>> len(host_b.inbox)
        1
        >>> host_b.inbox[0].payload
        'Direct message'
        >>> pkt1.ttl
        10
        
        # Test 2: Different network - via router
        >>> router.add_route(\"192.168.2.20\", host_c)
        >>> pkt2 = host_a.send_packet(\"192.168.2.20\", \"Via router\")
        >>> len(host_c.inbox)
        1
        >>> host_c.inbox[0].payload
        'Via router'
        >>> pkt2.ttl
        9
        
        # Test 3: No gateway - packet dropped
        >>> host_d = Host(\"192.168.1.30\", net)
        >>> net.register_device(host_d)
        >>> pkt3 = host_d.send_packet(\"192.168.2.20\", \"No route\")
        >>> len(host_c.inbox)
        1
        """
        pass

    
    def receive_packet(self, packet):
        """
        Receive a packet and store it in the inbox.
        
        This overrides the Device.receive_packet() method.
        Hosts are endpoints, so they store packets rather than forwarding.
        
        Args:
            packet (Packet): The packet being received
        
        >>> from network import Network
        >>> net = Network()
        >>> host = Host("192.168.1.10", net)
        >>> src = IPAddress("192.168.1.20")
        >>> dst = IPAddress("192.168.1.10")
        >>> pkt = Packet(src, dst, "Test message")
        
        >>> host.receive_packet(pkt)
        >>> len(host.inbox)
        1
        
        >>> host.inbox[0].payload
        'Test message'
        """
        self.inbox.append(packet)
    
    def get_messages(self):
        """
        Get all received message payloads from the inbox.
        
        Returns a list of just the payload strings (not full packets).
        
        Returns:
            list: List of message strings
        
        >>> from network import Network
        >>> net = Network()
        >>> host = Host("192.168.1.10", net)
        
        >>> src = IPAddress("192.168.1.20")
        >>> dst = IPAddress("192.168.1.10")
        >>> host.receive_packet(Packet(src, dst, "First"))
        >>> host.receive_packet(Packet(src, dst, "Second"))
        >>> host.receive_packet(Packet(src, dst, "Third"))
        
        >>> host.get_messages()
        ['First', 'Second', 'Third']
        
        >>> host2 = Host("192.168.1.30", net)
        >>> host2.get_messages()
        []
        """
        return [packet.payload for packet in self.inbox]
    
    def _determine_next_hop(self, destination_ip_string):
        """
        Determine the next hop IP address for a destination.
        
        This is a key networking concept: hosts make basic routing decisions.
        
        ROUTING LOGIC:
        1. Check if destination is on the same network (use is_same_network)
        2. If same network -> return destination IP (direct delivery)
        3. If different network -> return gateway IP (send to router)
        4. If no gateway configured -> return None (packet dropped)
        
        Args:
            destination_ip_string (str): Final destination IP address
        
        Returns:
            str: Next hop IP address, or None if no route available
        
        >>> from network import Network
        >>> net = Network()
        >>> host = Host("192.168.1.10", net, gateway="192.168.1.1")
        
        # Same network - direct delivery
        >>> host._determine_next_hop("192.168.1.20")
        '192.168.1.20'
        
        >>> host._determine_next_hop("192.168.1.100")
        '192.168.1.100'
        
        # Different network - use gateway
        >>> host._determine_next_hop("192.168.2.20")
        '192.168.1.1'
        
        >>> host._determine_next_hop("10.0.0.1")
        '192.168.1.1'
        
        # No gateway configured - no route
        >>> host2 = Host("192.168.1.30", net)
        >>> host2._determine_next_hop("192.168.2.20") is None
        True
        """        
        pass
    
    def __str__(self):
        """
        Return string representation of host.
        
        Returns:
            str: Host type and IP address
        
        >>> from network import Network
        >>> net = Network()
        >>> host = Host("192.168.1.10", net)
        >>> print(host)
        Host @ 192.168.1.10
        """
        return f'Host @ {self.ip_address}'
