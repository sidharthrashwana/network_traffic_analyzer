from scapy.all import *
import time
import network_analyzer_db as network_analyzer
from queue import Queue
import threading
import atexit
# Create a thread-safe queue to store captured packets as dictionaries
captured_packets_queue = Queue()
count =0

def insert_remaining_packets():
    print("Inserting remaining packets into the database...")
    remaining_packets = []

    while not captured_packets_queue.empty():
        remaining_packets.append(captured_packets_queue.get())

    if remaining_packets:
        packet_objects = [
            network_analyzer.NetworkAnalyzer(
                timestamp=packet["timestamp"],
                source_mac=packet["source_mac"],
                destination_mac=packet["destination_mac"],
                source_ip=packet["source_ip"],
                destination_ip=packet["destination_ip"],
                protocol=packet["protocol"],
                source_port=packet["source_port"],
                destination_port=packet["destination_port"],
                url=packet["dns-query"],
                length=packet["length"],
            )
            for packet in remaining_packets
        ]
        network_analyzer.insert_to_db_all(packet_objects)
        print("Inserted remaining packets into the database.")

def packet_handler(packet):
    global count

    """
        Ether : Layer
        IP : Layer
    """
    packet_dict = {
        "timestamp": packet.time,
        "source_mac":packet[Ether].src if Ether in packet else "N/A",
        "destination_mac":packet[Ether].dst if Ether in packet else "N/A",
        "source_ip": packet[IP].src if IP in packet else "N/A",
        "destination_ip": packet[IP].dst if IP in packet else "N/A",

    }
    source_port=dest_port=protocol = None
    if TCP in packet:
        protocol = "TCP"
        source_port = packet[TCP].sport
        dest_port = packet[TCP].dport
    elif UDP in packet:
        protocol = "UDP"
        source_port = packet[UDP].sport
        dest_port = packet[UDP].dport

    dns_query = None
    if packet.haslayer(DNSQR):
        dns_query = packet[DNSQR].qname.decode("utf-8")
        dns_query = dns_query.rstrip(".")  # Remove the trailing dot
    
    packet_dict.update({'source_port':source_port,
            'destination_port':dest_port,
            'length': len(packet),
            'dns-query':dns_query,
            'protocol': protocol
            })
    captured_packets_queue.put(packet_dict)
    count +=1
    print(packet_dict)
    print('\n',count)


def insert_packets():
    # Retrieve multiple packets from the queue at once
    while True:
        packet_batch = []
        for _ in range(100):
            #once the packet is read it will be popped from queue
            #if we add `captured_packets_queue.task_done()` then it will not be removed
            try:
                packet = captured_packets_queue.get(timeout=10000)  # Wait for 100000 second
                packet_batch.append(packet)
            except Empty:
                break  # Break if the queue is empty after waiting
        # packet = captured_packets_queue.get()
        if packet_batch:
            # Process and insert the batch of packets into the database
            packet_objects = [
                network_analyzer.NetworkAnalyzer(
                    timestamp=packet["timestamp"],
                    source_mac=packet["source_mac"],
                    destination_mac=packet["destination_mac"],
                    source_ip=packet["source_ip"],
                    destination_ip=packet["destination_ip"],
                    protocol=packet["protocol"],
                    source_port=packet["source_port"],
                    destination_port=packet["destination_port"],
                    url=packet["dns-query"],
                    length=packet["length"],
                )
                for packet in packet_batch
            ]
            network_analyzer.insert_to_db_all(packet_objects)


def sniff_packets():
    while True:
        sniff(iface="ens33", prn=packet_handler, count=1)
       
thread1 = threading.Thread(target=sniff_packets)
thread2 = threading.Thread(target=insert_packets)

try:
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
except Exception as e:
    print("Exiting...")
    insert_remaining_packets()