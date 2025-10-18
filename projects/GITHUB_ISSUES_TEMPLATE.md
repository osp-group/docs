# GitHub Issues Template - OSP Group Projects

Use this template to create issues in the GitHub Project Board.

---

## 🔴 CRITICAL: CRM Database Migration Not Executing

**Labels:** `critical`, `bug`, `crm`, `deployment`  
**Project:** OSP Group  
**Milestone:** CRM Deployment  
**Priority:** P0

### Description
Twenty CRM v0.2.1 deployed to Railway is starting successfully but database migrations are not executing, resulting in 404 errors due to missing database tables.

### Current Status
- ✅ Application starts successfully
- ✅ Redis connection working
- ✅ PostgreSQL connection working
- ✅ Environment variable `RUN_DATABASE_MIGRATIONS="true"` is set
- ❌ No migration logs in deployment output
- ❌ Database table `core.keyValuePair` does not exist
- ❌ Accessing https://osp-crm.up.railway.app shows 404

### Environment
- **Platform:** Railway
- **Application:** Twenty CRM v0.2.1
- **Services:** PostgreSQL, Redis, twenty-server
- **Region:** europe-west4
- **URL:** https://osp-crm.up.railway.app

### Expected Behavior
Migrations should execute automatically when `RUN_DATABASE_MIGRATIONS="true"` is set, creating all necessary database tables.

### Steps to Reproduce
1. Deploy Twenty CRM to Railway with PostgreSQL and Redis
2. Set environment variable `RUN_DATABASE_MIGRATIONS="true"`
3. Application starts but migrations don't run
4. Access application URL → 404 page

### Proposed Solution
1. Run migrations manually via Railway CLI:
   ```bash
   railway shell --service twenty-server
   yarn database:migrate:prod
   ```
2. Or execute via Railway run command:
   ```bash
   railway run --service twenty-server yarn database:migrate:prod
   ```

### Tasks
- [ ] Install Railway CLI on local machine
- [ ] Connect to twenty-server service
- [ ] Run migration command manually
- [ ] Verify tables created in PostgreSQL
- [ ] Test CRM accessibility
- [ ] Create first workspace
- [ ] Document migration process

### Dependencies
- Blocks: #2 (Website-CRM Integration)
- Blocks: #3 (Custom Domain Setup)

### References
- [Deployment Logs](../deployment/RAILWAY_REDIS_COMPLETE.md)
- [Architecture Overview](../architecture/OVERVIEW.md)

---

## 🟡 Website-CRM Integration - Lead Capture

**Labels:** `enhancement`, `integration`, `contabilidade`, `crm`  
**Project:** OSP Group  
**Milestone:** Q4 2025  
**Priority:** P1

### Description
Integrate website contact forms with Twenty CRM for automated lead capture and management.

### Current Status
- ✅ Firebase Functions implemented for form handling
- ✅ Firestore database configured
- ❌ Waiting for CRM deployment completion
- ❌ CRM API key not yet generated

### Scope
Connect ospcontabilidade.com.br contact forms to Twenty CRM to automatically create:
- Person records
- Company records
- Opportunity records

