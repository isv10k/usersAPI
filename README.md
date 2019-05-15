# Simple api for user management
Accepts GET, POST, PATCH, DELETE
POST body example:
	/users/
	{"name": "John", "age": 20}
	[{"name": "Bill", "age": 37}, {"name": "Kate", "age": 30}]
GET 
	/users/
	/users/1
DELETE
	/users/
	/users/1
PATCH
	/users/
	/users/1
	body exmample:
	{"name": "Joe"}}
