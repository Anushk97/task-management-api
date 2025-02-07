Subject: Database Choice for Task Management API: SQLAlchemy vs MongoDB

Hi Lukas,

I want to ask if I can use SQLAlchemy with SQLite instead of MongoDB for this task management API project.

SQLAlchemy is the better choice for this specific use case because:

1. SQL Alchemy has a quick setup & development vs MongoDB because it's a simple to use ORM for Python

2. This task have a fixed structure (id, title, description, status), so we can use SQLAlchemy's schema validation without the need for MongoDB's flexibility with data structure.

3. SQLite DB has built-in data consistency (ACID compliance). It is also perfect for task updates and status changes.

However, we should consider MongoDB if:
- We need to scale to multiple servers
- Tasks need to store varying types of data
- We expect a massive amount of concurrent users
- We need built-in sharding

For now, SQLAlchemy will do the job without the overhead of running a separate database server. I can always migrate to MongoDB if that is strictly required.

Let me know if this approach is fine for this project.

Best regards,
Anushk 

P.S. The app is already running smoothly with SQLAlchemy, and the setup process is as simple as running two commands!
