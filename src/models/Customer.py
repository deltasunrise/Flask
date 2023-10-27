from src.models.Driver import _get_connection



class Customer:
    def __init__(self, customer_id, name, email, phone, address):
        self.name = name
        self.customer_id = customer_id
        self.email = email
        self.phone = phone
        self.address = address

def list_customers():
    list_customers = []
    driver = _get_connection()
    if driver != None:
        with driver.session() as session:
            try:
                result = session.run("MATCH (c:Customer) RETURN ID(c) as id, c.name as name, c.email as email, c.phone as phone, c.address as address")
                for record in result:
                    list_customers.append({
                    'id' : record["id"],
                    'name' : record["name"],
                    'email' : record["email"],
                    'phone' : record["phone"],
                    'address' : record["address"]
                    })
                print(list_customers)
                return list_customers
            except Exception as e:
                print(f"Error: {e}")
                return list_customers


def add_customer(name,email,phone,address):
    driver = _get_connection()
    if driver != None:
        with driver.session() as session:
            try:
                result = session.run(
                    "CREATE (c:Customer {name: $name, email: $email, phone: $phone, address: $address})",
                    name=name,
                    email=email,
                    phone=phone,
                    address=address
                    )
                record = result.single()
                if record:
                    customer_id = record['id']
                    session.run("MATCH (c:Customer) WHERE ID(c) = $customer_id SET c.customer_id = toString($customer_id)", customer_id=customer_id)



                return
            except Exception as e:
                print(f"Error: {e}")
                return
    print("Driver not connected")


def update_customer(id, newAddress):
    driver = _get_connection()
    if driver != None:
        with driver.session() as session:
            try:
                session.run(
                    "MATCH (c:Customer) WHERE ID(c) = $id SET c.address = $newAddress", 
                    id=id,
                    newAddress=newAddress
                    )
                return
            except Exception as e:
                print(f"Error: {e}")
                return
    print("Driver not connected")

    

def delete_customer(id):
    driver = _get_connection()
    if driver != None:
        with driver.session() as session:
            try:
                session.run(
                    "MATCH (c:Customer) WHERE ID(c) = $id DETACH DELETE c", 
                    id=id
                    )
                return
            except Exception as e:
                print(f"Error: {e}")
                return
    print("Driver not connected")