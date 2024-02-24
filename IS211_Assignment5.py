import csv

class Request:
    def __init__(self, generation_time, file_name, processing_time):
        self.generation_time = generation_time
        self.file_name = file_name
        self.processing_time = processing_time

class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def busy(self):
        return self.current_request != None

    def tick(self):
        if self.current_request != None:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_request = None

    def start_next(self, new_request):
        self.current_request = new_request
        self.time_remaining = new_request.processing_time

def simulateOneServer(filename):
    server = Server()
    request_queue = []

    with open(filename, 'r') as file:
        requests_data = csv.reader(file)
        for row in requests_data:
            generation_time, file_name, processing_time = row
            request = Request(int(generation_time), file_name, int(processing_time))
            request_queue.append(request)

    total_latency = 0
    num_requests = len(request_queue)

    current_time = 0
    while request_queue or server.busy():
        if request_queue:
            current_request = request_queue.pop(0)
            total_latency += current_time - current_request.generation_time
            current_time += current_request.processing_time
            server.start_next(current_request)
        else:
            server.tick()
            current_time += 1

    average_latency = total_latency / num_requests
    print(f"Average latency with one server: {average_latency}")

def simulateManyServers(filename, num_servers):
    servers = [Server() for _ in range(num_servers)]
    request_queues = [[] for _ in range(num_servers)]

    with open(filename, 'r') as file:
        requests_data = csv.reader(file)
        for row in requests_data:
            generation_time, file_name, processing_time = row
            request = Request(int(generation_time), file_name, int(processing_time))
            request_queues[int(generation_time) % num_servers].append(request)

    total_latency = 0
    num_requests = sum(len(queue) for queue in request_queues)

    current_time = 0
    while any(server.busy() or queue for server, queue in zip(servers, request_queues)):
        for server, queue in zip(servers, request_queues):
            if queue:
                current_request = queue.pop(0)
                total_latency += current_time - current_request.generation_time
                server.start_next(current_request)
            else:
                server.tick()
        current_time += 1

    average_latency = total_latency / num_requests
    print(f"Average latency with {num_servers} servers: {average_latency}")

def main(filename, num_servers=1):
    if num_servers == 1:
        simulateOneServer(filename)
    else:
        simulateManyServers(filename, num_servers)

if __name__ == "__main__":
    main("/Users/asiamobley/Downloads/requests.csv", num_servers=1)
  

