# OSP Group - Prioritized Issues List

**Created:** October 18, 2025  
**Purpose:** Complete list of issues to create on GitHub Project Board

---

## 🔴 Phase 1: CRM Foundation & Website Integration (Critical)

### Repository: `osp-group/crm`

#### Issue 1.1: Fix Database Migration Deployment
**Priority:** P0 - Critical  
**Labels:** `critical`, `bug`, `deployment`, `crm`  
**Estimated Effort:** 3 points  
**Blocks:** All other CRM issues

**Description:**
Database migrations not executing on Railway deployment despite `RUN_DATABASE_MIGRATIONS="true"` being set. Application starts but shows 404 due to missing database tables.

**Tasks:**
- [ ] Install Railway CLI locally
- [ ] Connect to twenty-server service via Railway shell
- [ ] Run migration command: `yarn database:migrate:prod`
- [ ] Verify all tables created (core.keyValuePair, etc.)
- [ ] Access CRM at https://osp-crm.up.railway.app
- [ ] Verify no 404 errors
- [ ] Document migration process in docs repo

**Acceptance Criteria:**
- ✅ CRM accessible without errors
- ✅ All database tables exist
- ✅ Can create workspace and login

---

#### Issue 1.2: Configure CRM Data Model for Lead Capture
**Priority:** P0 - Critical  
**Labels:** `enhancement`, `crm`, `data-model`, `integration`  
**Estimated Effort:** 5 points  
**Depends on:** Issue 1.1  
**Blocks:** Issue 2.1, 2.2

**Description:**
Configure Twenty CRM tables and fields to properly receive and organize leads from ospcontabilidade.com.br contact forms. Ensure data structure matches website submission format.

**Current Website Form Fields:**
- Name (string, required)
- Email (string, required)
- Phone (string, optional)
- Company (string, optional)
- Message (text, required)
- Service Interest (select, optional)
- Source (hidden: "website-contact")

**Required CRM Configuration:**

1. **Person Object (Standard)**
   - ✅ Name → firstName + lastName (split)
   - ✅ Email → email (primary)
   - ✅ Phone → phone
   - 🆕 Add custom field: `sourceWebsite` (text)
   - 🆕 Add custom field: `initialMessage` (long text)
   - 🆕 Add custom field: `serviceInterest` (select)

2. **Company Object (Standard)**
   - ✅ Name → companyName
   - 🆕 Link to Person via `companyId`

3. **Opportunity Object (Standard)**
   - ✅ Name → Auto-generate: "[Company/Person] - [Service Interest]"
   - ✅ Stage → "Lead" (initial stage)
   - ✅ Amount → null (to be qualified)
   - ✅ Point of Contact → Link to Person
   - ✅ Company → Link to Company (if provided)
   - 🆕 Add custom field: `leadSource` (select: Website, Referral, Cold, etc.)
   - 🆕 Add custom field: `captureDate` (datetime)

**Tasks:**
- [ ] Login to CRM (after Issue 1.1)
- [ ] Navigate to Settings → Data Model
- [ ] Add custom fields to Person:
  - `sourceWebsite` (Text)
  - `initialMessage` (Long Text)
  - `serviceInterest` (Select: Accounting, Tax, Consulting, Other)
- [ ] Add custom fields to Opportunity:
  - `leadSource` (Select: Website, Referral, Cold Outreach, Partner)
  - `captureDate` (DateTime)
- [ ] Configure default Opportunity stages:
  - Lead → Qualified → Proposal → Negotiation → Won/Lost
- [ ] Test manual lead creation with sample data
- [ ] Document field mapping in integration docs
- [ ] Generate API key for Firebase Functions

**Acceptance Criteria:**
- ✅ All custom fields created and visible in CRM
- ✅ Can manually create Person → Company → Opportunity
- ✅ Field mapping documented
- ✅ API key generated and securely stored

---

### Repository: `osp-group/contabilidade`

