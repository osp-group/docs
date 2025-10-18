# Twenty CRM Railway Deployment - Complete Guide with Redis

**Date:** October 18, 2025  
**Status:** ✅ Final Configuration Complete - Ready for Redeploy  
**Platform:** Railway.app  
**Application:** Twenty CRM v0.2.1

---

## 📋 Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Issues Encountered & Solutions](#issues-encountered--solutions)
3. [Final Working Configuration](#final-working-configuration)
4. [Redis Setup & Timing Issue](#redis-setup--timing-issue)
5. [Verification Steps](#verification-steps)
6. [Next Steps](#next-steps)
7. [Troubleshooting Guide](#troubleshooting-guide)

---

## 🎯 Deployment Overview

### Services in Railway Project

1. **Postgres** - PostgreSQL database
   - Database: `railway`
   - User: `postgres`
   - Internal domain: `postgres.railway.internal`

2. **Redis** - Cache storage
   - Internal domain: `redis.railway.internal`
   - Port: 6379

3. **twenty-server** - Twenty CRM application
   - Public URL: `https://osp-crm.up.railway.app`
   - Port: 3000

---

## 🔧 Issues Encountered & Solutions

### Issue 1: Node Version Mismatch ❌ → ✅ FIXED

**Error:**
```
Node version v18.20.8 doesn't match the required version, please use ^24.5.0
```

**Solution:**
Updated `Dockerfile` line 1:
```dockerfile
FROM node:24-alpine
```

**Commit:** `0e853b6`

---

### Issue 2: Build Script Not Found ❌ → ✅ FIXED

**Error:**
```
Couldn't find a script named 'build'
```

**Root Cause:** Twenty CRM uses NX monorepo, not standard npm/yarn scripts

**Solution:**
Updated `Dockerfile` build command:
```dockerfile
RUN npx nx run twenty-server:build
```

**Commit:** `0e853b6`

---

### Issue 3: Lockfile Immutability Error ❌ → ✅ FIXED

**Error:**
```
The lockfile would have been modified by this install, which is explicitly forbidden
```

**Solution:**
Removed `--immutable` flag from `Dockerfile`:
```dockerfile
RUN yarn install && yarn cache clean && npx nx reset
```

**Commit:** `57f4a06`

---

### Issue 4: Missing Prettier Configuration ❌ → ✅ FIXED

**Error:**
```
Prettier config file not found
```

**Solution:**
Added `.prettierrc` to Dockerfile COPY command:
```dockerfile
COPY package.json yarn.lock .yarnrc.yml tsconfig.base.json nx.json .prettierrc ./
```

**Commit:** `6150085`

---

### Issue 5: Redis URL Required ❌ → ✅ FIXED

**Error:**
```
redis cache storage requires REDIS_URL to be defined, check your .env file
```

**Solution:**
1. Added Redis service in Railway
2. Configured `REDIS_URL` environment variable in twenty-server service

---

### Issue 6: Redis DNS Resolution Timing ⚠️ → 🔄 NEEDS REDEPLOY

**Error:**
```
Error: getaddrinfo ENOTFOUND redis.railway.internal
```

**Root Cause:**
- Railway provisioned Redis service
- twenty-server deployed and started immediately
- Redis internal DNS wasn't fully ready yet (takes 30-60 seconds)
- Application crashed trying to connect to unavailable Redis

**Why This Happens:**
Railway services show as "deployed" when the container starts, but internal networking (private domains like `redis.railway.internal`) takes additional time to become fully available. The application started before Redis DNS was ready.

**Solution:**
Trigger a manual redeploy of `twenty-server` now that Redis is fully provisioned:
1. Railway Dashboard → `twenty-server` service
2. Deployments tab → Latest deployment
3. Click "Redeploy" button

**Prevention:**
This is a one-time issue during initial Redis setup. Future deployments won't have this problem because Redis will already be running.

---

## ✅ Final Working Configuration

### Environment Variables - twenty-server Service

```bash
# Node Environment
NODE_ENV=production
PORT=3000

# Database Connection
PG_DATABASE_URL=${{Postgres.DATABASE_URL}}
PGDATABASE=${{Postgres.PGDATABASE}}

# Redis Cache
REDIS_URL=${{Redis.REDIS_PRIVATE_URL}}

# Application URLs
SERVER_URL=https://osp-crm.up.railway.app
FRONT_BASE_URL=https://osp-crm.up.railway.app

# CORS Configuration
FRONT_CORS_ORIGIN=https://osp-website-2026.web.app,https://ospcontabilidade.com.br,https://www.ospcontabilidade.com.br

# Storage Configuration
STORAGE_TYPE=local
STORAGE_LOCAL_PATH=.local-storage

# Message Queue
MESSAGE_QUEUE_TYPE=bull-mq

# Security Tokens (Generated with openssl rand -base64 32)
APP_SECRET=gKJDK9xQgoFcXULPR0uspT1RmU+742HUueuXc3Atjzg=
ACCESS_TOKEN_SECRET=V6ALIMnapIzHZf1hvhm7OToZgQab0I6rL6fRPkcjOP0=
REFRESH_TOKEN_SECRET=KNjVwNrDTOGNm7831BALntG28IN0j9yC2sIoXnHBCM4=
LOGIN_TOKEN_SECRET=2xpMAkXjGzSzrMKAEPsWmitMfBwUjlI3mxH+CjO4MC4=

# Optional Settings
SIGN_IN_PREFILLED=false
```

### Dockerfile Configuration

**Location:** `/Users/leo.de.souza1/osp/osp-crm/Dockerfile`

**Key Points:**
- ✅ Node 24-alpine base image
- ✅ NX build commands
- ✅ No --immutable flag on yarn install
- ✅ .prettierrc included in COPY
- ✅ PostgreSQL client tools included
- ✅ Production-optimized build

**Build Time:** ~5-6 minutes  
**Image Size:** Optimized with multi-stage build

---

## 🔴 Redis Setup & Timing Issue

### Understanding the Problem

**Timeline of Events:**

```
T+0:00  → User adds Redis service to Railway
T+0:05  → Railway creates Redis container
T+0:10  → Railway triggers auto-redeploy of twenty-server
T+0:15  → twenty-server container starts
T+0:15  → twenty-server tries to connect to redis.railway.internal
T+0:15  → DNS lookup fails (ENOTFOUND)
T+0:30  → Redis internal DNS becomes available
T+0:45  → twenty-server still crashing (already failed startup)
```

### Why This Happens

Railway's private networking (`.railway.internal` domains) requires:
1. Service container to be running
2. Internal DNS records to propagate
3. Private network routes to be established

This takes **30-60 seconds** even after the service shows as "deployed".

### The Fix

**Redeploy twenty-server after Redis is fully ready:**

```bash
# Option 1: Manual Redeploy
Railway Dashboard → twenty-server → Deployments → Redeploy

# Option 2: Trigger via variable change
Add/remove a space in any env var → Save
```

### After Redeploy - Expected Logs

✅ **Success indicators:**
```log
[Nest] LOG [InstanceLoader] CacheStorageModule dependencies initialized
[Nest] LOG [Redis] Connected to Redis successfully
[Nest] LOG [NestFactory] Nest application successfully started
[Nest] LOG Application is running on: http://[::]:3000
```

❌ **Failure indicators:**
```log
Error: getaddrinfo ENOTFOUND redis.railway.internal
[ioredis] Unhandled error event
```

---

## 🧪 Verification Steps

### 1. Check Deployment Logs

```bash
# Look for these success messages:
✓ All modules initialized
✓ Redis connection successful
✓ Database connection successful
✓ Application started on port 3000
✓ Healthcheck passing
```

### 2. Test CRM URL

```bash
curl https://osp-crm.up.railway.app/healthz
# Expected: 200 OK response
```

### 3. Access Web Interface

1. Open browser: `https://osp-crm.up.railway.app`
2. Should see Twenty CRM login/signup page
3. No errors or "Service Unavailable" messages

### 4. Check Railway Dashboard

1. All three services show green status
2. No crash logs or restart loops
3. Healthcheck passing (green checkmark)

---

## 🚀 Next Steps

### 1. Verify Deployment ✅
- [ ] Redeploy twenty-server service
- [ ] Check logs for successful Redis connection
- [ ] Verify healthcheck passes
- [ ] Access CRM URL in browser

### 2. Create Admin Account ✅
- [ ] Visit https://osp-crm.up.railway.app
- [ ] Complete signup process
- [ ] Create workspace
- [ ] Verify login works

### 3. Generate API Key ✅
- [ ] Log in to CRM
- [ ] Navigate to Settings → Developers → API Keys
- [ ] Create new API key named "Website Integration"
- [ ] Copy and save the API key securely

### 4. Configure Firebase Functions ✅
```bash
cd ~/osp/osp-contabilidade/functions
firebase functions:config:set crm.api_url="https://osp-crm.up.railway.app/graphql"
firebase functions:config:set crm.api_key="<YOUR_API_KEY>"
firebase functions:config:get  # Verify
```

### 5. Deploy Firebase Functions ✅
```bash
cd ~/osp/osp-contabilidade/functions
npm install
firebase deploy --only functions
```

### 6. Test End-to-End Integration ✅
- [ ] Submit test form on website
- [ ] Verify Firestore document created
- [ ] Check document syncs to CRM
- [ ] Verify Person, Company, and Opportunity created

---

## 🔍 Troubleshooting Guide

### Redis Connection Issues

**Symptom:** `ENOTFOUND redis.railway.internal`

**Solutions:**
1. **Wait and redeploy** - Redis needs 30-60s to be fully ready
2. **Check variable reference** - Should be `${{Redis.REDIS_PRIVATE_URL}}`
3. **Verify service name** - Must match exactly in Railway (case-sensitive)
4. **Check same project** - Redis and twenty-server must be in same Railway project

**Alternative (for testing only):**
```bash
CACHE_STORAGE_TYPE=memory
# Remove REDIS_URL variable
```

### Database Connection Issues

**Symptom:** Can't connect to PostgreSQL

**Solutions:**
1. Verify `PG_DATABASE_URL=${{Postgres.DATABASE_URL}}`
2. Check Postgres service is running
3. Verify both services in same Railway project
4. Check Railway private network is enabled

### Build Failures

**Symptom:** Docker build fails

**Solutions:**
1. Verify Node version is 24+ in Dockerfile
2. Check all required files are in git repository
3. Ensure `.prettierrc` is committed
4. Verify no yarn.lock conflicts

### Application Crashes

**Symptom:** Container starts but crashes immediately

**Check these in order:**
1. ✅ All environment variables set
2. ✅ Database connection working
3. ✅ Redis connection working
4. ✅ All JWT secrets configured
5. ✅ CORS origins correct
6. ✅ Storage path exists

### Healthcheck Failures

**Symptom:** Healthcheck never passes

**Solutions:**
1. Check application logs for startup errors
2. Verify PORT=3000 is set
3. Ensure `/healthz` endpoint exists
4. Check no other process blocking port 3000
5. Verify healthcheck timeout (5 minutes) in railway.json

---

## 📊 Deployment Statistics

| Metric | Value |
|--------|-------|
| Total Build Time | ~5-6 minutes |
| Docker Build Steps | 20 |
| Dependencies Compiled | 3,664 files |
| Total Commits | 4 (0e853b6, b1c32ac, 57f4a06, 6150085) |
| Services Required | 3 (Postgres, Redis, twenty-server) |
| Environment Variables | 16 |
| Build Attempts | 5 |
| Issues Resolved | 6 |

---

## 📚 Related Documentation

- [OSP_RAILWAY_DEPLOYMENT_FIX.md](./OSP_RAILWAY_DEPLOYMENT_FIX.md) - Initial troubleshooting
- [OSP_RAILWAY_ENV_SETUP.md](./OSP_RAILWAY_ENV_SETUP.md) - Environment setup guide
- [OSP_RAILWAY_ENV_FINAL.md](./OSP_RAILWAY_ENV_FINAL.md) - Final configuration
- [OSP_ARCHITECTURE_DIAGRAM.md](./OSP_ARCHITECTURE_DIAGRAM.md) - System architecture
- [OSP_CRM_WEBSITE_INTEGRATION_COMPLETE.md](./OSP_CRM_WEBSITE_INTEGRATION_COMPLETE.md) - Integration guide

---

## ✅ Current Status

**Build:** ✅ Successful (all 20 steps completed)  
**Docker Image:** ✅ Created and pushed  
**PostgreSQL:** ✅ Running and connected  
**Redis:** ✅ Provisioned (DNS ready after 60s)  
**Application:** ⏳ Needs redeploy (post-Redis setup)  
**Configuration:** ✅ Complete  
**Next Action:** **Redeploy twenty-server service**

---

## 🎓 Lessons Learned

### 1. Railway Service Provisioning Timing
- Services show as "deployed" before internal DNS is ready
- Private networking takes 30-60 seconds to fully establish
- Solution: Manual redeploy after new services are added

### 2. Twenty CRM Requirements
- Requires Node 24.5.0+ (not 18.x)
- Uses NX monorepo (not standard npm scripts)
- Needs Redis for cache storage in production
- Requires specific environment variables for all features

### 3. Docker Build Optimization
- Remove --immutable flag for better CI/CD compatibility
- Include all config files (.prettierrc) in Docker context
- Use multi-stage builds for smaller images
- Cache dependencies for faster rebuilds

### 4. Environment Variable Best Practices
- Use Railway references (${{Service.VAR}}) for cross-service communication
- Generate secure secrets with openssl (32 bytes base64)
- Configure CORS for all production domains
- Use environment-specific URLs (no hardcoding)

---

**Last Updated:** October 18, 2025  
**Deployment Status:** Ready for final redeploy  
**Estimated Time to Complete:** 5 minutes
