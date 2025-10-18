# 🚀 OSP CRM & Website Integration - Complete Setup Guide

**Date:** October 18, 2025  
**Status:** Ready to deploy  
**Integration:** OSP Contabilidade Website → Twenty CRM on Railway

---

## 📋 Overview

This guide walks you through deploying your CRM to Railway and connecting it with your website forms so that all leads automatically create:
- 👤 **People** (contacts)
- 🏢 **Companies**
- 💰 **Opportunities** (sales pipeline)

---

## 🎯 What We're Building

```
Website Form Submit
        ↓
    Firestore
        ↓
Firebase Cloud Function
        ↓
Twenty CRM GraphQL API
        ↓
Creates: Person + Company + Opportunity
```

---

## Part 1: Deploy CRM to Railway

### Step 1: Fix Node.js Version in Dockerfile

Your CRM requires Node.js 24, but the Dockerfile was using Node 18. This has been fixed.

**File:** `/Users/leo.de.souza1/osp/osp-crm/Dockerfile`

✅ **Already updated to:**
```dockerfile
FROM node:24-alpine AS base
```

### Step 2: Commit and Push Changes

```bash
cd ~/osp/osp-crm

# Add the updated Dockerfile
git add Dockerfile railway.json

# Commit
git commit -m "Fix: Update Dockerfile to Node 24 for Railway deployment"

# Push to GitHub
git push origin main
```

### Step 3: Deploy to Railway

Follow the **Quick Start Guide:**

👉 **See:** `/Users/leo.de.souza1/osp/OSP_RAILWAY_QUICK_START.md`

**Key steps:**
1. Sign up at https://railway.app
2. Create project: `osp-crm`
3. Add PostgreSQL (one click)
4. Connect GitHub repo
5. Set environment variables
6. Generate public domain
7. Wait for deployment

**Estimated time:** 30 minutes

### Step 4: Save Your CRM URL

After deployment, you'll get a URL like:
```
https://osp-crm.up.railway.app
```

**Save this!** You'll need it for the next part.

---

## Part 2: Set Up Firebase Functions

### Step 5: Initialize Firebase Functions

```bash
cd ~/osp/osp-contabilidade

# Install Firebase Functions dependencies
cd functions
npm install

# Build TypeScript
npm run build
```

### Step 6: Configure CRM Connection

Set your Railway CRM URL and API key:

```bash
# Replace with your actual Railway URL
firebase functions:config:set crm.api_url="https://osp-crm.up.railway.app/graphql"

# You'll get the API key from your CRM after logging in
# (We'll do this in Step 9)
firebase functions:config:set crm.api_key="YOUR_API_KEY_HERE"

# Verify configuration
firebase functions:config:get
```

### Step 7: Update Firebase Config

Update `firebase.json` to include functions:

```bash
cd ~/osp/osp-contabilidade
```

Check if `firebase.json` includes functions:

```json
{
  "functions": {
    "source": "functions"
  },
  "hosting": {
    ...
  },
  "firestore": {
    ...
  }
}
```

If not, add the functions section.

---

## Part 3: Get CRM API Key

### Step 8: Access Your CRM

1. Open your Railway CRM URL: `https://osp-crm.up.railway.app`
2. Log in with your admin credentials
3. If first time, create admin account

### Step 9: Generate API Key

In your CRM:

1. Click ⚙️ **Settings** (bottom left)
2. Click **Developers** → **API Keys**
3. Click **+ New API Key**
4. Fill in:
   - **Name:** `Website Integration`
   - **Description:** `API key for OSP website contact forms`
   - **Expires:** Never (or 1 year)
5. Click **Create**
6. **⚠️ COPY THE KEY NOW** - you won't see it again!

Example key:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 10: Save API Key to Firebase

```bash
cd ~/osp/osp-contabilidade

# Set the API key (replace with your actual key)
firebase functions:config:set crm.api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Verify it's set
firebase functions:config:get
```

You should see:
```json
{
  "crm": {
    "api_url": "https://osp-crm.up.railway.app/graphql",
    "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

## Part 4: Configure CORS in CRM

### Step 11: Add Website URLs to CRM

Your CRM needs to allow requests from your website.

**In Railway Dashboard:**

1. Go to your `osp-crm` project
2. Click on **twenty-server** service
3. Go to **Variables** tab
4. Add new variable:

```bash
FRONT_CORS_ORIGIN=https://osp-website-2026.web.app,https://osp-website-2026.firebaseapp.com,https://contabilidade.osp.com.br
```

5. Railway will automatically redeploy (wait 2-3 minutes)

---

## Part 5: Deploy Firebase Functions

### Step 12: Deploy to Firebase

```bash
cd ~/osp/osp-contabilidade

