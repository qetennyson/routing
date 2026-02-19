"""
Packet class for representing network packets with headers and payload.

Packets contain source/destination addresses, data payload, and metadata
like TTL (Time To Live) and sequence numbers.
"""

from ip_address import IPAddress


class Packet:
    """
    Represents a network packet with addressing and metadata.
    
    Packets are sent between devices and contain:
    - Source and destination IP addresses
    - Payload data (the message)
    - TTL (Time To Live) to prevent infinite loops
    - Sequence number for tracking and ordering
    """
    
    def __init__(self, source, destination, payload, ttl=10, sequence=1):
        """
        Create a new packet.
        
        Args:
            source (IPAddress): Source IP address
            destination (IPAddress): Destination IP address
            payload (str): The message/data being sent
            ttl (int): Time To Live (default 10 hops)
            sequence (int): Packet sequence number (default 1)
        
        >>> src = IPAddress("192.168.1.10")
        >>> dst = IPAddress("192.168.2.20")
        >>> pkt = Packet(src, dst, "Hello", ttl=10, sequence=1)
        >>> pkt.payload
        'Hello'
        
        >>> pkt.ttl
        10
        
        >>> pkt.sequence
        1
        """
        self.src = source
        self.dest = destination
        self.payload = payload
        self.ttl = ttl
        self.sequence = sequence
        
    
    def decrement_ttl(self):
        """
        Decrease the TTL by 1 (called when packet passes through a router).
        
        Each router hop decrements TTL to prevent infinite routing loops.
        
        >>> src = IPAddress("192.168.1.10")
        >>> dst = IPAddress("192.168.2.20")
        >>> pkt = Packet(src, dst, "Test", ttl=5)
        >>> pkt.ttl
        5
        
        >>> pkt.decrement_ttl()
        >>> pkt.ttl
        4
        
        >>> pkt.decrement_ttl()
        >>> pkt.ttl
        3
        """
        self.ttl -= 1
    
    def is_expired(self):
        """
        Check if packet has expired (TTL reached 0).
        
        Expired packets should be dropped by routers.
        
        Returns:
            bool: True if TTL is 0, False otherwise
        
        >>> src = IPAddress("192.168.1.10")
        >>> dst = IPAddress("192.168.2.20")
        >>> pkt = Packet(src, dst, "Test", ttl=2)
        >>> pkt.is_expired()
        False
        
        >>> pkt.decrement_ttl()
        >>> pkt.is_expired()
        False
        
        >>> pkt.decrement_ttl()
        >>> pkt.is_expired()
        True
        """
        return self.ttl == 0
    
    def __str__(self):
        """
        Return string representation of packet.
        
        Format: "Packet[seq=X, ttl=Y]: source -> destination | payload"
        
        Returns:
            str: Human-readable packet representation
        
        >>> src = IPAddress("192.168.1.10")
        >>> dst = IPAddress("192.168.2.20")
        >>> pkt = Packet(src, dst, "Hello!", ttl=8, sequence=5)
        >>> print(pkt)
        Packet[seq=5, ttl=8]: 192.168.1.10 -> 192.168.2.20 | Hello!
        """
        return f'Packet[seq={self.sequence}, ttl={self.ttl}]: {self.src} -> {self.dest} | {self.payload}'
