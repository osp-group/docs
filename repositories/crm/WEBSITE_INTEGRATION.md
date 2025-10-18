# Website Form to OSP CRM Integration Guide

This guide explains how to connect your website forms to OSP CRM so that form submissions automatically create leads, contacts, companies, and opportunities.

## Overview

Your website will send form data to OSP CRM's GraphQL API, which will automatically create records in your CRM database.

## Step 1: Generate an API Key in OSP CRM

1. **Login to OSP CRM** at http://localhost:3001
   - Email: `leopagotto@gmail.com`
   - Password: `2rec8kkk`

2. **Navigate to Settings → API & Webhooks**
   - Click on "Settings" (gear icon in the left sidebar)
   - Select "Developers" → "API Keys"

3. **Create a New API Key**
   - Click "New API Key"
   - Give it a name (e.g., "Website Integration")
   - Select a role with appropriate permissions
   - Set an expiration date (or leave blank for no expiration)
   - Click "Save"

4. **Copy the API Token**
   - After creating, you'll see the token displayed
   - **Copy this token immediately** - you won't be able to see it again!
   - It will look something like: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## Step 2: Understanding the GraphQL API

Your OSP CRM GraphQL API is available at:
```
http://localhost:3000/graphql
```

### Authentication
Include your API key in the Authorization header:
```
Authorization: Bearer YOUR_API_KEY_TOKEN
```

### Available Operations

#### 1. Create a Person (Contact)
```graphql
mutation CreatePerson($data: PersonCreateInput!) {
  createPerson(data: $data) {
    id
    name {
      firstName
      lastName
    }
    email
    phone
    city
    companyId
  }
}
```

**Variables:**
```json
{
  "data": {
    "name": {
      "firstName": "John",
      "lastName": "Doe"
    },
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "city": "San Francisco"
  }
}
```

#### 2. Create a Company
```graphql
mutation CreateCompany($data: CompanyCreateInput!) {
  createCompany(data: $data) {
    id
    name
    domainName
    address
    employees
  }
}
```

**Variables:**
```json
{
  "data": {
    "name": "Acme Corporation",
    "domainName": "acme.com",
    "address": "123 Main St, San Francisco, CA",
    "employees": 50
  }
}
```

#### 3. Create an Opportunity
```graphql
mutation CreateOpportunity($data: OpportunityCreateInput!) {
  createOpportunity(data: $data) {
    id
    name
    amount {
      amountMicros
      currencyCode
    }
    stage
    closeDate
    pointOfContactId
    companyId
  }
}
```

**Variables:**
```json
{
  "data": {
    "name": "Website Lead - John Doe",
    "amount": {
      "amountMicros": 5000000000,
      "currencyCode": "USD"
    },
    "stage": "NEW",
    "closeDate": "2025-12-31T00:00:00.000Z",
    "pointOfContactId": "person-id-here",
    "companyId": "company-id-here"
  }
}
```

## Step 3: Website Backend Integration

Here are examples in different languages:

### Node.js / Express Example

```javascript
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const CRM_API_URL = 'http://localhost:3000/graphql';
const API_KEY = 'YOUR_API_KEY_TOKEN_HERE';

app.post('/api/contact-form', async (req, res) => {
  try {
    const { firstName, lastName, email, phone, company, message } = req.body;

    // 1. Create the person
    const createPersonMutation = `
      mutation CreatePerson($data: PersonCreateInput!) {
        createPerson(data: $data) {
          id
          name {
            firstName
            lastName
          }
          email
        }
      }
    `;

    const personResponse = await axios.post(
      CRM_API_URL,
      {
        query: createPersonMutation,
        variables: {
          data: {
            name: { firstName, lastName },
            email,
            phone,
          },
        },
      },
      {
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    const personId = personResponse.data.data.createPerson.id;

    // 2. Create an opportunity
    const createOpportunityMutation = `
      mutation CreateOpportunity($data: OpportunityCreateInput!) {
        createOpportunity(data: $data) {
          id
          name
        }
      }
    `;

    await axios.post(
      CRM_API_URL,
      {
        query: createOpportunityMutation,
        variables: {
          data: {
            name: `Website Lead - ${firstName} ${lastName}`,
            stage: "NEW",
            pointOfContactId: personId,
          },
        },
      },
      {
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    res.json({ success: true, message: 'Lead created in CRM' });
  } catch (error) {
    console.error('CRM API Error:', error.response?.data || error.message);
    res.status(500).json({ success: false, error: 'Failed to create lead' });
  }
});

app.listen(3002, () => {
  console.log('Form handler running on port 3002');
});
```

