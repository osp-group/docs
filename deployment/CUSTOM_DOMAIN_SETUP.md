# 🌐 OSP Custom Domain & Subdomain Setup Guide

**Created:** October 16, 2025  
**Purpose:** Configure professional subdomains for OSP services  
**Domain:** osp.com.br

---

## 📋 Overview

This guide shows you how to set up professional subdomains for your OSP infrastructure once you own `osp.com.br`.

### Your Planned Subdomain Structure

```
┌─────────────────────────────────────────────────────────┐
│                    osp.com.br                            │
│              (Main Company Website)                      │
└──────────────────────┬──────────────────────────────────┘
                       │
        ───────────────┼───────────────
        │              │              │
        ↓              ↓              ↓
┌──────────────┐  ┌──────────┐  ┌──────────────┐
│contabilidade │  │   crm    │  │   (future)   │
│.osp.com.br   │  │.osp.com.br  │  subdomains  │
│              │  │           │  │              │
│ Marketing    │  │ CRM       │  │ Other apps   │
│ Lead Capture │  │ System    │  │              │
│ (Firebase)   │  │ (Render)  │  │              │
└──────────────┘  └──────────┘  └──────────────┘
```

---

## ⏱️ Timeline

**Do this AFTER:**
- ✅ CRM is deployed to Render
- ✅ Website-CRM integration is working
- ✅ You own osp.com.br domain
- ✅ Everything tested on temporary URLs

**Why wait?**
- No point setting up custom domains until everything works
- DNS changes take time to propagate (up to 24 hours)
- Easier to debug with stable URLs first

---

## 🎯 Step 1: Prerequisites

Before starting:

- [ ] Own `osp.com.br` domain
- [ ] Have access to domain registrar (where you bought it)
- [ ] CRM deployed and working on Render
- [ ] Website deployed and working on Firebase
- [ ] Integration between website and CRM tested
- [ ] Know your current temporary URLs

**Your Current URLs:**
- CRM: `https://[your-app].onrender.com`
- Website: `https://osp-website-2026.web.app`

---

## 🎯 Step 2: Plan Your DNS Records

Here's what DNS records you'll need to add:

### For Main Site (osp.com.br)

This can point to whatever you want your main site to be:

**Option A: Redirect to contabilidade subdomain**
```
Type: CNAME
Name: @ (or leave blank)
Value: contabilidade.osp.com.br
```

**Option B: Point to a specific service**
```
Type: A
Name: @ (or leave blank)
Value: [IP address of your main site]
```

### For Marketing Site (contabilidade.osp.com.br)

Will be configured in Firebase:

```
Type: A
Name: contabilidade
Value: [Firebase provides this]

Type: TXT
Name: contabilidade
Value: [Firebase provides this for verification]
```

### For CRM (crm.osp.com.br)

Will be configured in Render:

```
Type: CNAME
Name: crm
Value: [your-app].onrender.com
```

---

## 🎯 Step 3: Configure CRM Custom Domain

### 3.1 In Render Dashboard

1. **Go to Render Dashboard:** https://dashboard.render.com
2. Click on your **server** service (the CRM)
3. Click **"Settings"** tab
4. Scroll down to **"Custom Domain"** section
5. Click **"Add Custom Domain"**

### 3.2 Add Your Subdomain

1. Enter: `crm.osp.com.br`
2. Click "Save"
3. Render will show you DNS instructions:
   ```
   Add a CNAME record:
   
   Name: crm
   Value: your-app-xxxxx.onrender.com
   ```
4. **Copy these values** - you'll need them next

### 3.3 Add DNS Record in Domain Registrar

1. **Log into your domain registrar** (e.g., Registro.br, GoDaddy, Hostgator)
2. **Find DNS Management** (might be called "DNS Settings", "Manage DNS", "Zone Editor")
3. **Add new CNAME record:**
   - **Type:** CNAME
   - **Name:** crm (or crm.osp.com.br depending on registrar)
   - **Value:** [the value Render gave you]
   - **TTL:** 3600 (or Auto/Default)
4. **Save changes**

### 3.4 Wait for DNS Propagation

- **Minimum:** 10 minutes
- **Average:** 1-2 hours
- **Maximum:** 24-48 hours (rare)

**Check status:**
```bash
# Check if DNS is propagated
nslookup crm.osp.com.br

# Or use online tool:
# https://www.whatsmydns.net
```

### 3.5 Verify in Render

1. Go back to Render dashboard
2. Check Custom Domain section
3. When DNS is propagated, you'll see:
   - ✅ DNS Configured
   - ✅ SSL Certificate Active

**Render automatically provides HTTPS!** No extra configuration needed.

---

## 🎯 Step 4: Configure Website Custom Domain

### 4.1 In Firebase Console

1. **Go to Firebase Console:** https://console.firebase.google.com
2. Select your project: `osp-website-2026`
3. Click **"Hosting"** in left menu
4. Click **"Add custom domain"** button

