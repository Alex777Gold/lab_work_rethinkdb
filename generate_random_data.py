import rethinkdb as rdb
import faker
import json

r = rdb.RethinkDB()

# Connect to the RethinkDB server
connection = r.connect(host='localhost', port=28015)
# Create a database and table
db_name = 'test_db'
table_name = 'test_table'
# Generate and insert data until the total size reaches 100 MB
fake = faker.Faker()
total_size_bytes = 0
target_size_mb = 1 * 1024 * 1024

while total_size_bytes < target_size_mb:
    # Generate fake data
    data = {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email(),
        'phone': fake.phone_number()
    }
    # Calculate the size of the data in bytes
    data_size_bytes = len(json.dumps(data))
    # Check if adding this data will exceed the target size
    if total_size_bytes + data_size_bytes > target_size_mb:
        break
    # Insert data into the table
    r.db(db_name).table(table_name).insert(data).run(connection)
    # Calculate the size of the inserted data in bytes
    total_size_bytes += len(json.dumps(data))
    print(total_size_bytes, "\n")
table_info = r.db('test_db').table('test_table').info().run(connection)
print(table_info)
# Close the connection
connection.close()

print(
    f"Data inserted successfully. Total size: {total_size_bytes / (1024*1024):.2f} MB")