### PHP Example

```php
<?php
define('CRM_API_URL', 'http://localhost:3000/graphql');
define('API_KEY', 'YOUR_API_KEY_TOKEN_HERE');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $firstName = $_POST['firstName'];
    $lastName = $_POST['lastName'];
    $email = $_POST['email'];
    $phone = $_POST['phone'];

    // Create person
    $personMutation = '
        mutation CreatePerson($data: PersonCreateInput!) {
            createPerson(data: $data) {
                id
                name {
                    firstName
                    lastName
                }
                email
            }
        }
    ';

    $personData = [
        'query' => $personMutation,
        'variables' => [
            'data' => [
                'name' => [
                    'firstName' => $firstName,
                    'lastName' => $lastName
                ],
                'email' => $email,
                'phone' => $phone
            ]
        ]
    ];

    $ch = curl_init(CRM_API_URL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($personData));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . API_KEY,
        'Content-Type: application/json'
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode === 200) {
        $result = json_decode($response, true);
        $personId = $result['data']['createPerson']['id'];
        
        // Create opportunity
        $opportunityMutation = '
            mutation CreateOpportunity($data: OpportunityCreateInput!) {
                createOpportunity(data: $data) {
                    id
                    name
                }
            }
        ';

        $opportunityData = [
            'query' => $opportunityMutation,
            'variables' => [
                'data' => [
                    'name' => "Website Lead - $firstName $lastName",
                    'stage' => 'NEW',
                    'pointOfContactId' => $personId
                ]
            ]
        ];

        $ch = curl_init(CRM_API_URL);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($opportunityData));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . API_KEY,
            'Content-Type: application/json'
        ]);

        curl_exec($ch);
        curl_close($ch);

        echo json_encode(['success' => true, 'message' => 'Lead created in CRM']);
    } else {
        echo json_encode(['success' => false, 'error' => 'Failed to create lead']);
    }
}
?>
```

### Python / Flask Example

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CRM_API_URL = 'http://localhost:3000/graphql'
API_KEY = 'YOUR_API_KEY_TOKEN_HERE'

@app.route('/api/contact-form', methods=['POST'])
def handle_contact_form():
    data = request.json
    
    # Create person
    person_mutation = """
        mutation CreatePerson($data: PersonCreateInput!) {
            createPerson(data: $data) {
                id
                name {
                    firstName
                    lastName
                }
                email
            }
        }
    """
    
    person_variables = {
        'data': {
            'name': {
                'firstName': data['firstName'],
                'lastName': data['lastName']
            },
            'email': data['email'],
            'phone': data.get('phone', '')
        }
    }
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    person_response = requests.post(
        CRM_API_URL,
        json={'query': person_mutation, 'variables': person_variables},
        headers=headers
    )
    
    person_id = person_response.json()['data']['createPerson']['id']
    
    # Create opportunity
    opportunity_mutation = """
        mutation CreateOpportunity($data: OpportunityCreateInput!) {
            createOpportunity(data: $data) {
                id
                name
            }
        }
    """
    
    opportunity_variables = {
        'data': {
            'name': f"Website Lead - {data['firstName']} {data['lastName']}",
            'stage': 'NEW',
            'pointOfContactId': person_id
        }
    }
    
    requests.post(
        CRM_API_URL,
        json={'query': opportunity_mutation, 'variables': opportunity_variables},
        headers=headers
    )
    
    return jsonify({'success': True, 'message': 'Lead created in CRM'})