### 4.2 Enter Your Subdomain

1. Enter: `contabilidade.osp.com.br`
2. Click "Continue"
3. Firebase will show you DNS records to add

### 4.3 Verify Ownership

Firebase will ask you to add a TXT record:

```
Type: TXT
Name: contabilidade (or _acme-challenge.contabilidade)
Value: [long string provided by Firebase]
```

1. **Add this TXT record** in your domain registrar
2. **Wait 5-10 minutes**
3. **Click "Verify"** in Firebase console

### 4.4 Connect Your Domain

After verification, Firebase will show A records:

```
Type: A
Name: contabilidade
Value: 151.101.1.195

Type: A
Name: contabilidade
Value: 151.101.65.195
```

1. **Add these A records** in your domain registrar
2. **Save changes**
3. **Wait for DNS propagation** (15 minutes to 24 hours)

### 4.5 Wait for SSL Certificate

Firebase will automatically provision an SSL certificate:
- This can take up to 24 hours
- Status shows as "Pending" then "Connected"
- You'll get HTTPS automatically

---

## 🎯 Step 5: Update Environment Variables

Once both custom domains are active, update your configurations:

### 5.1 Update Render Environment Variables

1. Go to Render dashboard → Your CRM service
2. Click "Environment" tab
3. Update these variables:

```
FRONT_BASE_URL=https://crm.osp.com.br
SERVER_URL=https://crm.osp.com.br
FRONT_CORS_ORIGIN=https://contabilidade.osp.com.br,https://osp.com.br
```

4. Click "Save Changes"
5. Render will automatically redeploy (takes 2-3 minutes)

### 5.2 Update Firebase Functions Configuration

Update your CRM API URL:

```bash
cd ~/osp/osp-contabilidade

firebase functions:config:set crm.api_url="https://crm.osp.com.br/graphql"

# View config to verify
firebase functions:config:get
```

### 5.3 Redeploy Firebase Functions

```bash
firebase deploy --only functions
```

Wait 2-3 minutes for deployment to complete.

### 5.4 Update Contact Form (if hardcoded)

If your contact form has the URL hardcoded, update it:

**File:** `client/src/components/ContactForm.tsx`

Change:
```typescript
const FIREBASE_FUNCTION_URL = 
  import.meta.env.PROD 
    ? 'https://us-central1-osp-website-2026.cloudfunctions.net/submitContactToCRM'
    : 'http://localhost:5001/osp-website-2026/us-central1/submitContactToCRM';
```

This doesn't change (Firebase Functions URLs don't change), but verify it's correct.

---

## 🎯 Step 6: Test Everything

### 6.1 Test CRM Access

1. **Open browser** and go to: `https://crm.osp.com.br`
2. **Verify:**
   - ✅ Page loads
   - ✅ HTTPS padlock icon showing
   - ✅ Can log in
   - ✅ Dashboard works normally

### 6.2 Test Website Access

1. **Open browser** and go to: `https://contabilidade.osp.com.br`
2. **Verify:**
   - ✅ Page loads
   - ✅ HTTPS padlock icon showing
   - ✅ All pages working
   - ✅ Images loading correctly

### 6.3 Test Form Submission

1. Go to: `https://contabilidade.osp.com.br/contato`
2. Fill out contact form with test data
3. Submit form
4. **Verify:**
   - ✅ Success message appears
   - ✅ No errors in browser console
5. Go to: `https://crm.osp.com.br`
6. Check Opportunities
7. **Verify:**
   - ✅ New opportunity created
   - ✅ Person (contact) created
   - ✅ Company created (if provided)

### 6.4 Check SSL Certificates

Use this tool to verify SSL: https://www.ssllabs.com/ssltest/

Test both:
- `https://crm.osp.com.br`
- `https://contabilidade.osp.com.br`

Should both get an **A or A+ rating**.

---

## 🎯 Step 7: Update Documentation & Links

### 7.1 Update Internal Documentation

Update all documentation with new URLs:
- OSP_MASTER_GUIDE.md
- OSP_QUICK_REFERENCE.md
- Any internal wikis or notes

### 7.2 Update External Links

If applicable:
- Google My Business
- Social media profiles
- Email signatures
- Business cards
- Marketing materials

### 7.3 Set Up Redirects

**In Firebase Hosting:**

Create/update `firebase.json` to redirect old URL:

```json
{
  "hosting": {
    "public": "dist/public",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "redirects": [
      {
        "source": "/:path*",
        "destination": "https://contabilidade.osp.com.br/:path*",
        "type": 301
      }
    ]
  }
}
```

This ensures anyone visiting `osp-website-2026.web.app` gets redirected to your custom domain.

---

## 🐛 Troubleshooting

### Issue: DNS not propagating after 24 hours

