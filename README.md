# meli-test API Documentation

## Overview

The `meli-test` API provides endpoints to analyze DNA sequences and compute mutant statistics. The API consists of the following endpoints:

1. **`POST /mutant`** - Accepts a DNA sequence and determines whether it is from a mutant or a human.
2. **`GET /stats`** - Provides statistics on the number of human and mutant DNA sequences, along with the mutant ratio.

## Endpoints

### `POST /mutant`
**Description**: This endpoint accepts a DNA sequence and analyzes whether it belongs to a mutant or a human based on the sequence provided.

- **Request Body**:
  - The request must contain a JSON object with a key `dna` whose value is a list of strings representing the DNA sequence.
  - The DNA sequence will be automatically converted to uppercase for processing.

- **Request Format**:
  ```json
  {
    "dna": ["ATGC", "GGAT", "CGAT", "AAAA"]
  }

- Response:
- - If the DNA sequence belongs to a mutant, the API will return a 200 OK status.
- - If the DNA sequence does not belong to a mutant (i.e., it's human), the API will return a 403 Forbidden status.

### `GET /stats`
**Description**: This endpoint provides statistics on the number of human and mutant DNA sequences, along with the mutant ratio.

- **response Format**:
  ```json
  {
  "count_human_dna": 3,
  "count_mutant_dna": 2,
  "ratio": 0.4
    }

## the endpoint was provided in the google forms that was sent