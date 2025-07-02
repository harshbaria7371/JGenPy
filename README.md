# JGenPy : Precision Test Data, Effortlessly Generated.

## 🎯 Project Overview
JGenPy is Python tool generates realistic, structured test data based on a user-provided JSON schema. It uses a powerful directive system embedded directly within the schema to give you fine-grained control over the generated data values, from random UUIDs and names to complex nested objects and arrays.

---

## ✨ Features

-   **Schema-Driven Generation**: Creates data that strictly conforms to the structure of your input JSON schema.
-   **Powerful Directive System**: Specify data types and generation patterns directly within the schema (e.g., `"email": "string:email"`).
-   **Realistic Data**: Leverages the `Faker` library to produce believable emails, names, phone numbers, UUIDs, lorem ipsum text (words, sentences, paragraphs), street addresses, cities, countries, random strings, strings matching regex patterns, random integers within a range, random floats within a range, random booleans, and various date types (past, future, current).
-   **Complex Data Structures**: Natively supports nested JSON objects and arrays of both primitive values and complex objects.
-   **Extensible**: Easily add new custom generators for your specific needs.
-   **Command-Line Interface**: Simple and intuitive CLI for generating data and saving it to a file or printing it to the console.
-   **Robust Error Handling**: Provides clear error messages for invalid schemas, malformed directives, and file issues.


## 🚀 Getting Started
Follow these simple steps to get AVIATEGEN up and running on your system.

### Prerequisites
1. Python 3.9+
2. pip (Python package installer)
3. Libraries in requirements.txt

### Setting up local development environment
1. Install suitable python version (mentioned above)
2. Clone repository
3. Install libraries mentioned in requirements.txt

---

## 🧑‍💻 Usage
**1. Define Your JSON Schema with Directives**

Create a JSON file (e.g., employee_data_schema.json in an examples directory) that defines the structure of your desired data.

Example `examples/employee_data_schema.json`
> {
  "userId": "string:uuid",
  "firstname": "string:firstname",
  "lastname": "string:lastname",
  "country": "string:country",
  "phoneNumber": "string:phone"
}

**2. Generate Data**

**Command Line**

Here the main script name is `run_data_generator.py` :

> python .\run_data_generator.py <SCHEMA_JSON_FILE> <NUMBER_OF_RECORDS> --output <OUTPUT_FILE_PATH_WITH_NAME>

**Explanation of Parameters:**
1. `<SCHEMA_JSON_FILE>`: This is the path to your JSON schema file. (e.g. `.\examples\user_profile_schema.json`)
2. `<NUMBER_OF_RECORDS>`: This is the number of records (JSON Objects) you want to generate.
3. `--output <OUTPUT_FILE_PATH_WITH_NAME>`: This specifies the output file path, including the desired filename for the generated JSON data. (e.g., `.\seed\userdata.json`)

**Example**
To generate 1 record based on `employee_data_schema.json` and save it to `userdata.json` in the `seed` directory:

> python .\run_data_generator.py .\examples\user_profile_schema.json 1 --output .\seed\userdata.json

---

## 📜 License 
JGenPy is distributed under the ISC License.

Made with ❤️ by Harsh Baria / harshbaria7371