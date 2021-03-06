Versions
---------

## Current

### 0.4
- Better code documentation
- Index for model fields
- Index queries
- ORM additional fields:
    - Choice
    - Text
    - ManyToMany

## Old

### 0.1
First version which had the following features:

- Some simple queries:
    - Get by example data
    - Random document
    - All documents
- Started with advanced queries
- Started with basic ORM:
    - Models
    - Fields for models (char, number, foreign key)
    - Model query manager
- Transactions to create and update documents
- Managing databases, collections and documents

### 0.2

- More test coverage
- Advanced queries can now be run for multiple collections
- Simple queries added:
    - Remove by example data
    - Update by example data
    - Replace by example data
- ORM:
    - Adding date and datetime fields
    - Queryset for model manager
    
### 0.3
- Index support
- User support
- Execute raw ArangoDB queries
- ORM Queryset Filtering (with boolean)
- ORM Queryset limit
- ORM additional fields:
    - UUID
    - Boolean

## Future

### 0.5
- Bitarray index
- Batch execution
- Replication
- Endpoint
- Better traversal query
- ORM index queries
- ORM additional fields:
    - File
    - NumberRange
    - URL
    - MailAddress
    - Password

### 0.6
- Authentication
- System
- HTTP exception handling
- Document revision

### 0.7
- Graph