# CORS Test Lab

Interactive demonstration of Cross-Origin Resource Sharing (CORS) concepts, based on the Hacker News discussion about developers misunderstanding CORS.

**HN Thread:** https://news.ycombinator.com/item?id=48614844  
**Article:** https://fosterelli.co/developers-dont-understand-cors  
**MDN Docs:** https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS

## Quick Start

```bash
# Terminal 1 - Start API server (port 8001)
cd server
python3 api_server.py

# Terminal 2 - Start client server (port 8000)
cd client
python3 server.py

# Open browser
open http://localhost:8000
```

## What This Demonstrates

This test lab shows exactly what CORS does and does NOT do, addressing the core confusion from the HN thread:

### ❌ Common Misconception
> "CORS prevents cross-origin requests"

### ✅ Reality
> "CORS controls whether JavaScript can READ responses to cross-origin requests. The requests are sent regardless!"

## HN Discussion Highlights

### The Core Debate

**Comment that sparked debate:**
> "Access-Control-Allow-Origin header will ensure that only Javascript running on the zoom.us domain can talk to the localhost webserver."

**Top reply (correct):**
> "No, that does not do that. JavaScript from any other website can still talk to localhost:19421 just the same. CORS doesn't restrict anything... That header just allows JavaScript running on zoom.us to read the responses... The requests happen in any case!"

### Key Insights from HN Thread:

1. **CORS is not a security boundary**
   - Requests are ALWAYS sent (for simple requests)
   - Server must validate requests independently
   - CORS only controls browser's response access

2. **Simple vs Preflighted Requests**
   - Simple: GET, HEAD, POST with form-encoded data
   - Preflighted: Everything else (JSON, custom headers, PUT, DELETE, etc.)
   - Preflight uses OPTIONS request first

3. **Safe vs Idempotent (HTTP semantics)**
   - **Safe**: No state change (GET, HEAD, OPTIONS)
   - **Idempotent**: Same result if repeated (GET, PUT, DELETE)
   - **Neither**: POST, PATCH
   - Safety matters for CORS, not just idempotency

4. **"CORS is confusing because..."**
   - Poor documentation
   - Copy-paste from Stack Overflow
   - `Access-Control-Allow-Origin: *` as a "fix-all"
   - Lack of understanding of same-origin policy history

## Test Scenarios

### 1. Simple GET Request
- **What happens:** Browser sends GET, server responds with CORS headers
- **Result:** ✅ JavaScript can read response
- **Key point:** No preflight needed

### 2. GET with CORS Blocked
- **What happens:** Browser sends GET, server responds WITHOUT CORS headers
- **Result:** ❌ Browser blocks JavaScript from reading response
- **Key point:** ⚠️ **Server still processed the request!** Check server logs!

### 3. Simple POST (form-encoded)
- **What happens:** POST with `Content-Type: application/x-www-form-urlencoded`
- **Result:** ✅ No preflight, request sent immediately
- **Key point:** Form-encoded POST is "simple" for historical reasons (HTML forms)

### 4. Preflighted POST (JSON)
- **What happens:** 
  1. Browser sends OPTIONS preflight
  2. Server responds with allowed methods/headers
  3. Browser sends actual POST
- **Result:** ✅ Works if server approves preflight
- **Key point:** Two requests sent, not one

### 5. Custom Headers
- **What happens:** Any custom header triggers preflight
- **Result:** OPTIONS request checks if header is allowed
- **Key point:** `X-Custom-Header` requires explicit allowlist

### 6. Credentials + Wildcard
- **What happens:** Request with `credentials: 'include'` to server with `Access-Control-Allow-Origin: *`
- **Result:** ❌ Browser blocks (security violation)
- **Key point:** Wildcard and credentials are mutually exclusive

### 7. Localhost API Risk (Zoom Vulnerability)
- **What happens:** Any website can make requests to `http://localhost:xxxx`
- **Result:** ⚠️ Requests succeed, CORS may or may not block reading response
- **Key point:** Localhost APIs are accessible from any origin! Must implement proper auth, not just CORS.