#### Issue 2.1: Update Firebase Functions for CRM Integration
**Priority:** P0 - Critical  
**Labels:** `enhancement`, `integration`, `contabilidade`, `firebase`  
**Estimated Effort:** 8 points  
**Depends on:** Issue 1.1, Issue 1.2  
**Blocks:** Issue 2.2

**Description:**
Update existing Firebase Functions to integrate with Twenty CRM API, ensuring all form submissions create proper Person, Company, and Opportunity records with correct field mapping.

**Current State:**
- ✅ `submitContactToCRM` function exists
- ✅ Firestore for temporary storage works
- ❌ CRM configuration missing
- ❌ Field mapping needs update for custom fields

**Implementation Steps:**

1. **Configure Firebase Functions Environment**
   ```bash
   cd ~/osp/osp-contabilidade/functions
   firebase functions:config:set crm.api_url="https://osp-crm.up.railway.app/graphql"
   firebase functions:config:set crm.api_key="[KEY_FROM_ISSUE_1.2]"
   firebase functions:config:get  # Verify
   ```

2. **Update GraphQL Mutations**
   - Update `createPerson` mutation to include custom fields:
     - `sourceWebsite`
     - `initialMessage`
     - `serviceInterest`
   - Update `createCompany` mutation (if company provided)
   - Update `createOpportunity` mutation to include:
     - `leadSource: "Website"`
     - `captureDate: new Date()`
     - Link to Person and Company

3. **Update Form Data Mapping**
   ```javascript
   // Map form data to CRM fields
   const [firstName, ...lastNameParts] = formData.name.split(' ');
   const lastName = lastNameParts.join(' ');
   
   const personData = {
     firstName,
     lastName,
     email: formData.email,
     phone: formData.phone || null,
     sourceWebsite: 'ospcontabilidade.com.br',
     initialMessage: formData.message,
     serviceInterest: formData.service || 'General Inquiry'
   };
   ```

4. **Add Error Handling & Retry Logic**
   - Catch CRM API errors
   - Log failures to Firestore with `syncStatus: "failed"`
   - Implement retry function for failed syncs
   - Send admin notification on repeated failures

5. **Update Existing Functions**
   - `syncContactToCRM`: Main integration function
   - `submitContactToCRM`: Form submission handler
   - `retryFailedSyncs`: Scheduled retry (runs every 15 minutes)

**Tasks:**
- [ ] Set Firebase Functions config with CRM credentials
- [ ] Update GraphQL mutation queries
- [ ] Implement field mapping logic
- [ ] Add comprehensive error handling
- [ ] Update retry logic for failed syncs
- [ ] Add logging for debugging
- [ ] Write unit tests for mapping functions
- [ ] Deploy functions to production
- [ ] Test with sample form submission

**Testing Checklist:**
- [ ] Form submission successful on website
- [ ] Firestore document created with syncStatus
- [ ] Person created in CRM with all fields
- [ ] Company created if provided
- [ ] Opportunity created and linked correctly
- [ ] Error handling works (test with invalid data)
- [ ] Retry logic works for failed syncs

**Acceptance Criteria:**
- ✅ Firebase Functions deployed successfully
- ✅ Form submissions create CRM records
- ✅ All custom fields populated correctly
- ✅ Error handling and retry logic working
- ✅ No data loss on form submissions

---

#### Issue 2.2: End-to-End Website-CRM Integration Testing
**Priority:** P0 - Critical  
**Labels:** `testing`, `integration`, `contabilidade`, `crm`  
**Estimated Effort:** 5 points  
**Depends on:** Issue 2.1

**Description:**
Comprehensive testing of the complete lead capture flow from website form submission through CRM record creation.

**Test Scenarios:**

1. **Complete Form Submission (Happy Path)**
   - Fill all fields: Name, Email, Phone, Company, Service, Message
   - Submit form
   - Verify Firestore: syncStatus = "synced"
   - Verify CRM:
     - Person created with all fields
     - Company created
     - Opportunity created with correct stage
     - All relationships linked correctly

2. **Minimal Form Submission**
   - Fill only required: Name, Email, Message
   - No phone, no company
   - Verify Person created, no Company, Opportunity still created

