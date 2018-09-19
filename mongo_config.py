from pymodm.connection import connect

# Connect to MongoDB and call the connection "my-app".
connect("mongodb://localhost:27017/snap", alias="snap-app")
