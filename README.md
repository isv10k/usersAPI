# Simple api for user management
Accepts GET, POST, PATCH, DELETE

POST body example:

	endpoint /users/
	{"name": "John", "age": 20}
	[{"name": "Bill", "age": 37}, {"name": "Kate", "age": 30}]
	
GET endpoints:

	/users/
	/users/1
	
DELETE endpoints:

	/users/
	/users/1
	
PATCH endpoints:

	/users/
	/users/1
	body exmample:
	{"name": "Joe"}
