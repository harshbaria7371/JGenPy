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

## 🚀 Getting Started
Follow these simple steps to get JGenPy up and running on your system.

### Prerequisites
1. Python 3.9+
2. pip (Python package installer)
3. Libraries in requirements.txt

### Setting up local development environment
1. Install suitable python version (mentioned above)
2. Clone repository
3. Install libraries mentioned in requirements.txt

## 🧑‍💻 Usage

Basic Data Generation
``` python .\run_data_generator.py .\examples\user_profile_schema.json 1 --output .\seed\userdata.json ```

Here, Command required 3 parameters: Schema json file path, count of records, output file path
This command will generate structured data based on JSON schema. 

## 📜 License
JGenPy is distributed under the ISC License. 

Made with ❤️ by Harsh Baria / harshbaria7371
