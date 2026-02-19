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
        super().__init__(ip_string, network)
        self.inbox = []
        self.sequence = 1
    
    def send_packet(self, destination_ip_string, payload):
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