if __name__ == '__main__':
    app.run(port=3002)
```

## Step 4: HTML Form Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>Contact Form</title>
</head>
<body>
    <h1>Contact Us</h1>
    <form id="contactForm">
        <label>First Name:</label>
        <input type="text" name="firstName" required><br><br>
        
        <label>Last Name:</label>
        <input type="text" name="lastName" required><br><br>
        
        <label>Email:</label>
        <input type="email" name="email" required><br><br>
        
        <label>Phone:</label>
        <input type="tel" name="phone"><br><br>
        
        <label>Company:</label>
        <input type="text" name="company"><br><br>
        
        <label>Message:</label>
        <textarea name="message" rows="4"></textarea><br><br>
        
        <button type="submit">Submit</button>
    </form>

    <script>
        document.getElementById('contactForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            const response = await fetch('/api/contact-form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert('Thank you! Your information has been submitted.');
                e.target.reset();
            } else {
                alert('There was an error. Please try again.');
            }
        });
    </script>
</body>
</html>
```

## Step 5: Testing Your Integration

### Using cURL (Command Line)

```bash
curl -X POST http://localhost:3000/graphql \
  -H "Authorization: Bearer YOUR_API_KEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CreatePerson($data: PersonCreateInput!) { createPerson(data: $data) { id name { firstName lastName } email } }",
    "variables": {
      "data": {
        "name": {
          "firstName": "Test",
          "lastName": "User"
        },
        "email": "test@example.com",
        "phone": "+1234567890"
      }
    }
  }'
```

### Using Postman

1. Create a new POST request to `http://localhost:3000/graphql`
2. Add header: `Authorization: Bearer YOUR_API_KEY_TOKEN`
3. Set body type to "GraphQL"
4. Paste the mutation query and variables

## Step 6: Workflow Automation (Advanced)

You can also set up **webhooks** in OSP CRM to trigger actions when new leads are created:

1. Go to **Settings → API & Webhooks → Webhooks**
2. Create a new webhook
3. Select trigger event (e.g., "Person Created")
4. Enter your webhook URL
5. OSP CRM will send POST requests to your URL when events occur

## Security Best Practices

1. **Never expose your API key** in client-side JavaScript
2. **Always use HTTPS** in production
3. **Implement rate limiting** on your backend
4. **Validate and sanitize** all form inputs
5. **Use environment variables** for sensitive data
6. **Set appropriate API key permissions** (least privilege principle)
7. **Rotate API keys** periodically

## Production Deployment

When deploying to production:

1. Change API URL from `http://localhost:3000/graphql` to your production domain
2. Use HTTPS: `https://your-crm-domain.com/graphql`
3. Store API keys in environment variables
4. Set up proper CORS configuration on the CRM server
5. Monitor API usage and errors

## Common Issues & Solutions

### Issue: "Unauthorized" Error
- **Solution**: Check that your API key is correct and included in the Authorization header

### Issue: "Invalid field" Error
- **Solution**: Verify field names match the GraphQL schema. Use GraphQL Playground to explore available fields.

### Issue: CORS Error
- **Solution**: Configure CORS settings in your OSP CRM backend to allow requests from your website domain

### Issue: "Person already exists"
- **Solution**: Check for existing records before creating new ones, or update existing records instead

## GraphQL Playground

To explore the available queries and mutations:

1. Visit http://localhost:3000/graphql in your browser
2. Add your API key to the HTTP headers:
   ```json
   {
     "Authorization": "Bearer YOUR_API_KEY_TOKEN"
   }
   ```
3. Use the documentation explorer on the right side to discover available operations

## Need Help?

- Check the GraphQL schema documentation in the playground
- Review the Twenty CRM documentation
- Test queries in the GraphQL Playground before implementing in your code

---

**Note**: Replace `YOUR_API_KEY_TOKEN_HERE` with your actual API key from Step 1.