# Deploy functions only
firebase deploy --only functions

# Or deploy everything
firebase deploy
```

**Wait for deployment to complete** (~2-3 minutes)

### Step 13: Verify Functions Are Live

Check Firebase Console:
1. Go to https://console.firebase.google.com
2. Select your project
3. Go to **Functions**
4. You should see:
   - `submitContactToCRM` (HTTP function)
   - `syncContactToCRM` (Firestore trigger)
   - `retryFailedSyncs` (Scheduled function)

---

## Part 6: Test the Integration

### Step 14: Test Form Submission

1. Go to your website: `https://osp-website-2026.web.app`
2. Navigate to contact form
3. Fill out the form with test data:
   - Name: Test User
   - Company: Test Company
   - Email: test@example.com
   - Phone: (11) 99999-9999
   - Purpose: Consultoria
   - Sector: Technology
   - Message: This is a test
4. Click **Submit**

### Step 15: Verify in Firestore

1. Go to Firebase Console → Firestore Database
2. Look for `contact_submissions` collection
3. Find your test submission
4. Check the document has:
   - ✅ `status: 'synced'`
   - ✅ `crmCompanyId: '...'`
   - ✅ `crmPersonId: '...'`
   - ✅ `crmOpportunityId: '...'`

### Step 16: Verify in CRM

1. Go to your CRM: `https://osp-crm.up.railway.app`
2. Check **People** section
   - Should see "Test User"
3. Check **Companies** section
   - Should see "Test Company"
4. Check **Opportunities** section
   - Should see "Test Company - Consultoria"

✅ **If you see all three, integration is working!**

---

## Part 7: Monitor and Maintain

### Step 17: Monitor Logs

**Firebase Functions logs:**
```bash
firebase functions:log
```

**Railway logs:**
1. Go to Railway dashboard
2. Click on **twenty-server**
3. Go to **Logs** tab

### Step 18: Check Failed Syncs

In Firestore, check for documents with `status: 'failed'`:

```bash
# View in Firebase Console
# Go to Firestore → contact_submissions
# Filter by status == 'failed'
```

Failed syncs will be automatically retried every hour by the `retryFailedSyncs` function.

---

## 🎯 Complete Checklist

### CRM Deployment
- [ ] Dockerfile updated to Node 24
- [ ] Changes committed and pushed to GitHub
- [ ] Railway account created
- [ ] CRM deployed to Railway
- [ ] Railway URL saved
- [ ] Admin account created in CRM
- [ ] API key generated and saved
- [ ] CORS configured in Railway

### Firebase Setup
- [ ] Firebase Functions initialized
- [ ] Functions dependencies installed
- [ ] CRM API URL configured
- [ ] CRM API key configured
- [ ] Firebase config verified
- [ ] Functions deployed to Firebase
- [ ] Functions visible in Firebase Console

### Testing
- [ ] Test form submitted on website
- [ ] Form data in Firestore
- [ ] Firestore document shows `status: 'synced'`
- [ ] Person created in CRM
- [ ] Company created in CRM
- [ ] Opportunity created in CRM

### Monitoring
- [ ] Firebase Functions logs checked
- [ ] Railway logs checked
- [ ] No errors in console
- [ ] Email notifications working (if configured)

---

## 🔧 Troubleshooting

### Issue: "CRM configuration missing"

**Solution:**
```bash
cd ~/osp/osp-contabilidade
firebase functions:config:get

# If empty, set again:
firebase functions:config:set crm.api_url="https://osp-crm.up.railway.app/graphql"
firebase functions:config:set crm.api_key="YOUR_KEY"

# Redeploy
firebase deploy --only functions
```

### Issue: "GraphQL errors" or "401 Unauthorized"

**Solution:**
1. Check API key is correct (no extra spaces)
2. Verify API key hasn't expired
3. Generate new API key in CRM if needed
4. Update Firebase config with new key
5. Redeploy functions

### Issue: "CORS error"

**Solution:**
1. Check `FRONT_CORS_ORIGIN` in Railway includes your website URL
2. Restart Railway service
3. Wait for deployment to complete
4. Clear browser cache and try again

### Issue: Form submits but no CRM data

**Solution:**
1. Check Firestore document status
2. If `status: 'failed'`, check `syncError` field
3. Check Firebase Functions logs:
   ```bash
   firebase functions:log --only syncContactToCRM
   ```
4. Verify CRM is accessible: `https://osp-crm.up.railway.app/graphql`
5. Test API key with curl:
   ```bash
   curl -X POST https://osp-crm.up.railway.app/graphql \
     -H "Authorization: Bearer YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"query":"{ __typename }"}'
   ```

### Issue: Railway build fails