3. **Duplicate Submissions**
   - Submit same email twice
   - Verify CRM handles duplicates (update vs create new)

4. **Error Scenarios**
   - Invalid email format
   - CRM API temporarily down
   - Verify Firestore marks as "failed"
   - Verify retry function picks it up

5. **Performance Testing**
   - Submit 10 forms in quick succession
   - Verify all processed within 30 seconds
   - Check for race conditions

**Tasks:**
- [ ] Create test form submissions document
- [ ] Test complete form (all fields)
- [ ] Test minimal form (required only)
- [ ] Test duplicate email handling
- [ ] Test error scenarios
- [ ] Test retry mechanism
- [ ] Verify data integrity in CRM
- [ ] Check Firebase Functions logs
- [ ] Document any issues found
- [ ] Create monitoring dashboard (if needed)

**Acceptance Criteria:**
- ✅ All test scenarios pass
- ✅ No data loss in any scenario
- ✅ Error handling works correctly
- ✅ Performance meets requirements (<30s)
- ✅ Duplicate handling works as expected
- ✅ Documentation updated with findings

---

## 🟡 Phase 2: CRM Workflow Configuration (High Priority)

### Repository: `osp-group/crm`

#### Issue 3.1: Configure Sales Workflow Stages
**Priority:** P1 - High  
**Labels:** `enhancement`, `crm`, `workflow`, `sales`  
**Estimated Effort:** 5 points  
**Depends on:** Issue 1.2

**Description:**
Set up proper sales workflow stages in Twenty CRM to guide sales team through the lead-to-customer journey. Configure automation where possible.

**Proposed Workflow:**

1. **Lead** (Initial stage)
   - Auto-assigned from website
   - Needs qualification

2. **Qualified**
   - Lead verified as legitimate
   - Contact made
   - Needs assessment scheduled

3. **Needs Assessment**
   - Discovery call completed
   - Requirements documented
   - Proposal needed

4. **Proposal Sent**
   - Formal proposal delivered
   - Awaiting client review

5. **Negotiation**
   - Price/terms discussion
   - Contract review

6. **Won**
   - Deal closed
   - Contract signed
   - Onboarding started

7. **Lost**
   - Deal lost
   - Reason documented

**Tasks:**
- [ ] Configure Opportunity stages in CRM
- [ ] Set probability percentages for each stage
- [ ] Define required fields for stage transitions
- [ ] Create stage transition rules (if possible)
- [ ] Add custom fields for lost reasons
- [ ] Configure notifications for stage changes
- [ ] Create dashboard for pipeline visualization
- [ ] Document workflow in process docs
- [ ] Train sales team on workflow

**Automation Ideas:**
- Auto-assign leads round-robin to sales team
- Auto-notify sales rep when new lead arrives
- Auto-send email templates at certain stages
- Auto-create follow-up tasks based on stage

**Acceptance Criteria:**
- ✅ All stages configured and visible
- ✅ Probability percentages set
- ✅ Transition rules defined
- ✅ Sales team trained
- ✅ Pipeline dashboard working

---

#### Issue 3.2: Create Sales Team User Accounts & Permissions
**Priority:** P1 - High  
**Labels:** `administration`, `crm`, `access-control`  
**Estimated Effort:** 3 points  
**Depends on:** Issue 1.1

**Description:**
Set up user accounts for sales team members with appropriate permissions and roles.

**User Roles:**

1. **Admin** (1 user)
   - Full system access
   - User management
   - Settings configuration

2. **Sales Manager** (1-2 users)
   - View all opportunities
   - Reassign leads
   - Generate reports
   - View team performance

3. **Sales Representative** (3-5 users)
   - View assigned opportunities
   - Update opportunity details
   - Create activities/notes
   - Close deals

**Tasks:**
- [ ] Define role permissions in CRM
- [ ] Create user accounts for each team member
- [ ] Assign appropriate roles
- [ ] Configure workspace settings
- [ ] Set up email notifications per role
- [ ] Create onboarding checklist for new users
- [ ] Document user management process
- [ ] Test permissions for each role

