"""This class is used for testing.  Do not modify it."""

class SimpleDevice:
    def __init__(self):
        self.inbox = []

    def receive_packet(self, pkt):
        self.inbox.append(pkt)