### 8. Image/Script Bypass
- **What happens:** `<img src="http://api.example.com/data">`
- **Result:** Request sent, image loads (or fails), but JS cannot read pixel data
- **Key point:** Certain tags bypass CORS but with restricted access

## Security Takeaways

### What CORS Protects Against:
✅ Malicious site reading sensitive data from your bank API  
✅ CSRF attacks that need to read responses  
✅ Data exfiltration via JavaScript

### What CORS Does NOT Protect Against:
❌ CSRF attacks (requests are still sent!)  
❌ Server-side request forgery  
❌ Direct API access (curl, Postman, etc.)  
❌ Simple form submissions  
❌ Image/script tag requests

### Proper Security Requires:
1. **CORS headers** - Control browser access
2. **CSRF tokens** - Validate request origin server-side
3. **Authentication** - Verify user identity
4. **Authorization** - Check permissions
5. **Input validation** - Sanitize all data
6. **SameSite cookies** - Prevent CSRF

## The Zoom Vulnerability Explained

**What happened:**
1. Zoom ran local web server on `http://localhost:19421`
2. Used `<img>` tags to bypass CORS (images don't enforce CORS)
3. Encoded data in image dimensions (width/height)
4. Any website could trigger Zoom actions

**Why CORS headers wouldn't have fully fixed it:**
- Image requests bypass CORS
- Even with proper CORS, requests would still be sent
- Needed: Authentication, CSRF tokens, user confirmation

**Proper fix:**
1. Require authentication token
2. Validate Origin header server-side
3. Implement CSRF protection
4. Use postMessage API instead of localhost server
5. Require user interaction

## Common CORS Misconfigurations

### ❌ Dangerous: Wildcard with credentials
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```
**Browser will block this** - but developers often "fix" by removing credentials check, creating vulnerability.

### ❌ Dangerous: Reflecting Origin header
```http
Access-Control-Allow-Origin: [value of Origin header]
Access-Control-Allow-Credentials: true
```
**Allows any site to make credentialed requests** - essentially disables protection.

### ❌ Dangerous: Overly permissive
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```
**Allows any site to read your API responses** - only safe for truly public data.

### ✅ Correct: Specific origin with credentials
```http
Access-Control-Allow-Origin: https://trusted-app.example.com
Access-Control-Allow-Credentials: true
Vary: Origin
```

## Testing Your Understanding

After running the test lab, you should understand:

1. **Q: Does CORS prevent my API from being called by other sites?**
   A: No. Requests are sent. CORS only controls if the browser lets JavaScript read responses.

2. **Q: If I don't set CORS headers, am I safe from CSRF?**
   A: No. Simple requests (GET, form POST) are sent anyway. Use CSRF tokens.

3. **Q: Why does my POST with JSON trigger OPTIONS?**
   A: JSON content-type is not "simple". Browser must preflight to check if server allows it.

4. **Q: Can I use `*` with `withCredentials`?**
   A: No. Browser blocks this combination. Must specify exact origin.

5. **Q: Is localhost safe from CORS?**
   A: No. Any website can make requests to localhost. Implement proper security.

## Further Reading

- **MDN CORS Guide**: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
- **CORS Errors**: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS/Errors
- **Fetch Spec**: https://fetch.spec.whatwg.org/#http-cors-protocol
- **OWASP CORS**: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Origin_Resource_Sharing_Cheat_Sheet.html
- **PortSwigger**: https://portswigger.net/web-security/cors

## Running the Tests

1. Start both servers
2. Open http://localhost:8000
3. Open browser DevTools (F12) → Network tab
4. Click test buttons and observe:
   - Which requests trigger preflight OPTIONS
   - Request/response headers
   - Which requests succeed vs fail
   - Server console output (shows ALL requests are received)

## Key Files

- `server/api_server.py` - Test API with various CORS configurations
- `client/index.html` - Interactive test UI
- `client/server.py` - Static file server

## License

MIT - Educational purposes. Use to understand CORS, not as production code!