**Security Considerations:**
- Limit data export to Admin/Manager only
- Restrict deletion permissions
- Audit log for sensitive changes
- Regular permission reviews

**Acceptance Criteria:**
- ✅ All user accounts created
- ✅ Roles assigned correctly
- ✅ Permissions tested and working
- ✅ Users can login successfully
- ✅ Onboarding documentation complete

---

#### Issue 3.3: Implement Lead Assignment & Routing Rules
**Priority:** P1 - High  
**Labels:** `enhancement`, `crm`, `automation`, `workflow`  
**Estimated Effort:** 5 points  
**Depends on:** Issue 3.2

**Description:**
Configure automatic lead assignment rules to distribute incoming leads fairly among sales team members.

**Assignment Strategy:**

**Option 1: Round Robin (Recommended for Start)**
- Distribute leads evenly among active sales reps
- Skip reps who are on vacation/inactive
- Reset counter monthly

**Option 2: Territory-Based**
- Assign based on company location (if provided)
- Useful as team grows

**Option 3: Service-Based**
- Assign based on service interest
- Match rep expertise with client needs

**Tasks:**
- [ ] Choose assignment strategy (start with Round Robin)
- [ ] Configure assignment rules in CRM
- [ ] Test assignment with sample leads
- [ ] Add manual reassignment capability for managers
- [ ] Configure notifications:
  - Email to assigned rep
  - Slack notification (if integrated)
  - In-app notification
- [ ] Create reassignment workflow for declined leads
- [ ] Add vacation/inactive status handling
- [ ] Document assignment rules

**Metrics to Track:**
- Leads assigned per rep
- Response time by rep
- Conversion rate by rep
- Reassignment frequency

**Acceptance Criteria:**
- ✅ Assignment rules configured and active
- ✅ Leads distributed fairly
- ✅ Notifications working
- ✅ Reassignment process working
- ✅ Metrics dashboard created

---

## 🟢 Phase 3: Additional Website Integration (Medium Priority)

### Repository: `osp-group/digital`

#### Issue 4.1: Migrate Digital Website to Firebase Hosting
**Priority:** P2 - Medium  
**Labels:** `deployment`, `infrastructure`, `digital`  
**Estimated Effort:** 8 points  

**Description:**
Migrate OSP Digital website to Firebase Hosting to consolidate infrastructure and enable easy CRM integration for lead capture.

**Current State:**
- Platform: [Current hosting - Vercel?]
- Framework: [React/Vite]
- Domain: [Current domain]

**Target State:**
- Platform: Firebase Hosting
- Same framework and build process
- Shared Firebase project with contabilidade site
- Unified lead capture system

**Migration Steps:**

1. **Firebase Project Setup**
   - Use existing Firebase project from contabilidade
   - Add digital site as separate hosting target
   - Configure hosting settings

2. **Configure Firebase Hosting**
   ```bash
   cd ~/osp/osp-digital
   firebase init hosting
   # Select existing project
   # Public directory: dist
   # Configure as SPA: Yes
   # Setup automatic builds: Yes
   ```

3. **Update Build Configuration**
   - Add firebase.json
   - Configure hosting targets
   - Set up deployment scripts
   - Configure custom domain

4. **DNS Configuration**
   - Point domain to Firebase
   - Configure SSL certificate
   - Test DNS propagation

5. **Deploy & Test**
   - Deploy to Firebase preview
   - Test all pages and functionality
   - Verify forms work
   - Update domain DNS
   - Monitor for issues

**Tasks:**
- [ ] Backup current site
- [ ] Initialize Firebase in digital repo
- [ ] Configure hosting settings
- [ ] Update build scripts
- [ ] Deploy to Firebase preview
- [ ] Test thoroughly
- [ ] Configure custom domain
- [ ] Update DNS records
- [ ] Deploy to production
- [ ] Monitor for 24 hours
- [ ] Document deployment process

**Rollback Plan:**
- Keep current hosting active for 7 days
- DNS can be reverted quickly
- Have backup of current configuration

