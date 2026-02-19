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
        pass
    
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
        pass
    
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
        pass
