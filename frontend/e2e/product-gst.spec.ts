import { test, expect } from '@playwright/test'

test('product gst flow', async ({ page }) => {
  // Assumes frontend dev server is running on http://localhost:3000
  await page.goto('http://localhost:3000/product-gst')
  await page.fill('input', 'Laptop')
  await page.click('text=Fetch')
  // Wait for result area to show GST Rate
  await expect(page.locator('text=GST Rate')).toBeVisible({ timeout: 5000 })
  const rate = await page.locator('text=GST Rate').textContent()
  expect(rate).toContain('18')
})
