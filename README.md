# JGenPy : Precision Test Data, Effortlessly Generated.

## 🎯 Project Overview
JGenPy is a Python tool that generates realistic, structured test data based on a user-provided JSON schema. It uses a powerful directive system embedded directly within the schema to give you fine-grained control over the generated data values, from random UUIDs and names to complex nested objects and arrays.

---

## ✨ Features

-   **Schema-Driven Generation**: Creates data that strictly conforms to the structure of your input JSON schema.
-   **Powerful Directive System**: Specify data types and generation patterns directly within the schema (e.g., `"email": "string:email"`).
-   **Realistic Data**: Leverages the `Faker` library to produce believable emails, names, phone numbers, UUIDs, lorem ipsum text (words, sentences, paragraphs), street addresses, cities, countries, provinces, postal codes, VAT numbers, random strings, strings matching regex patterns, random integers within a range, random floats within a range, random booleans, and various date types (past, future, current, birth dates).
-   **Locale-Aware Generation**: Configure country/locale via `.config` file to generate data specific to that region (e.g., Indian names, addresses, phone numbers when Country=India).
-   **Complex Data Structures**: Natively supports nested JSON objects and arrays of both primitive values and complex objects.
-   **Extensible**: Easily add new custom generators for your specific needs.
-   **Command-Line Interface**: Simple and intuitive CLI for generating data and saving it to a file or printing it to the console.
-   **Robust Error Handling**: Provides clear error messages for invalid schemas, malformed directives, and file issues.

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
```bash
pip install -r requirements.txt
```

### Configuration
JGenPy supports locale-specific data generation through a `.config` file in the project root. Create a `.config` file with:
```
Country=India
```
Available countries include: India, United States, United Kingdom, Canada, Australia, Germany, France, Spain, Italy, Japan, China, Brazil, and many more. The generated data (names, addresses, phone numbers, etc.) will match the configured country's locale.


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
To generate 1 record based on `user_profile_schema.json` and save it to `userdata.json` in the `seed` directory:

> python .\run_data_generator.py .\examples\user_profile_schema.json 1 --output .\seed\userdata.json

---

## 📖 Examples

### Example 1: Simple Employee Data
```json
{
  "userId": "string:uuid",
  "firstname": "string:firstname",
  "lastname": "string:lastname",
  "country": "string:country",
  "phoneNumber": "string:phone"
}
```

### Example 2: Product with Nested Objects and Arrays
```json
{
  "productId": "string:uuid",
  "productName": "string:lorem(type=text,max_nb_chars=50)",
  "category": "string:word",
  "quantity": "integer:range(min=1,max=10)",
  "unitPrice": "float:random(min=5.00,max=200.00,dp=2)",
  "purchaseDate": "date:past(years=1,format=%Y-%m-%d)",
  "supplierInfo": {
    "supplierName": "string:name",
    "supplierId": "string:random(length=8)"
  },
  "ratings": "array:integer:range(min=1,max=5),count=3"
}
```

### Example 3: Complex User Profile with Arrays
```json
{
  "userId": "string:uuid",
  "username": "string:email",
  "fullName": "string:name",
  "age": "integer:range(min=18,max=75)",
  "isActive": "boolean:random",
  "lastLogin": "date:past(years=1,format=%Y-%m-%d %H:%M:%S)",
  "vatNumber": "string:vat_number(length=25)",
  "profile": {
    "bio": "string:lorem(type=sentence)",
    "websiteUrl": "string:email",
    "address": {
      "street": "string:street_address",
      "city": "string:city",
      "zipCode": "string:regex(pattern=\\d{5}(-\\d{4})?)"
    }
  },
  "tags": "array:string:word,count=5",
  "orderHistory": "array:object,count=2,schema_file=product_item_schema.json"
}
```

---

## ☕ Support

If you find this project helpful, you can support my work by buying me a coffee:

<p><a href="https://www.buymeacoffee.com/bariaharshg">
<img align="left" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="Buy Me A Coffee" />
</a></p><br><br>

## 📜 License 
JGenPy is distributed under the ISC License.

Made with ❤️ by Harsh Baria / harshbaria7371