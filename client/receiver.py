import grpc
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from emp_pb2_grpc import DataManagementStub
from emp_pb2 import Employee, Employees, OptForCab, ConnectionRequest, AllConnections

import random
names = ["Abhiram", "Anil", "Manish", "Niraj", "Sayantan", "Ravi"]

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = DataManagementStub(channel)
        for i,name in enumerate(names):
            employee = Employee(
                id = i+1,
                name = name,
                salary = random.choice([3000, 4000, 5000]),
                cab = OptForCab.YES,
            )
            response = stub.createemployee(employee)
            print(response.__str__())

        print("All employees are:")
        response = stub.reademployees(Employees())
        print(response.__str__())

        response = stub.establishconnection(ConnectionRequest(
            emp1_id=3, 
            emp2_id=4
        ))
        print(response.__str__())
        print("All connections are:")
        response = stub.readconnections(AllConnections())
        print(response.__str__())

        


if __name__ == "__main__":
    run()