### Implementation Steps
1. [ ] Wait for CRM deployment (#1) to complete
2. [ ] Access CRM and create admin account
3. [ ] Generate API key in CRM Settings → Developers → API Keys
4. [ ] Configure Firebase Functions:
   ```bash
   cd ~/osp/osp-contabilidade/functions
   firebase functions:config:set crm.api_url="https://osp-crm.up.railway.app/graphql"
   firebase functions:config:set crm.api_key="[KEY_FROM_CRM]"
   ```
5. [ ] Deploy Firebase Functions:
   ```bash
   firebase deploy --only functions
   ```
6. [ ] Test form submission on production website
7. [ ] Verify lead appears in CRM under:
   - People (contact person)
   - Companies (company name)
   - Opportunities (sales opportunity)

### Testing Checklist
- [ ] Form submission successful
- [ ] Firestore document created with `syncStatus: "synced"`
- [ ] Person created in CRM with correct fields
- [ ] Company created in CRM (if provided)
- [ ] Opportunity created in CRM
- [ ] All fields mapped correctly (name, email, phone, message)

### Dependencies
- **Blocked by:** #1 (CRM Database Migration)
- **Related:** #3 (Custom Domain Setup)

### References
- [Integration Guide](../integration/CRM_WEBSITE_INTEGRATION.md)
- [Firebase Functions Code](https://github.com/osp-group/contabilidade/tree/main/functions)

---

## 🟡 Custom Domain Configuration

**Labels:** `infrastructure`, `deployment`, `all-repos`  
**Project:** OSP Group  
**Milestone:** Q4 2025  
**Priority:** P1

### Description
Configure custom domains for all OSP Group services with proper SSL/TLS certificates.

### Proposed Domains
- **CRM:** crm.ospcontabilidade.com.br
- **Contabilidade:** ospcontabilidade.com.br (existing)
- **Digital:** [TBD]

### Tasks
1. [ ] Decide on domain strategy for CRM
2. [ ] Purchase additional domains if needed
3. [ ] Configure DNS records:
   - [ ] A records
   - [ ] CNAME records
   - [ ] TXT records for verification
4. [ ] Railway Configuration:
   - [ ] Add custom domain to twenty-server service
   - [ ] Wait for SSL certificate provisioning
5. [ ] Update CORS settings in CRM:
   ```bash
   FRONT_CORS_ORIGIN="https://ospcontabilidade.com.br,https://www.ospcontabilidade.com.br"
   ```
6. [ ] Update Firebase Functions config with new CRM URL
7. [ ] Test all integrations with new domains

### Dependencies
- **Requires:** #1 (CRM deployment must be complete)
- **Impacts:** #2 (Will require Firebase Functions config update)

### References
- [Custom Domain Setup Guide](../deployment/CUSTOM_DOMAIN_SETUP.md)

---

## 🟢 SEO Optimization - Contabilidade

**Labels:** `enhancement`, `seo`, `contabilidade`  
**Project:** OSP Group  
**Milestone:** Q1 2026  
**Priority:** P2

### Description
Optimize ospcontabilidade.com.br for search engines to improve organic traffic and rankings.

### Completed
- ✅ SEO inventory completed
- ✅ URL mapping created
- ✅ Current structure documented

### Pending Tasks
1. [ ] **URL Redirects**
   - [ ] Implement 301 redirects based on mapping
   - [ ] Test all redirect chains
   - [ ] Verify no broken links

2. [ ] **Meta Tags**
   - [ ] Add unique meta descriptions to all pages
   - [ ] Optimize title tags (50-60 characters)
   - [ ] Add Open Graph tags for social sharing
   - [ ] Implement structured data (JSON-LD)

3. [ ] **Content Optimization**
   - [ ] Add alt text to all images
   - [ ] Optimize heading hierarchy (H1, H2, H3)
   - [ ] Improve internal linking
   - [ ] Add FAQ schema

4. [ ] **Performance**
   - [ ] Convert images to WebP format
   - [ ] Implement lazy loading
   - [ ] Minify CSS/JS
   - [ ] Enable HTTP/2

5. [ ] **Technical SEO**
   - [ ] Generate XML sitemap
   - [ ] Submit sitemap to Google Search Console
   - [ ] Create robots.txt
   - [ ] Set up Google Analytics 4

### References
- [SEO Inventory](../repositories/contabilidade/SEO_INVENTORY.md)
- [URL Mapping](https://github.com/osp-group/contabilidade/blob/main/osp-url-mapping-master.csv)

---

## 🟢 Digital Website Enhancement

**Labels:** `enhancement`, `content`, `digital`  
**Project:** OSP Group  
**Milestone:** Q1 2026  
**Priority:** P2

### Description
Update and enhance the OSP Digital website to better showcase services and capabilities.

### Tasks
1. [ ] **Content Audit**
   - [ ] Review current pages
   - [ ] Identify missing content
   - [ ] Update outdated information

2. [ ] **Services Portfolio**
   - [ ] Create detailed service pages
   - [ ] Add case studies
   - [ ] Include client testimonials

3. [ ] **Lead Generation**
   - [ ] Add contact forms
   - [ ] Integrate with CRM (after #1 and #2)
   - [ ] Implement conversion tracking

4. [ ] **Visual Updates**
   - [ ] Update design system
   - [ ] Add modern UI components
   - [ ] Improve mobile responsiveness

### References
- [Digital Repository](https://github.com/osp-group/digital)
- [Design Guidelines](https://github.com/osp-group/digital/blob/main/design_guidelines.md)

---

## How to Use This Template

1. **Create Repository Issues:**
   - Go to each repository
   - Create new issue
   - Copy relevant section from above
   - Add appropriate labels
   - Assign to team members

2. **Link to GitHub Project:**
   - Create/use existing GitHub Project in osp-group organization
   - Add issues to project board
   - Organize by status (Todo, In Progress, Done)
   - Track progress visually

3. **Update Regularly:**
   - Check off completed tasks
   - Update status as work progresses
   - Add comments with updates
   - Link related PRs

4. **Cross-Reference:**
   - Use `#issue-number` to reference related issues
   - Mention blocking relationships
   - Keep dependencies updated

