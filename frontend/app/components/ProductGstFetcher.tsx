"use client"
import React, { useState } from 'react'

export default function ProductGstFetcher() {
  const [product, setProduct] = useState('Laptop')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  async function fetchGst() {
    setLoading(true)
    setResult(null)
    try {
      const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'
      const res = await fetch(`${base}/gst/product`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_name: product, amount: 1000 })
      })
      const data = await res.json()
      setResult(data)
    } catch (e) {
      setResult({ error: String(e) })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{padding:12}}>
      <h3>Product GST Lookup</h3>
      <input value={product} onChange={e=>setProduct(e.target.value)} />
      <button onClick={fetchGst} disabled={loading} style={{marginLeft:8}}>{loading? 'Loading...':'Fetch'}</button>
      <pre style={{marginTop:12}}>{JSON.stringify(result, null, 2)}</pre>
    </div>
  )
}
