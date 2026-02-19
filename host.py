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
    
    def __init__(self, ip_string, network):
        """
        Initialize a host device.
        
        The host maintains an inbox (list) for received packets and
        a sequence counter that starts at 1 and auto-increments.
        
        Args:
            ip_string (str): IP address for this host
            network (Network): The network this host belongs to
        
        >>> from network import Network
        >>> net = Network()
        >>> host = Host("192.168.1.10", net)
        >>> str(host.ip_address)
        '192.168.1.10'
        
        >>> host.inbox
        []
        """
        pass
    
    def send_packet(self, destination_ip_string, payload):
        """
        Send a packet to a destination IP address.
        
        Creates a new packet with auto-incrementing sequence number,
        looks up the destination device in the network, and delivers
        the packet by calling the destination's receive_packet method.
        
        Args:
            destination_ip_string (str): Destination IP address
            payload (str): Message to send
        
        >>> from network import Network
        >>> net = Network()
        >>> host_a = Host("192.168.1.10", net)
        >>> host_b = Host("192.168.1.20", net)
        >>> net.register_device(host_a)
        >>> net.register_device(host_b)
        
        >>> host_a.send_packet("192.168.1.20", "Hello!")
        >>> len(host_b.inbox)
        1
        
        >>> host_b.inbox[0].payload
        'Hello!'
        
        >>> host_a.send_packet("192.168.1.20", "Second message")
        >>> len(host_b.inbox)
        2
        
        >>> host_b.inbox[1].sequence
        2
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
        pass
    
    def get_messages(self):
        """
        Get all received message payloads from the inbox.
        
        Returns a list of just the payload strings (not full packets).
        
        Returns:
            list: List of message strings
        
        >>> from network import Network
        >>> net = Network()
        >>> host_a = Host("192.168.1.10", net)
        >>> host_b = Host("192.168.1.20", net)
        >>> net.register_device(host_a)
        >>> net.register_device(host_b)
        
        >>> host_a.send_packet("192.168.1.20", "First")
        >>> host_a.send_packet("192.168.1.20", "Second")
        >>> host_a.send_packet("192.168.1.20", "Third")
        
        >>> host_b.get_messages()
        ['First', 'Second', 'Third']
        
        >>> host_c = Host("192.168.1.30", net)
        >>> host_c.get_messages()
        []
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
        pass
