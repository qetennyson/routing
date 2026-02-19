"""
Example network simulation demonstrating 2-hop routing.

This file shows how all the classes work together to simulate
packet routing through a network with hosts and routers.

Once you've implemented all the classes, run this file to see
your network simulation in action!

Usage:
    python example_simulation.py
"""

from network import Network
from host import Host
from router import Router


def main():
    print("=" * 60)
    print("Network Simulation: 2-Hop Routing Demo")
    print("=" * 60)
    print()
    
    # Step 1: Create the network
    print("Step 1: Creating network...")
    net = Network()
    print(f"[OK] {net}")
    print()
    
    # Step 2: Create devices
    print("Step 2: Creating devices...")
    host_a = Host("192.168.1.10", net)
    router = Router("192.168.1.1", net)
    host_b = Host("192.168.2.20", net)
    print(f"[OK] {host_a}")
    print(f"[OK] {router}")
    print(f"[OK] {host_b}")
    print()
    
    # Step 3: Register devices with network
    print("Step 3: Registering devices with network...")
    net.register_device(host_a)
    net.register_device(router)
    net.register_device(host_b)
    print(f"[OK] All devices registered")
    print(f"[OK] {net}")
    print()
    
    # Step 4: Configure router routing table
    print("Step 4: Configuring router routes...")
    router.add_route("192.168.1.10", host_a)  # Route to host A
    router.add_route("192.168.2.20", host_b)  # Route to host B
    print(f"[OK] Router has {len(router.routing_table)} routes")
    print()
    
    # Step 5: Send packets through the network
    print("Step 5: Sending packets...")
    print()
    
    # Packet 1: Host A -> Router -> Host B
    print("Sending: Host A (192.168.1.10) -> Router -> Host B (192.168.2.20)")
    print("Message: 'Hello from Host A!'")
    
    # Host A sends to router (since it's in different network)
    # In a real implementation, Host would know to send to router
    # For this demo, we'll simulate by having Host A create packet
    # and manually route it through router
    from packet import Packet
    from ip_address import IPAddress
    
    src = IPAddress("192.168.1.10")
    dst = IPAddress("192.168.2.20")
    pkt1 = Packet(src, dst, "Hello from Host A!", ttl=10, sequence=1)
    
    print(f"Created: {pkt1}")
    print("Routing through router...")
    router.receive_packet(pkt1)
    print(f"Packet TTL after routing: {pkt1.ttl}")
    print()
    
    # Packet 2: Host B -> Router -> Host A  
    print("Sending: Host B (192.168.2.20) -> Router -> Host A (192.168.1.10)")
    print("Message: 'Reply from Host B!'")
    
    src2 = IPAddress("192.168.2.20")
    dst2 = IPAddress("192.168.1.10")
    pkt2 = Packet(src2, dst2, "Reply from Host B!", ttl=10, sequence=2)
    
    print(f"Created: {pkt2}")
    print("Routing through router...")
    router.receive_packet(pkt2)
    print(f"Packet TTL after routing: {pkt2.ttl}")
    print()
    
    # Step 6: Check messages received
    print("Step 6: Checking received messages...")
    print()
    
    print(f"Host A inbox ({len(host_a.inbox)} packets):")
    for msg in host_a.get_messages():
        print(f"  - {msg}")
    print()
    
    print(f"Host B inbox ({len(host_b.inbox)} packets):")
    for msg in host_b.get_messages():
        print(f"  - {msg}")
    print()
    
    # Step 7: Demonstrate TTL expiration
    print("Step 7: Demonstrating TTL expiration...")
    print()
    
    src3 = IPAddress("192.168.1.10")
    dst3 = IPAddress("192.168.2.20")
    pkt3 = Packet(src3, dst3, "This will expire!", ttl=1)
    
    print(f"Created packet with TTL=1: {pkt3}")
    print("Forwarding through router (should be dropped)...")
    
    initial_count = len(host_b.inbox)
    router.forward_packet(pkt3)
    
    if len(host_b.inbox) == initial_count:
        print("[OK] Packet was dropped (TTL expired)")
    else:
        print("[FAIL] Packet was not dropped (check TTL logic)")
    print()
    
    print("=" * 60)
    print("Simulation Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