**Solution:**
1. Check Railway logs for specific error
2. Verify Node version is 24 in Dockerfile
3. Check environment variables are set
4. Try manual redeploy in Railway dashboard

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     USER SUBMITS FORM                    │
└───────────────────────┬─────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              OSP WEBSITE (Firebase Hosting)              │
│                  ContactForm.tsx                         │
└───────────────────────┬─────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                    FIRESTORE DATABASE                    │
│              Collection: contact_submissions             │
│              Document: { ...formData }                   │
└───────────────────────┬─────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│           FIREBASE CLOUD FUNCTION (Trigger)              │
│              syncContactToCRM(snap, context)             │
└───────────────────────┬─────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                  GRAPHQL API CALLS                       │
│  1. findOrCreateCompany() → Company ID                   │
│  2. findOrCreatePerson() → Person ID                     │
│  3. createOpportunity() → Opportunity ID                 │
└───────────────────────┬─────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              TWENTY CRM (Railway)                        │
│        https://osp-crm.up.railway.app                    │
│                                                          │
│  ✅ Person created in People                            │
│  ✅ Company created in Companies                        │
│  ✅ Opportunity created in Opportunities                │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│          FIRESTORE UPDATED (Success)                     │
│  Document updated with:                                  │
│  - status: 'synced'                                      │
│  - crmCompanyId: '...'                                   │
│  - crmPersonId: '...'                                    │
│  - crmOpportunityId: '...'                               │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Pro Tips

### 1. Test Mode

During testing, use a specific email pattern:
- Use `test+[number]@osp.com.br`
- Example: `test+1@osp.com.br`, `test+2@osp.com.br`
- Makes it easy to find and delete test data

### 2. Monitoring Dashboard

Create a simple monitoring dashboard:
```bash
# Watch Firebase logs in real-time
firebase functions:log --only syncContactToCRM

# In another terminal, watch Railway
railway logs --service twenty-server
```

### 3. Batch Operations

To sync existing Firestore contacts to CRM:

```javascript
// Run in Firebase Console
const batch = db.batch();
const contacts = await db.collection('contact_submissions')
  .where('status', '==', 'new')
  .limit(10)
  .get();

contacts.forEach(doc => {
  batch.update(doc.ref, { status: 'pending' });
});

await batch.commit();
// Cloud Function will trigger for each
```

### 4. Custom Fields

To add custom fields to CRM:

1. Add fields in CRM Settings → Objects
2. Update Cloud Function mutations with new fields
3. Redeploy functions

### 5. Error Notifications

Add email notifications for failed syncs:

```typescript
// In Cloud Function
import * as nodemailer from 'nodemailer';

// On sync failure, send email
await sendEmail({
  to: 'admin@osp.com.br',
  subject: 'CRM Sync Failed',
  body: `Contact: ${formData.email}\nError: ${error.message}`
});
```

---

## 📈 Next Steps

### Phase 1: Production Deployment ✅ (You are here)
- [x] Deploy CRM to Railway
- [x] Deploy Firebase Functions
- [x] Test integration
- [ ] Monitor for 48 hours

### Phase 2: Enhancements (Week 2)
- [ ] Add email notifications
- [ ] Create admin dashboard for monitoring
- [ ] Add analytics tracking
- [ ] Set up automated reports

### Phase 3: Optimization (Month 1)
- [ ] Add custom fields to CRM
- [ ] Create automated workflows
- [ ] Integrate email marketing
- [ ] Set up team onboarding

---

## 📞 Support Resources

### Railway
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app
- Status: https://status.railway.app

### Twenty CRM
- Discord: https://discord.gg/cx5n4Jzs57
- Docs: https://twenty.com/developers
- GitHub: https://github.com/twentyhq/twenty

### Firebase
- Docs: https://firebase.google.com/docs/functions
- Console: https://console.firebase.google.com
- Status: https://status.firebase.google.com

---

## ✅ Success Criteria

Your integration is successful when:

✅ **Form Submission**
- User fills form on website
- Form submits without errors
- Success message displayed

✅ **Data Storage**
- Form data saved to Firestore
- Document has all fields
- Timestamp is accurate

✅ **CRM Sync**
- Person appears in CRM
- Company appears in CRM
- Opportunity appears in CRM
- All data is correct

✅ **Status Updates**
- Firestore document status = 'synced'
- CRM IDs are saved in Firestore
- No error messages in logs

✅ **Error Handling**
- Failed syncs are marked in Firestore
- Automatic retry works
- Errors are logged properly

---

## 🎉 You're Ready!

Follow this guide step-by-step, and you'll have a fully integrated CRM system connected to your website in about 1-2 hours.

**Questions?** Check the troubleshooting section or refer to the platform-specific docs.

**Good luck with your deployment! 🚀**