**Solution:**
1. Check your DNS records in registrar - make sure there are no typos
2. Make sure TTL is set to 3600 or lower (not 86400)
3. Try flushing your local DNS cache:
   ```bash
   # macOS
   sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
   
   # Windows
   ipconfig /flushdns
   ```
4. Test from different network (mobile data vs wifi)
5. Use online DNS checker: https://www.whatsmydns.net

### Issue: SSL certificate not provisioning

**Render:**
- Usually automatic within 5 minutes
- Make sure DNS is properly configured first
- Contact Render support if stuck

**Firebase:**
- Can take up to 24 hours
- Make sure A records are correct
- Status shows in Firebase Console → Hosting

### Issue: CORS errors after custom domain

**Solution:**
1. Update `FRONT_CORS_ORIGIN` in Render to include new domain
2. Make sure there are no trailing slashes
3. Restart CRM service in Render
4. Clear browser cache
5. Test in incognito mode

### Issue: Form submissions fail after domain change

**Solution:**
1. Check Firebase Functions logs:
   ```bash
   firebase functions:log
   ```
2. Verify CRM API URL is updated in Functions config
3. Test CRM API directly:
   ```bash
   curl https://crm.osp.com.br/graphql \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"query":"query { currentUser { id } }"}'
   ```
4. Check browser console for errors
5. Verify API key is still valid

### Issue: Old URL still showing in search results

**Solution:**
- This is normal and will update over time (1-4 weeks)
- Speed it up:
  1. Submit new sitemap to Google Search Console
  2. Request indexing of new URLs
  3. Set up 301 redirects from old URLs

---

## 📋 DNS Record Reference

Here's a quick reference of all DNS records you need:

### For Domain Registrar (e.g., Registro.br)

```
# Main domain (optional - can point anywhere)
@ or blank → [your choice]

# Marketing/Website subdomain (Firebase)
Type: A
Name: contabilidade
Value: 151.101.1.195

Type: A
Name: contabilidade
Value: 151.101.65.195

Type: TXT (for verification)
Name: contabilidade or _acme-challenge.contabilidade
Value: [Firebase provides this]

# CRM subdomain (Render)
Type: CNAME
Name: crm
Value: your-app-xxxxx.onrender.com
```

---

## ✅ Post-Setup Checklist

After everything is configured:

- [ ] Both domains accessible via HTTPS
- [ ] SSL certificates showing valid
- [ ] Form submission creates lead in CRM
- [ ] No CORS errors
- [ ] Redirects from old URLs working
- [ ] All team members can access CRM
- [ ] Email notifications working (if configured)
- [ ] Monitoring/alerts set up
- [ ] Documentation updated with new URLs
- [ ] Search engine submission (optional)

---

## 💰 Costs

**Domain Registration:**
- `.com.br` domain: ~R$40-60/year (via Registro.br)

**Hosting (no change):**
- Firebase: Still FREE
- Render: Still $7-25/month

**SSL Certificates:**
- Both Firebase and Render: FREE (automatic)

**Total Additional Cost:** Just the domain registration!

---

## 🎯 Timeline Summary

| Task | Time Required | Can Work Immediately? |
|------|---------------|----------------------|
| Add DNS records | 5 minutes | No, needs propagation |
| DNS propagation | 10 min - 24 hours | No, must wait |
| SSL certificate (Render) | 5-10 minutes | After DNS works |
| SSL certificate (Firebase) | Up to 24 hours | After DNS works |
| Update environment variables | 10 minutes | Yes |
| Test everything | 30 minutes | After SSL works |
| **Total** | **1-3 days** | Patience required! |

---

## 📞 Support Resources

**DNS/Domain Issues:**
- Registro.br support (if using .br domain)
- Your domain registrar's support

**Firebase Hosting:**
- Firebase Console → Hosting → Support
- https://firebase.google.com/support

**Render Custom Domains:**
- Render docs: https://render.com/docs/custom-domains
- Render support: support@render.com

**DNS Propagation Check:**
- https://www.whatsmydns.net
- https://dnschecker.org

**SSL Testing:**
- https://www.ssllabs.com/ssltest/
- Built-in browser tools (padlock icon)

---

## 🎉 Success!

Once everything is set up, you'll have:

✅ **Professional URLs:**
- `https://crm.osp.com.br`
- `https://contabilidade.osp.com.br`
- `https://osp.com.br` (main site)

✅ **Automatic HTTPS** on all domains

✅ **Seamless integration** that looks professional to clients

✅ **Scalable infrastructure** ready for future services

✅ **Easy to remember** URLs for your team

**Your OSP digital ecosystem is now complete!** 🚀

---

## 📝 Notes

- Save this document for future reference
- Keep track of when you registered domain (renewal dates)
- Document any changes you make
- Consider setting calendar reminders for domain renewal
- Back up DNS configuration screenshots

**Remember:** DNS changes always take time. Don't panic if things don't work immediately. Most issues resolve themselves within a few hours as DNS propagates globally.

Good luck with your custom domain setup! 🍀
