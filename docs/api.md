# API Documentation

Server Stats REST API for calculating statistical metrics on matrices with binary masks.

---

## Base URL

```
http://localhost:5000
```

---

## Endpoints

### POST /run

Calculate statistical metrics on a result with a binary mask.

#### Request

**Content-Type:** `application/json`

**Body:**
```json
{
  "result": [[float, ...], ...],
  "mask": [[int, ...], ...]
}
```

**Parameters:**
- `result` (required): 2D array of float values (0.0 - 10.0)
- `mask` (required): 2D array of binary values (0 or 1), same dimensions as result

**Validation Rules:**
- Result values must be floats between 0.0 and 10.0
- Mask values must be binary (0 or 1)
- Result and mask must have identical dimensions
- Mask must contain at least one value of 1

#### Response

**Success (200):**
```json
{
  "metrics": {
    "mean": float,
    "median": float,
    "mae": float,
    "threshold_accuracy": float,
    "quantized_iou": float,
    "compliance": float,
    "range_polygon": object
  }
}
```

**Metrics:**
- `mean`: Arithmetic mean of masked values
- `median`: Median of masked values
- `mae`: Mean Absolute Error
- `threshold_accuracy`: Accuracy at threshold values
- `quantized_iou`: Intersection over Union with quantization
- `compliance`: Compliance metric
- `range_polygon`: Range polygon analysis

**Error (400):**
```json
{
  "error": "error message"
}
```

**Error (500):**
```json
{
  "error": "Internal server error"
}
```

#### Examples

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:5000/run",
    json={
        "result": [[1.5, 2.3, 3.7], [4.2, 5.8, 6.1]],
        "mask": [[1, 1, 0], [1, 0, 1]]
    }
)

if response.status_code == 200:
    metrics = response.json()["metrics"]
    print(f"Mean: {metrics['mean']:.2f}")
else:
    print(f"Error: {response.json()['error']}")
```

**cURL:**
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d @assets/sample_request.json
```

---

### GET /health

Health check endpoint to verify server status.

#### Request

No parameters required.

#### Response

**Success (200):**
```json
{
  "status": "healthy"
}
```

#### Examples

**Python:**
```python
import requests

response = requests.get("http://localhost:5000/health")
print(response.json())
# {"status": "healthy"}
```

**cURL:**
```bash
curl http://localhost:5000/health
```

---

## Error Codes

| Status Code | Description |
|------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input data |
| 500 | Internal Server Error |

## Common Error Messages

| Error Message | Cause |
|--------------|-------|
| `Missing 'result' in request body` | Request missing required result field |
| `Missing 'mask' in request body` | Request missing required mask field |
| `Result and mask must have the same dimensions` | Dimension mismatch |
| `Result values must be floats between 0 and 10` | Invalid result values |
| `Mask values must be binary (0 or 1)` | Invalid mask values |
| `Mask must contain at least one value of 1` | No valid area in mask |

---

## Sample Files

- Request: [assets/sample_request.json](../assets/sample_request.json)
- Response: [assets/sample_response.json](../assets/sample_response.json)