**Acceptance Criteria:**
- ✅ Site live on Firebase Hosting
- ✅ All pages working correctly
- ✅ Custom domain configured
- ✅ SSL certificate active
- ✅ Performance equal or better
- ✅ Deployment documented

---

#### Issue 4.2: Add Contact Forms to Digital Website
**Priority:** P2 - Medium  
**Labels:** `enhancement`, `digital`, `forms`, `integration`  
**Estimated Effort:** 5 points  
**Depends on:** Issue 4.1

**Description:**
Add contact/inquiry forms to OSP Digital website and integrate with CRM using the same Firebase Functions infrastructure as the contabilidade site.

**Forms to Add:**

1. **General Contact Form**
   - Location: Contact page
   - Fields: Name, Email, Phone, Company, Service Interest, Message
   - Submit to: Same Firebase Function as contabilidade

2. **Service-Specific Forms**
   - Location: Each service page
   - Pre-fill service interest based on page
   - Same structure as general form

3. **Quick Quote Form**
   - Location: Homepage, sidebar
   - Fields: Name, Email, Service (required), Message (optional)
   - Quick conversion focus

**Tasks:**
- [ ] Design form UI matching digital site design
- [ ] Create reusable form component
- [ ] Add form validation
- [ ] Integrate with Firebase Functions (reuse from contabilidade)
- [ ] Add success/error messages
- [ ] Configure source tracking: "digital-website"
- [ ] Add to relevant pages
- [ ] Test form submissions
- [ ] Verify CRM integration works
- [ ] Add analytics tracking

**Form Data Structure:**
```javascript
{
  name: string,
  email: string,
  phone: string (optional),
  company: string (optional),
  service: string,
  message: string,
  source: "digital-website",
  page: "/services/web-development", // Track which page
  timestamp: Date
}
```

**Acceptance Criteria:**
- ✅ Forms added to all relevant pages
- ✅ Forms visually match site design
- ✅ Validation working correctly
- ✅ Submissions reach CRM
- ✅ User receives confirmation
- ✅ Analytics tracking active

---

#### Issue 4.3: Cross-Link Digital and Contabilidade Websites
**Priority:** P2 - Medium  
**Labels:** `enhancement`, `seo`, `digital`, `contabilidade`  
**Estimated Effort:** 3 points  
**Depends on:** Issue 4.1

**Description:**
Create strategic cross-links between OSP Digital and OSP Contabilidade websites to improve SEO, user experience, and lead generation across both properties.

**Linking Strategy:**

**From Digital → Contabilidade:**
- Footer: "OSP Contabilidade - Accounting Services"
- Services page: Link to accounting when relevant
- Blog posts: Natural contextual links

**From Contabilidade → Digital:**
- Footer: "OSP Digital - Digital Services"
- Services: "Need a website? Visit OSP Digital"
- Digital transformation content

**Tasks:**
- [ ] Identify strategic link opportunities
- [ ] Design link placement (UI/UX)
- [ ] Add links to navigation/footer
- [ ] Add contextual in-content links
- [ ] Implement link tracking (UTM parameters)
- [ ] Update sitemaps
- [ ] Test all links
- [ ] Monitor referral traffic
- [ ] Document linking strategy

**SEO Benefits:**
- Improved domain authority through internal linking
- Better crawlability
- Increased page authority
- Cross-traffic between sites

**Acceptance Criteria:**
- ✅ Links added to both sites
- ✅ Links properly tracked
- ✅ No broken links
- ✅ Sitemaps updated
- ✅ Referral traffic visible in analytics

---

## 🟢 Phase 4: SEO Optimization (Medium Priority)

### Repository: `osp-group/contabilidade`

#### Issue 5.1: Implement URL Structure & Redirects
**Priority:** P2 - Medium  
**Labels:** `seo`, `enhancement`, `contabilidade`  
**Estimated Effort:** 8 points

**Description:**
Implement proper URL structure and 301 redirects based on the SEO inventory and URL mapping created in Delivery 1.

**Current State:**
- ✅ SEO inventory completed
- ✅ URL mapping created (osp-url-mapping-master.csv)
- ❌ Redirects not implemented
- ❌ Some URLs suboptimal

