# Development environment

This project requires Python 3.10+ and several runtimes for testing generated code.

## Python Setup

Install Python 3.10 or later. The prerequisites are listed in `requirements.txt`:

```shell
pip install -r requirements.txt
```

## Required Runtimes/SDKs

Install the following runtimes separately:

| Runtime | Version | Purpose |
|---------|---------|---------|
| [.NET SDK](https://dotnet.microsoft.com/en-us/download) | 6.0+ | C# code generation |
| [OpenJDK](https://learn.microsoft.com/en-us/java/openjdk/download) | 21+ | Java code generation |
| [Node.js](https://nodejs.org/en/download/) | 14+ | TypeScript code generation |
| [Go](https://go.dev/dl/) | 1.21+ | Go code generation |
| [Docker](https://www.docker.com/get-started) | Latest | Test containers (brokers) |

## Validation Tools

For running tests that validate generated output, install these CLI tools:

```shell
npm install -g azure-functions-core-tools@4 --unsafe-perm true
npm install -g @asyncapi/cli
npm install -g @openapitools/openapi-generator-cli
```

## Running the Tests

Tests use PyTest with Docker-based testcontainers for message brokers (Kafka, MQTT, AMQP).

```shell
# Run all tests (30+ minutes)
pytest

# Run targeted tests (recommended)
pytest test/py/test_python.py::test_kafkaproducer_contoso_erp_py

# Always redirect output to preserve error details
pytest test/cs/test_csharp.py > tmp/test_output.txt 2>&1
```

**Important:** Full test runs take 30+ minutes. Target specific tests when validating changes.

## C# Code Generation Dependencies

The generated C# code depends on an experimental extension to the C# CloudEvents SDK that is not yet available from NuGet.

**Setup steps:**

1. Create a local directory for extension packages and set the environment variable `CEDISCO_NUGET_LOCAL_FEED` to point to it.

2. Clone the repository: [CloudNative.CloudEvents.Endpoints](https://github.com/clemensv/CloudNative.CloudEvents.Endpoints/)

3. Build the project in the `source` directory with `dotnet build` and copy the resulting packages from `source/packages` to your local feed directory.

## Java Code Generation Dependencies

The generated Java code depends on an experimental extension to the Java CloudEvents SDK that is not yet available from Maven Central.

**Setup steps:**

1. Clone the repository: [io.cloudevents.experimental.endpoints](https://github.com/clemensv/io.cloudevents.experimental.endpoints)

2. Build with `mvn install` to install packages into your local Maven repository.

## TypeScript Code Generation Dependencies

TypeScript templates require Node.js 14+ (already listed in Required Runtimes above). No additional dependencies are needed beyond the npm packages installed during project generation.
