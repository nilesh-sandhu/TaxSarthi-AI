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
      const base = process.env.NEXT_PUBLIC_API_BASE_URL || '/api'
      const res = await fetch(`${base}/gst/product`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_name: product, amount: 1000 })
      })

      if (!res.ok) {
        const text = await res.text()
        throw new Error(`${res.status} ${text}`)
      }

      const data = await res.json()
      setResult(data)
    } catch (e:any) {
      setResult({ error: String(e) })
    } finally {
      setLoading(false)
    }
  }

  function renderResult() {
    if (!result) return null
    if (result.error) return <div style={{color:'red'}}>{result.error}</div>
    if (result.classification_required) {
      return (
        <div>
          <strong>Multiple classifications found — please refine:</strong>
          <ul>
            {result.hsn_options?.slice(0,10).map((o:any, i:number)=> (
              <li key={i}>{o.hsn} — {o.description?.slice(0,80)} — {o.gst_rate}%</li>
            ))}
          </ul>
        </div>
      )
    }

    return (
      <div>
        <div><strong>Product</strong>: {result.product}</div>
        <div><strong>HSN</strong>: {result.hsn}</div>
        <div><strong>GST Rate</strong>: {result.gst_rate}%</div>
        <div><strong>GST Amount</strong>: {result.gst_amount}</div>
        <div style={{marginTop:8}}><small>Source: {result.source}</small></div>
      </div>
    )
  }

  return (
    <div style={{padding:12,maxWidth:700}}>
      <h3>Product GST Lookup</h3>
      <div style={{display:'flex',gap:8,alignItems:'center'}}>
        <input value={product} onChange={e=>setProduct(e.target.value)} style={{flex:1,padding:8,fontSize:16}} />
        <button onClick={fetchGst} disabled={loading} style={{padding:'8px 12px'}}>{loading? 'Loading...':'Fetch'}</button>
      </div>
      <div style={{marginTop:12,background:'#f8f9fb',padding:12,borderRadius:6}}>
        {renderResult()}
      </div>
    </div>
  )
}