**Implementation:**

1. **Analyze Mapping File**
   - Review osp-url-mapping-master.csv
   - Identify redirect requirements
   - Prioritize by traffic/importance

2. **Implement Redirects**
   - Configure Firebase Hosting redirects in firebase.json
   - Add 301 permanent redirects for old URLs
   - Test each redirect

3. **Optimize URL Structure**
   - Clean, descriptive URLs
   - Remove unnecessary parameters
   - Consistent naming convention
   - Proper hierarchy

**Tasks:**
- [ ] Review URL mapping spreadsheet
- [ ] Create redirect rules in firebase.json
- [ ] Test all redirects (manual + automated)
- [ ] Update internal links to use new URLs
- [ ] Update sitemap with new URLs
- [ ] Submit updated sitemap to Google
- [ ] Monitor Google Search Console for crawl errors
- [ ] Document redirect rules

**Redirect Configuration Example:**
```json
{
  "hosting": {
    "redirects": [
      {
        "source": "/old-page",
        "destination": "/new-page",
        "type": 301
      }
    ]
  }
}
```

**Acceptance Criteria:**
- ✅ All redirects implemented
- ✅ No broken links
- ✅ Redirects return 301 status
- ✅ Sitemap updated and submitted
- ✅ No increase in 404 errors

---

#### Issue 5.2: Add Comprehensive Meta Tags & Structured Data
**Priority:** P2 - Medium  
**Labels:** `seo`, `enhancement`, `contabilidade`  
**Estimated Effort:** 8 points

**Description:**
Add unique, optimized meta tags and structured data (JSON-LD) to all pages for improved SEO and rich search results.

**Required Meta Tags Per Page:**

1. **Essential Meta Tags**
   - `<title>` - Unique, 50-60 characters
   - `<meta name="description">` - Unique, 150-160 characters
   - `<meta name="keywords">` - Relevant keywords
   - `<link rel="canonical">` - Prevent duplicates

2. **Open Graph (Social Sharing)**
   - `og:title`
   - `og:description`
   - `og:image`
   - `og:url`
   - `og:type`

3. **Twitter Cards**
   - `twitter:card`
   - `twitter:title`
   - `twitter:description`
   - `twitter:image`

**Structured Data (Schema.org):**

1. **Organization Schema** (All pages)
   ```json
   {
     "@context": "https://schema.org",
     "@type": "AccountingService",
     "name": "OSP Contabilidade",
     "description": "...",
     "url": "https://ospcontabilidade.com.br",
     "logo": "...",
     "contactPoint": {...}
   }
   ```

2. **Service Schema** (Service pages)
3. **FAQPage Schema** (FAQ section)
4. **LocalBusiness Schema** (Contact page)

**Tasks:**
- [ ] Audit existing meta tags
- [ ] Write unique titles for all pages
- [ ] Write unique descriptions for all pages
- [ ] Add Open Graph tags
- [ ] Add Twitter Card tags
- [ ] Implement Organization schema
- [ ] Add Service schemas
- [ ] Add FAQ schema where applicable
- [ ] Add LocalBusiness schema
- [ ] Test with Google Rich Results Test
- [ ] Validate all structured data
- [ ] Document meta tag strategy

**Tools to Use:**
- Google Rich Results Test
- Schema.org validator
- Facebook Sharing Debugger
- Twitter Card Validator

**Acceptance Criteria:**
- ✅ All pages have unique titles & descriptions
- ✅ All social meta tags present
- ✅ Structured data validates without errors
- ✅ Rich results showing in Google test
- ✅ Social sharing previews working

---

#### Issue 5.3: Image Optimization & Performance
**Priority:** P2 - Medium  
**Labels:** `performance`, `seo`, `contabilidade`  
**Estimated Effort:** 5 points

**Description:**
Optimize all images for web performance: convert to WebP, implement lazy loading, add proper alt text, and optimize file sizes.

**Current Issues:**
- Large image file sizes
- Not using modern formats (WebP)
- Missing alt text on many images
- No lazy loading

