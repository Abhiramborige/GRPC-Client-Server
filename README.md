## GRPC_Client_Server
A client server communication using  GRPC Proto structure.

The RPC calls that client can send to retrieve data from server include:
```proto
rpc createemployee(Employee) returns(Response);
rpc reademployees(void) returns(Employees);
rpc readconnections(void) returns(AllConnections);
rpc establishconnection(ConnectionRequest) returns(Response);
rpc updatesalary(Employee) returns(Employee);
```
Implementation of the functions are in server/sender.py and calls are made in client/receiver.py
To start with:
1. `pip install grpcio-tools`
2. `cd <project_path>`
3. `python -m grpc_tools.protoc --proto_path ./ --python_out ./ --pyi_out=./ --grpc_python_out=./ emp.proto`
4. To start the server: `python server\sender.py`
5. Modify the client accordingly as per wish and start calling RPCs: `python client/receiver.py`
