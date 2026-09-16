def test_create_transaction(client):
  # Registering user
  register_response = client.post(
    "/auth/register",
    json={
      "username": "robaak1105",
      "email": "akroba1105@gmail.com",
      "password": "robaak11050303"
    }
  )

  assert register_response.status_code == 201

  # Logging in user 
  login_response = client.post(
    "/auth/login",
    json={
      "username": "robaak1105",
      "password": "robaak11050303"
    }
  )

  assert login_response.status_code == 200

  # Retrieving token from response
  token = login_response.json()["access_token"]

  headers = {
    "Authorization": f"Bearer {token}"
  }

  # Creating a category for future use 
  category_response = client.post(
    "/categories",
    json={
      "name": "Cars"
    },
    headers=headers
  )

  assert category_response.status_code == 201

  # Putting category's id in a variable for future use
  category_id = int(category_response.json()["id"])

  # Creating a transaction
  transaction_response = client.post(
    "/transactions",
    json={
      "amount": "166150.00",
      "description": "Bought a G-Wagon at 19",
      "type": "expense",
      "category_id": category_id,
      "transaction_date": "2029-09-16T12:00:00"
    },
    headers=headers
  )

  assert transaction_response.status_code == 201

  data = transaction_response.json()

  assert data["amount"] == "166150.00"
  assert data["description"] == "Bought a G-Wagon at 19"
  assert data["type"] == "expense"
  assert data["category_id"] == category_id

def test_get_transaction(client):
  # Registering user
  register_response = client.post(
    "/auth/register",
    json={
      "username": "robaak1105",
      "email": "akroba1105@gmail.com",
      "password": "robaak11050303"
    }
  )
  
  assert register_response.status_code == 201 

  # Logging user in 
  login_response = client.post(
    "/auth/login",
    json={
      "username": "robaak1105",
      "password": "robaak11050303"
    }
  )

  assert login_response.status_code == 200

  token = login_response.json()["access_token"]

  headers = {
    "Authorization": f"Bearer {token}"
  }

  # Creating category 
  category_response = client.post(
    "/categories",
    json={
      "name": "Real Estate"
    },
    headers=headers
  )

  # Getting category's id from category_response
  category_id = category_response.json()["id"]

  assert category_response.status_code == 201 

  # Creating transnaction 
  transaction_response = client.post(
    "/transactions",
    json={
      "amount": "565000.00",
      "description": "Bought a big house with 2 garages and pool.",
      "type": "expense",
      "category_id": category_id,
      "transaction_date": "2029-09-16T12:00:00"
    },
    headers=headers
  )

  # Getting transactions id from transaction_response
  transaction_id = transaction_response.json()["id"]

  assert transaction_response.status_code == 201

  # Getting specific Transaction
  response = client.get(
    f"/transactions/{transaction_id}",
    headers=headers
  )

  data = response.json()

  assert response.status_code == 200

  assert data["id"] == transaction_id
  assert data["amount"] == "565000.00"
  assert data["description"] == "Bought a big house with 2 garages and pool."
  assert data["type"] == "expense"
  assert data["transaction_date"] == "2029-09-16T12:00:00"

def test_patch_transaction(client):
  # Registering a user
  register_response = client.post(
    "/auth/register",
    json={
      "username": "akroba1105",
      "email": "akroba1105@gmail.com",
      "password": "robaak11050303"
    }
  )

  assert register_response.status_code == 201

  # Logging user in
  login_response = client.post(
    "/auth/login",
    json={
      "username": "akroba1105",
      "password": "robaak11050303"
    }
  )

  assert login_response.status_code == 200 

  token = login_response.json()["access_token"]

  headers = {
    "Authorization": f"Bearer {token}"
  }

  # Creating a category 
  category_response = client.post(
    "/categories",
    json = {
      "name": "Balance"
    },
    headers=headers
  )

  assert category_response.status_code == 201

  category_id = category_response.json()["id"]

  # Creating a transaction 
  transaction_response = client.post(
    "/transactions",
    json={
      "amount": "40000.00",
      "description": "Monthly paycheck.",
      "type": "income",
      "category_id": category_id,
      "transaction_date": "2027-09-16T12:00:00"
    },
    headers=headers
  )

  transaction_id = transaction_response.json()["id"]

  assert transaction_response.status_code == 201 

  # Patch a transaction 
  response = client.patch(
    f"/transactions/{transaction_id}",
    json={
      "amount": "56000.00",
      "description": "Monthly paycheck with bonus."      
    },
    headers=headers
  )

  assert response.status_code == 200

  data = response.json()

  assert data["id"] == transaction_id
  assert data["amount"] == "56000.00"
  assert data["description"] == "Monthly paycheck with bonus."
  assert data["type"] == "income"
  assert data["category_id"] == category_id
  assert data["transaction_date"] == "2027-09-16T12:00:00"