**Optimization Strategy:**

1. **Format Conversion**
   - Convert PNG/JPG → WebP
   - Keep originals as fallback
   - Use `<picture>` element for compatibility

2. **File Size Reduction**
   - Compress images (target: <100KB each)
   - Use appropriate dimensions
   - No oversized images

3. **Lazy Loading**
   - Implement native lazy loading: `loading="lazy"`
   - Images below fold load on scroll
   - Faster initial page load

4. **Alt Text**
   - Descriptive alt text for all images
   - Include relevant keywords naturally
   - Improve accessibility

**Tasks:**
- [ ] Audit all images on site
- [ ] Convert images to WebP format
- [ ] Compress all images
- [ ] Resize oversized images
- [ ] Implement lazy loading
- [ ] Add/update alt text for all images
- [ ] Update image references in code
- [ ] Test in multiple browsers
- [ ] Measure performance improvement
- [ ] Update image optimization script

**Use Existing Script:**
```bash
cd ~/osp/osp-contabilidade
node optimize-images-fast.mjs
```

**Performance Targets:**
- Lighthouse score: >90
- Largest Contentful Paint: <2.5s
- First Input Delay: <100ms
- Cumulative Layout Shift: <0.1

**Acceptance Criteria:**
- ✅ All images converted to WebP
- ✅ All images <100KB (except hero images <200KB)
- ✅ Lazy loading implemented
- ✅ All images have descriptive alt text
- ✅ Lighthouse score improved
- ✅ Page load time reduced

---

## 📊 Summary by Repository

### osp-group/crm (6 issues)
1. ✅ Fix Database Migration Deployment (P0)
2. ✅ Configure CRM Data Model (P0)
3. ✅ Configure Sales Workflow Stages (P1)
4. ✅ Create Sales Team Accounts (P1)
5. ✅ Implement Lead Assignment Rules (P1)

### osp-group/contabilidade (5 issues)
1. ✅ Update Firebase Functions for CRM (P0)
2. ✅ End-to-End Integration Testing (P0)
3. ✅ Implement URL Redirects (P2)
4. ✅ Add Meta Tags & Structured Data (P2)
5. ✅ Image Optimization (P2)

### osp-group/digital (3 issues)
1. ✅ Migrate to Firebase Hosting (P2)
2. ✅ Add Contact Forms (P2)
3. ✅ Cross-Link with Contabilidade (P2)

**Total: 14 Issues across 3 repositories**

---

## 🎯 Implementation Order

### Week 1: CRM Foundation
- Issue 1.1: Fix Migration (CRM)
- Issue 1.2: Configure Data Model (CRM)
- Issue 2.1: Update Firebase Functions (Contabilidade)

### Week 2: Integration Testing & Workflows
- Issue 2.2: Integration Testing (Contabilidade)
- Issue 3.1: Sales Workflow (CRM)
- Issue 3.2: User Accounts (CRM)

### Week 3: Lead Management & Digital Site
- Issue 3.3: Lead Assignment (CRM)
- Issue 4.1: Migrate Digital to Firebase
- Issue 4.2: Add Forms to Digital

### Week 4: SEO & Polish
- Issue 5.1: URL Redirects (Contabilidade)
- Issue 5.2: Meta Tags (Contabilidade)
- Issue 5.3: Image Optimization (Contabilidade)
- Issue 4.3: Cross-Linking

---

## 📋 Next Steps

1. **Create GitHub Project Board**
   - Visit: https://github.com/orgs/osp-group/projects
   - Create new board: "OSP Group - Q4 2025"

2. **Create Issues**
   - Copy each issue above to appropriate repository
   - Add labels, assignees, estimates
   - Link dependencies

3. **Add to Project Board**
   - Organize by phase/week
   - Set up kanban columns
   - Track progress

4. **Start Work**
   - Begin with Phase 1 (Critical)
   - Update issue status as work progresses
   - Close issues when complete

---

**Last Updated:** October 18, 2025  
**Owner:** OSP Group Team
