## GRPC_Client_Server
A client server communication using  GRPC Proto structure
The function that client can call to retrieve data from server include:
```proto
rpc createemployee(Employee) returns(Response);
rpc reademployees(void) returns(Employees);
rpc readconnections(void) returns(AllConnections);
rpc establishconnection(ConnectionRequest) returns(Response);
rpc updatesalary(Employee) returns(Employee);
```
Implementation of the functions are in server/sender.py and calls are made in client/receiver.py
