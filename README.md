# JGenPy

This Python tool generates realistic, structured test data based on a user-provided JSON schema. It uses a powerful directive system embedded directly within the schema to give you fine-grained control over the generated data values, from random UUIDs and names to complex nested objects and arrays.

---

## Features

-   **Schema-Driven Generation**: Creates data that strictly conforms to the structure of your input JSON schema.
-   **Powerful Directive System**: Specify data types and generation patterns directly within the schema (e.g., `"email": "string:email"`).
-   **Realistic Data**: Leverages the `Faker` library to produce believable names, addresses, emails, and more.
-   **Complex Data Structures**: Natively supports nested JSON objects and arrays of both primitive values and complex objects.
-   **Extensible**: Easily add new custom generators for your specific needs.
-   **Command-Line Interface**: Simple and intuitive CLI for generating data and saving it to a file or printing it to the console.
-   **Robust Error Handling**: Provides clear error messages for invalid schemas, malformed directives, and file issues.

---