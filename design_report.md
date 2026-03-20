Conceptual & Logical Design Report: FinTech Transaction Engine

1. Objective and Core Entities
The objective of this phase is to model a raw FinTech dataset into a rigorous, normalized PostgreSQL database. Upon analyzing the flat CSV transaction data, four core entities were identified to represent the financial ledger accurately:

Customers: Individuals holding accounts.

Accounts: Financial vehicles (Checking, Savings, Credit) owned by customers.

Merchants: The businesses receiving funds.

Transactions: The ledger entries recording the movement of funds between an account and a merchant.

2. Normalization Process (Reaching 3NF)
To ensure data integrity, the schema was designed to satisfy Third Normal Form (3NF) through the following progression:

First Normal Form (1NF): All attributes are atomic. For example, customer names are divided into first_name and last_name, ensuring no multi-valued attributes exist. Every table features a unique, non-null Primary Key (e.g., transaction_id, customer_id).

Second Normal Form (2NF): The schema contains no partial dependencies. Because we utilize single-column surrogate primary keys (like merchant_id rather than a composite key of merchant_name and category), all non-key attributes depend entirely on the primary key of their respective tables.

Third Normal Form (3NF): All transitive dependencies have been eliminated. In the raw dataset, a merchant's category depends on the merchant's name, which in turn depends on the transaction. We resolved this by extracting merchant_name and category into an independent Merchants table. Now, the Transactions table only references merchant_id, ensuring non-key attributes do not depend on other non-key attributes.

3. Resolving Many-to-Many Relationships
In a financial ecosystem, a single Account can make purchases at many Merchants, and a single Merchant can process payments from many Accounts.

Leaving this as a direct many-to-many (M:N) relationship would violate relational database principles. We resolved this by utilizing the Transactions table as a bridge (or junction) table. The Transactions entity holds two Foreign Keys (account_id and merchant_id), effectively breaking the M:N relationship into two easily manageable one-to-many (1:N) relationships.

4. Prevention of Data Anomalies
By achieving 3NF, this schema inherently protects the application from the three major data anomalies:

Insertion Anomaly: We can add a new Merchant to the system (perhaps when onboarding a new vendor) without requiring an active transaction to exist, because merchant data is stored independently of the ledger.

Update Anomaly: If a customer changes their email address, we only need to update a single row in the Customers table. In a flat, unnormalized schema, we would have to update thousands of historical transaction rows, risking data inconsistency.

Deletion Anomaly: If we delete a reversed or fraudulent transaction from the Transactions table, we do not accidentally delete the associated Customer or Merchant data from the database.