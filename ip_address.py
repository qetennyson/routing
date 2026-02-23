"""
IPAddress class for representing and validating IPv4 addresses.

This class handles parsing, validation, and comparison of IP addresses
in dotted-decimal notation (e.g., "192.168.1.1").
"""


class IPAddress:
    """
    Represents an IPv4 address with validation and utility methods.
    
    An IP address consists of four octets (numbers 0-255) separated by dots.
    Example: 192.168.1.1
    """
    
    def __init__(self, ip_string):
        """
        Initialize an IPAddress from a string in dotted-decimal format.
        
        Args:
            ip_string (str): IP address as string (e.g., "192.168.1.1")
        
        This constructor must:
        1. Call the _parse_ip_string private method (the _ indicates this method should never be used outside the class)
        2. Store the result in an attribute called self.octets
        
        If the IP is invalid (wrong format, out of range, non-numeric), 
        store None in self.octets so is_valid() can detect it.
        
        >>> ip = IPAddress("192.168.1.1")
        >>> ip.octets
        [192, 168, 1, 1]
        
        >>> ip = IPAddress("10.0.0.1")
        >>> ip.octets
        [10, 0, 0, 1]
        
        >>> ip = IPAddress("255.255.255.0")
        >>> ip.octets
        [255, 255, 255, 0]
        
        >>> ip = IPAddress("invalid")
        >>> ip.octets is None
        True
        
        >>> ip = IPAddress("256.1.1.1")
        >>> ip.octets is None
        True
        """
        self.octets = self._parse_ip_string(ip_string)
        self.gateway = gateway

    

    def _parse_ip_string(self, ip_string):
        """
        Helper method to parse and validate IP string into octets list.
        
        Args:
            ip_string (str): IP address string to parse
        
        Returns:
            list or None: List of 4 integers if valid, None if invalid
        
        This is a private helper (note the _ prefix) that:
        1. Splits on '.'
        2. Validates count (must be 4 parts)
        3. Converts to integers
        4. Validates range (0-255)
        """
        # Your validation logic goes here
        # Return list of ints or None
        octets = []
        
        if not ip_string:
            return None
        
        octet_strings = ip_string.split('.')

        if len(octet_strings) != 4:
            return None
        
        for octet in octet_strings:
            if not octet.isdigit():
                return None
            else:
                int_octet = int(octet)
                if not (0 <= int_octet <= 255):
                    return None
                else:
                    octets.append(int_octet)

        return octets
        
    def is_same_network(self):

    def is_valid(self):
        """
        Check if this IP address is valid.
        
        Since validation happens in __init__ via _parse_ip_string,
        this method just checks if self.octets is not None.
        
        Returns:
            bool: True if valid, False otherwise
        
        >>> IPAddress("192.168.1.1").is_valid()
        True
        
        >>> IPAddress("255.255.255.255").is_valid()
        True
        
        >>> IPAddress("0.0.0.0").is_valid()
        True
        
        >>> IPAddress("256.1.1.1").is_valid()
        False
        
        >>> IPAddress("192.168.1").is_valid()
        False
        
        >>> IPAddress("192.168.1.1.1").is_valid()
        False
        
        >>> IPAddress("abc.def.ghi.jkl").is_valid()
        False
        
        >>> IPAddress("").is_valid()
        False
        """
        return self.octets is not None

    
    def get_octets(self):
        """
        Get the four octets of the IP address as a list of integers.
        
        Simply returns the stored self.octets attribute.
        
        Returns:
            list: List of four integers [octet1, octet2, octet3, octet4]
        
        >>> IPAddress("192.168.1.1").get_octets()
        [192, 168, 1, 1]
        
        >>> IPAddress("10.0.0.255").get_octets()
        [10, 0, 0, 255]
        """
        return self.octets
    
    def matches_prefix(self, prefix):
        """
        Check if this IP address starts with the given prefix.
        
        Used for routing table lookups with simple prefix matching.
        This is commonly used in Router.forward_packet() to check if
        a packet's destination IP matches a routing table entry.

        Hint: Return False if self.octets is invalid, i.e. None
        
        Args:
            prefix (str): IP prefix to match (e.g., "192.168.1" or "10.0")
        
        Returns:
            bool: True if IP starts with prefix, False otherwise
        
        >>> ip = IPAddress("192.168.1.10")
        >>> ip.matches_prefix("192.168.1")
        True
        
        >>> ip.matches_prefix("192.168")
        True
        
        >>> ip.matches_prefix("192")
        True
        
        >>> ip.matches_prefix("10")
        False
        
        >>> ip.matches_prefix("192.168.1.10")
        True
        
        >>> ip2 = IPAddress("10.0.0.1")
        >>> ip2.matches_prefix("10.0")
        True
        
        >>> ip2.matches_prefix("10")
        True
        
        >>> ip2.matches_prefix("192")
        False
        """
        if not self.octets:
            return False
        
        prefix_octets = prefix.split(".")
        for index, octet in enumerate(prefix_octets):
            if not(str(octet) == str(self.octets[index])):
                return False
        return True



    
    def __str__(self):
        """
        Return string representation of IP address in dotted-decimal format.
        
        Reconstruct the dotted-decimal string from self.octets by joining
        with periods. Convert each integer octet to a string first.

        Hint: Return False if self.octets is invalid, i.e. None
        
        Returns:
            str: IP address as "octet.octet.octet.octet"
        
        >>> str(IPAddress("192.168.1.1"))
        '192.168.1.1'
        
        >>> str(IPAddress("10.0.0.1"))
        '10.0.0.1'
        """
        if not self.octets:
            return False
        
        return '.'.join(str(octet) for octet in self.octets)
    
    def __eq__(self, other):
        """
        Check if two IP addresses are equal.
        
        Args:
            other (IPAddress): Another IP address to compare
        
        Returns:
            bool: True if addresses are equal, False otherwise
        
        >>> IPAddress("192.168.1.1") == IPAddress("192.168.1.1")
        True
        
        >>> IPAddress("192.168.1.1") == IPAddress("192.168.1.2")
        False
        
        >>> IPAddress("10.0.0.1") == IPAddress("10.0.0.1")
        True
        """
        return self.octets == other.octets
    
    def is_same_network(self, other_ip):
        """
        Check if another IP address is on the same /24 network.
        
        Two IPs are on the same network if their first 3 octets match.
        This simulates a /24 subnet mask (255.255.255.0).
        
        KEY NETWORKING CONCEPT:
        Hosts use this to decide routing:
        - Same network → send directly to destination
        - Different network → send to gateway (router)
        
        Args:
            other_ip (IPAddress): Another IP address to compare
        
        Returns:
            bool: True if on same /24 network, False otherwise
        
        >>> ip1 = IPAddress("192.168.1.10")
        >>> ip2 = IPAddress("192.168.1.20")
        >>> ip1.is_same_network(ip2)
        True
        
        >>> ip3 = IPAddress("192.168.2.20")
        >>> ip1.is_same_network(ip3)
        False
        
        >>> ip4 = IPAddress("10.0.0.1")
        >>> ip5 = IPAddress("10.0.0.50")
        >>> ip4.is_same_network(ip5)
        True
        
        >>> ip6 = IPAddress("10.0.1.1")
        >>> ip4.is_same_network(ip6)
        False
        """
        pass
