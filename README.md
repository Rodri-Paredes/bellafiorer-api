# BellaFiore API

This project is the backend API for BellaFiore, a platform dedicated to managing flower orders. BellaFiore enables users to track the status of their flower orders, view orders for a specific day, check if orders have been paid, and see the total amount for each order.

## Requirements

- MySQL 8.0 or earlier

## Database

We utilize Flyway as our migration tool to manage the database schema and version control. Flyway helps us to apply database migrations effortlessly, ensuring that our database stays consistent and up-to-date across different environments.

To apply all migrations, run the following command:

flyway migrate -url="jdbc:mysql://localhost:3306/bellafiore" -user="root" -password="****"

Replace **** with your MySQL database password. This command will execute all pending migrations against the specified database URL.