from concurrent import futures
import grpc
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from emp_pb2_grpc import add_DataManagementServicer_to_server, DataManagementServicer
from emp_pb2 import Employee, Employees, ConnectionRequest, Response, Connections, AllConnections


class DataManagementServicer(DataManagementServicer):
    def __init__(self):
        self.emp_list = Employees()
        self.connections_graph = AllConnections()
    
    def check_employee(self, id):
        if id in [emp.id for emp in self.emp_list.employees]:
            return Response(statuscode=400, message=f"Employee with ID: {id} already exists")
        return Response(statuscode=200, message=f"Employee with ID {id} does not exists.")

    def createemployee(self, request, context):
        print(f"Request received to create employee:\n{request}")
        response = self.check_employee(request.id)
        if response.statuscode == 400:
            return response
        response = Employee(
            id=request.id,
            name=request.name,
            salary=request.salary,
            cab=request.cab,
        )
        self.emp_list.employees.append(response)
        # self.employees.sort(key=lambda x:x.id)
        # print(dict(context.invocation_metadata()))
        return Response(statuscode=200, message=f"Added employee with ID: {request.id}")

    def reademployees(self, request, context):
        return self.emp_list

    def readconnections(self, request, context):
        return self.connections_graph

    def establishconnection(self, request, context):
        response = self.check_employee(request.emp1_id)
        if response.statuscode == 200:
            return response
        response = self.check_employee(request.emp2_id)
        if response.statuscode == 200:
            return response

        def create_connection(emp1_id, emp2_id):
            print(f"Adding connection of {emp1_id} into connections array of {emp2_id} employee")
            connections = self.connections_graph.connections.get(emp1_id)
            print(f"Existing connections of {emp1_id} are: {connections}")
            if connections is not None:
                if emp2_id in connections.connected_to:
                    return Response(statuscode=400, message=f"Employee with ID {emp1_id} already connected with {emp2_id}.")
            self.connections_graph.connections[emp1_id].connected_to.append(emp2_id)
            return Response(statuscode=200, message=f"Employee with ID {emp1_id} connected with {emp2_id}.")
        
        response = create_connection(request.emp1_id, request.emp2_id)
        if response.statuscode == 400:
            return response
        response = create_connection(request.emp2_id, request.emp1_id)
        if response.statuscode == 400:
            return response
        
        return Response(statuscode=200, message=f"Employee with ID {request.emp1_id} and {request.emp2_id} mutually connected.")
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DataManagementServicer_to_server(DataManagementServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Listening at 50051")
    server.wait_for_termination()

if __name__=="__main__":
    serve()