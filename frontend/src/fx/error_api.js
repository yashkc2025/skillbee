#!/usr/bin/env node

const http = require('http')
const url = require('url')

// Configuration
const PORT = process.argv[2] || 8080
const ERROR_RESPONSE = {
  error: 'Internal Server Error',
  status: 500,
}

// Create server
const server = http.createServer((req, res) => {
  const method = req.method
  const path = req.url

  // Set CORS headers first for all requests
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:5173/')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
  res.setHeader(
    'Access-Control-Allow-Headers',
    'Content-Type, Authorization, sec-ch-ua-platform, Referer, User-Agent, sec-ch-ua, DNT, sec-ch-ua-mobile, X-Requested-With',
  )
  res.setHeader('Access-Control-Max-Age', '86400') // 24 hours

  // Handle preflight OPTIONS requests
  if (method === 'OPTIONS') {
    console.log(
      `${new Date().toISOString()}: OPTIONS ${path} - Preflight request, returning 500 error`,
    )
    res.writeHead(500, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify(ERROR_RESPONSE))
    return
  }

  // Log the request
  console.log(`${new Date().toISOString()}: ${method} ${path} - Returning 500 error`)

  // Read request body (for POST/PUT/PATCH) but don't process it
  let body = ''
  req.on('data', (chunk) => {
    body += chunk.toString()
  })

  req.on('end', () => {
    // Log request body if present
    if (body) {
      console.log(`Request body: ${body}`)
    }

    // Always return 500 error regardless of method or content
    res.writeHead(500, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify(ERROR_RESPONSE))
  })
})

// Start server
server.listen(PORT, () => {
  console.log(`Error API server running on port ${PORT}`)
  console.log(`All requests will return 500 errors`)
  console.log(`Press Ctrl+C to stop`)
})

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down server...')
  server.close(() => {
    console.log('Server closed')
    process.exit(0)
  })
})

process.on('SIGTERM', () => {
  console.log('\nShutting down server...')
  server.close(() => {
    console.log('Server closed')
    process.exit(0)
  })
})
