"""
Device base class for network devices (hosts and routers).

This is an abstract base class that defines the common interface
and attributes for all network devices.
"""

from ip_address import IPAddress


class Device:
    """
    Abstract base class for network devices.
    
    All network devices (hosts, routers) share common properties:
    - Each device has an IP address
    - Each device is part of a network
    - Each device can receive packets
    
    Subclasses must implement their own receive_packet() behavior.
    """
    
    def __init__(self, ip_string, network):
        """
        Initialize a network device.

        Hint: Your receiving an "ip string", but that should become an IPAddress! (think: 'composition' in Object-oriented Programming)
        
        Hint 2: Your self.attribute for the ip_string should probably be ip_address, rather than ip_string.
        
        Args:
            ip_string (str): IP address for this device
            network (Network): The network this device belongs to
        
        >>> from network import Network
        >>> net = Network()
        >>> device = Device("192.168.1.1", net)
        >>> str(device.ip_address)
        '192.168.1.1'
        >>> device.network is net
        True
        """
        self.ip_address = IPAddress(ip_string)
        self.network = network
    
    def receive_packet(self, packet):
        """
        Receive a packet (abstract method - subclasses implement this).
        
        Different device types handle packets differently:
        - Hosts: Store packet in inbox
        - Routers: Forward packet to next hop
        
        Args:
            packet (Packet): The packet being received
        
        This is the base implementation. Subclasses override this method.
        There is NOTHING more to do!
        """
        pass
    
    def __str__(self):
        """
        Return string representation of device.
        
        Returns:
            str: Device type and IP address
        
        >>> from network import Network
        >>> net = Network()
        >>> device = Device("192.168.1.1", net)
        >>> print(device)
        Device @ 192.168.1.1
        """
        return f'Device @ {self.ip_address}'
