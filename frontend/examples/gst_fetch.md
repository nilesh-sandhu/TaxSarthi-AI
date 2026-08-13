Frontend example: fetch GST for a product

Use this snippet from your frontend (e.g., React) to call the new backend endpoint and display results.

```javascript
async function fetchProductGst(productName, amount = 1000, interstate = false) {
  const res = await fetch('/api/gst/product', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_name: productName, amount, interstate })
  })

  if (!res.ok) throw new Error('Request failed: ' + res.status)
  const data = await res.json()
  return data
}

// Example usage
fetchProductGst('Laptop', 1000)
  .then(r => console.log(r))
  .catch(e => console.error(e))
```

Notes:
- In development, ensure your frontend dev server proxies `/api` to `http://127.0.0.1:8000` or call the backend URL directly.
- CORS for `http://localhost:3000` is already allowed in the backend.