def test_delete_transaction(client):
  # Registering user
  register_response = client.post(
    "/auth/register",
    json={
      "username": "robaak1105",
      "email": "akroba1105@gmail.com",
      "password": "akroba11050303"
    }
  )

  assert register_response.status_code == 201

  # Logging user in 
  login_response = client.post(
    "/auth/login",
    json={
      "username": "robaak1105",
      "password": "akroba11050303"
    }
  )

  assert login_response.status_code == 200

  token = login_response.json()["access_token"]

  headers = {
    "Authorization": f"Bearer {token}"
  }

  # Creating a category 
  category_response = client.post(
    "/categories",
    json={
      "name": "Infra bill"
    },
    headers=headers
  )

  assert category_response.status_code == 201

  category_id = category_response.json()["id"]

  # Creating a transaction
  transaction_response = client.post(
    "/transactions",
    json={
      "amount" : "2238.43",
      "description": "Bill from AWS services.",
      "category_id": category_id,
      "type": "expense",
      "transaction_date": "2029-06-24T12:00:00"
    },
    headers=headers
  )

  data = transaction_response.json()

  assert transaction_response.status_code == 201 

  transaction_id = data["id"]
    
  assert data["amount"] == "2238.43"
  assert data["description"] == "Bill from AWS services."
  assert data["category_id"] == category_id
  assert data["type"] == "expense"
  assert data["transaction_date"] == "2029-06-24T12:00:00"
  
  # Deleting a transaction
  delete_response = client.delete(
    f"/transactions/{transaction_id}",
    headers=headers
  )

  assert delete_response.status_code == 204

  # Retrieving a transaction by its id, which was deleted earlier 
  get_transaction_by_id_response = client.get(
    f"/transactions/{transaction_id}",
    headers=headers
  )

  assert get_transaction_by_id_response.status_code == 404

def test_get_specific_transaction(client):
  # Registering user
  register_response = client.post(
    "/auth/register",
    json={
      "username": "robaak1105",
      "email": "akroba1105@gmail.com",
      "password": "akroba11050303"
    }
  )

  assert register_response.status_code == 201

  # Logging user in 
  login_response = client.post(
    "/auth/login",
    json={
      "username": "robaak1105",
      "password": "akroba11050303"
    }
  )

  assert login_response.status_code == 200

  token = login_response.json()["access_token"]

  headers = {
    "Authorization": f"Bearer {token}"
  }

  # Creating a category 
  category_response = client.post(
    "/categories",
    json={
      "name": "Infra bill"
    },
    headers=headers
  )

  assert category_response.status_code == 201

  category_id = category_response.json()["id"]

  # Creating a transaction 1
  transaction_response_1 = client.post(
    "/transactions",
    json={
      "amount" : "2238.43",
      "description": "Bill from AWS services.",
      "category_id": category_id,
      "type": "expense",
      "transaction_date": "2029-06-24T12:00:00"
    },
    headers=headers
  )  

  assert transaction_response_1.status_code == 201

  # Creating transnaction 2
  transaction_response_2 = client.post(
    "/transactions",
    json={
      "amount": "166150.00",
      "description": "Bought a G-Wagon at 19",
      "type": "expense",
      "category_id": category_id,
      "transaction_date": "2029-09-16T12:00:00"
    },
    headers=headers
  )  

  assert transaction_response_2.status_code == 201

  # Creating transnaction 3
  transaction_response_3 = client.post(
    "/transactions",
    json={
      "amount": "565000.00",
      "description": "Bought a big house with 2 garages and pool.",
      "type": "expense",
      "category_id": category_id,
      "transaction_date": "2029-09-16T12:00:00"
    },
    headers=headers
  )

  assert transaction_response_3.status_code == 201

  # Creating a transaction 4
  transaction_response_4 = client.post(
    "/transactions",
    json={
      "amount": "40000.00",
      "description": "Monthly paycheck.",
      "type": "income",
      "category_id": category_id,
      "transaction_date": "2027-09-16T12:00:00"
    },
    headers=headers
  )

  assert transaction_response_4.status_code == 201

  # Calling get on all transactions
  get_all_transactions = client.get(
    "/transactions",
    headers=headers
  )

  assert get_all_transactions.status_code == 200

  all_transactions = get_all_transactions.json()

  assert isinstance(all_transactions, list)

  user_id = register_response.json()["id"]

  for transaction in all_transactions:
    assert transaction["user_id"] == user_id

  # Checking query parameters
  get_transactions_by_query_search_response = client.get(
    "/transactions?page=1&page_size=2",
    headers=headers
  )

  all_transactions_query = get_transactions_by_query_search_response.json()

  assert isinstance(all_transactions_query, list)
  assert len(all_transactions_query) == 2