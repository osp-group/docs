# 🔧 OSP Integration - Implementation Files

This document contains all the code you'll need to implement the website-to-CRM integration.

---

## 📁 File 1: Firebase Function (Main Integration Logic)

**Location:** `osp-contabilidade/functions/src/index.ts`

```typescript
/**
 * OSP Website to CRM Integration
 * Firebase Cloud Function that bridges website forms to CRM GraphQL API
 */

import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
import axios from 'axios';
import * as cors from 'cors';

// Initialize Firebase Admin
admin.initializeApp();

// Initialize CORS with your website domain
const corsHandler = cors({
  origin: [
    'https://osp-website-2026.web.app',
    'https://osp-website-2026.firebaseapp.com',
    'http://localhost:5000' // For local testing
  ],
  credentials: true
});

// CRM Configuration
const CRM_CONFIG = {
  apiUrl: functions.config().crm?.api_url || process.env.CRM_API_URL,
  apiKey: functions.config().crm?.api_key || process.env.CRM_API_KEY,
};

// Validate configuration on startup
if (!CRM_CONFIG.apiUrl || !CRM_CONFIG.apiKey) {
  console.error('❌ CRM configuration missing! Set with: firebase functions:config:set');
}

/**
 * Interface for contact form data from website
 */
interface ContactFormData {
  name: string;
  company: string;
  role?: string;
  email: string;
  phone: string;
  message: string;
}

/**
 * Split full name into first and last names
 */
function splitName(fullName: string): { firstName: string; lastName: string } {
  const parts = fullName.trim().split(' ');
  if (parts.length === 1) {
    return { firstName: parts[0], lastName: '' };
  }
  const firstName = parts[0];
  const lastName = parts.slice(1).join(' ');
  return { firstName, lastName };
}

/**
 * Extract domain from email
 */
function extractDomain(email: string): string {
  const match = email.match(/@(.+)$/);
  return match ? match[1] : '';
}

/**
 * Create a person (contact) in CRM
 */
async function createPersonInCRM(data: ContactFormData): Promise<string> {
  const { firstName, lastName } = splitName(data.name);

  const mutation = `
    mutation CreatePerson($data: PersonCreateInput!) {
      createPerson(data: $data) {
        id
        name {
          firstName
          lastName
        }
        email
      }
    }
  `;

  const variables = {
    data: {
      name: {
        firstName,
        lastName,
      },
      email: data.email,
      phone: data.phone || null,
      jobTitle: data.role || null,
    },
  };

  try {
    const response = await axios.post(
      CRM_CONFIG.apiUrl,
      { query: mutation, variables },
      {
        headers: {
          'Authorization': `Bearer ${CRM_CONFIG.apiKey}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.data.errors) {
      throw new Error(`GraphQL errors: ${JSON.stringify(response.data.errors)}`);
    }

    const personId = response.data.data.createPerson.id;
    console.log('✅ Person created:', personId);
    return personId;

  } catch (error: any) {
    console.error('❌ Error creating person:', error.response?.data || error.message);
    throw new Error(`Failed to create person: ${error.message}`);
  }
}

/**
 * Create a company in CRM
 */
async function createCompanyInCRM(companyName: string, email: string): Promise<string> {
  const domain = extractDomain(email);

  const mutation = `
    mutation CreateCompany($data: CompanyCreateInput!) {
      createCompany(data: $data) {
        id
        name
        domainName
      }
    }
  `;

  const variables = {
    data: {
      name: companyName,
      domainName: domain || null,
    },
  };

  try {
    const response = await axios.post(
      CRM_CONFIG.apiUrl,
      { query: mutation, variables },
      {
        headers: {
          'Authorization': `Bearer ${CRM_CONFIG.apiKey}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.data.errors) {
      throw new Error(`GraphQL errors: ${JSON.stringify(response.data.errors)}`);
    }

    const companyId = response.data.data.createCompany.id;
    console.log('✅ Company created:', companyId);
    return companyId;

  } catch (error: any) {
    console.error('⚠️ Error creating company:', error.response?.data || error.message);
    // Company creation is optional, so we don't throw
    return '';
  }
}

/**
 * Create an opportunity in CRM
 */
async function createOpportunityInCRM(
  data: ContactFormData,
  personId: string,
  companyId?: string
): Promise<string> {
  const { firstName, lastName } = splitName(data.name);
  const opportunityName = `Website Lead - ${firstName} ${lastName}`;

  const mutation = `
    mutation CreateOpportunity($data: OpportunityCreateInput!) {
      createOpportunity(data: $data) {
        id
        name
        stage
      }
    }
  `;

  const variables = {
    data: {
      name: opportunityName,
      stage: 'NEW',
      pointOfContactId: personId,
      companyId: companyId || null,
      description: data.message || null,
    },
  };

  try {
    const response = await axios.post(
      CRM_CONFIG.apiUrl,
      { query: mutation, variables },
      {
        headers: {
          'Authorization': `Bearer ${CRM_CONFIG.apiKey}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.data.errors) {
      throw new Error(`GraphQL errors: ${JSON.stringify(response.data.errors)}`);
    }

    const opportunityId = response.data.data.createOpportunity.id;
    console.log('✅ Opportunity created:', opportunityId);
    return opportunityId;

  } catch (error: any) {
    console.error('❌ Error creating opportunity:', error.response?.data || error.message);
    throw new Error(`Failed to create opportunity: ${error.message}`);
  }
}

/**
 * Main Firebase Cloud Function - Submit Contact Form
 * 
 * This function:
 * 1. Validates form data
 * 2. Creates person (contact) in CRM
 * 3. Creates company in CRM (if provided)
 * 4. Creates opportunity in CRM
 * 5. Saves backup to Firestore
 */
export const submitContactToCRM = functions.https.onRequest((request, response) => {
  return corsHandler(request, response, async () => {
    // Only allow POST requests
    if (request.method !== 'POST') {
      response.status(405).send({ error: 'Method not allowed' });
      return;
    }

    try {
      const formData: ContactFormData = request.body;

      // Validate required fields
      if (!formData.name || !formData.email || !formData.company) {
        response.status(400).send({
          error: 'Missing required fields: name, email, company'
        });
        return;
      }

      console.log('📝 Processing form submission:', formData.email);

      // Step 1: Create person in CRM
      const personId = await createPersonInCRM(formData);

      // Step 2: Create company in CRM (if company name provided)
      let companyId = '';
      if (formData.company) {
        companyId = await createCompanyInCRM(formData.company, formData.email);
      }

      // Step 3: Create opportunity in CRM
      const opportunityId = await createOpportunityInCRM(formData, personId, companyId);

      // Step 4: Save backup to Firestore (keep existing functionality)
      await admin.firestore().collection('contact_submissions').add({
        ...formData,
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        status: 'synced_to_crm',
        crmPersonId: personId,
        crmCompanyId: companyId || null,
        crmOpportunityId: opportunityId,
      });

      // Success response
      response.status(200).send({
        success: true,
        message: 'Contact submitted successfully to CRM',
        data: {
          personId,
          companyId: companyId || null,
          opportunityId,
        },
      });

      console.log('✅ Form submission complete:', {
        email: formData.email,
        personId,
        companyId,
        opportunityId,
      });

    } catch (error: any) {
      console.error('❌ Error processing form submission:', error);

      // Save error to Firestore for debugging
      try {
        await admin.firestore().collection('contact_submission_errors').add({
          formData: request.body,
          error: error.message,
          timestamp: admin.firestore.FieldValue.serverTimestamp(),
        });
      } catch (dbError) {
        console.error('Failed to log error to Firestore:', dbError);
      }

      // Return error response
      response.status(500).send({
        success: false,
        error: 'Failed to submit contact form',
        message: error.message,
      });
    }
  });
});

/**
 * Test function to verify CRM connection
 * Call this to test your API key and connection
 */
export const testCRMConnection = functions.https.onRequest(async (request, response) => {
  try {
    const testQuery = `
      query {
        currentUser {
          id
          email
        }
      }
    `;

    const result = await axios.post(
      CRM_CONFIG.apiUrl,
      { query: testQuery },
      {
        headers: {
          'Authorization': `Bearer ${CRM_CONFIG.apiKey}`,
          'Content-Type': 'application/json',
        },
      }
    );

    response.status(200).send({
      success: true,
      message: 'CRM connection successful',
      data: result.data,
    });

  } catch (error: any) {
    response.status(500).send({
      success: false,
      error: 'CRM connection failed',
      message: error.message,
      details: error.response?.data,
    });
  }
});
```

---

## 📁 File 2: Firebase Functions Package.json

**Location:** `osp-contabilidade/functions/package.json`

```json
{
  "name": "functions",
  "scripts": {
    "lint": "eslint --ext .js,.ts .",
    "build": "tsc",
    "build:watch": "tsc --watch",
    "serve": "npm run build && firebase emulators:start --only functions",
    "shell": "npm run build && firebase functions:shell",
    "start": "npm run shell",
    "deploy": "firebase deploy --only functions",
    "logs": "firebase functions:log"
  },
  "engines": {
    "node": "18"
  },
  "main": "lib/index.js",
  "dependencies": {
    "firebase-admin": "^11.8.0",
    "firebase-functions": "^4.3.1",
    "axios": "^1.6.0",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "@typescript-eslint/eslint-plugin": "^5.12.0",
    "@typescript-eslint/parser": "^5.12.0",
    "eslint": "^8.9.0",
    "eslint-config-google": "^0.14.0",
    "eslint-plugin-import": "^2.25.4",
    "firebase-functions-test": "^3.1.0",
    "typescript": "^4.9.0",
    "@types/cors": "^2.8.13"
  },
  "private": true
}
```

---

## 📁 File 3: Updated Contact Form Component

**Location:** `osp-contabilidade/client/src/components/ContactForm.tsx`

```typescript
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { useTranslation } from "react-i18next";
import { Loader2 } from "lucide-react";

// Firebase Function endpoint
const FIREBASE_FUNCTION_URL = 
  import.meta.env.PROD 
    ? 'https://us-central1-osp-website-2026.cloudfunctions.net/submitContactToCRM'
    : 'http://localhost:5001/osp-website-2026/us-central1/submitContactToCRM';

export default function ContactForm() {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    name: "",
    company: "",
    role: "",
    email: "",
    phone: "",
    message: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Submit to Firebase Function (which then sends to CRM)
      const response = await fetch(FIREBASE_FUNCTION_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok && result.success) {
        // Show success message
        toast({
          title: t('contact.form.successTitle'),
          description: t('contact.form.successDescription'),
        });
        
        // Reset form
        setFormData({
          name: "",
          company: "",
          role: "",
          email: "",
          phone: "",
          message: "",
        });
      } else {
        throw new Error(result.error || 'Failed to submit form');
      }
    } catch (error) {
      // Show error message
      toast({
        title: "Erro ao enviar",
        description: "Não foi possível enviar sua mensagem. Por favor, tente novamente.",
        variant: "destructive",
      });
      console.error("Error submitting contact form:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-2xl" aria-label={t('contact.form.title')}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="name">
            {t('contact.form.name')} {t('contact.form.required')}
          </Label>
          <Input
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            data-testid="input-name"
            aria-required="true"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="company">
            {t('contact.form.company')} {t('contact.form.required')}
          </Label>
          <Input
            id="company"
            name="company"
            value={formData.company}
            onChange={handleChange}
            required
            data-testid="input-company"
            aria-required="true"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="role">{t('contact.form.role')}</Label>
          <Input
            id="role"
            name="role"
            value={formData.role}
            onChange={handleChange}
            data-testid="input-role"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="email">
            {t('contact.form.email')} {t('contact.form.required')}
          </Label>
          <Input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
            data-testid="input-email"
            aria-required="true"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="phone">
          {t('contact.form.phone')} {t('contact.form.required')}
        </Label>
        <Input
          id="phone"
          name="phone"
          type="tel"
          value={formData.phone}
          onChange={handleChange}
          required
          placeholder={t('contact.form.phonePlaceholder')}
          data-testid="input-phone"
          aria-required="true"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="message">
          {t('contact.form.message')} {t('contact.form.required')}
        </Label>
        <Textarea
          id="message"
          name="message"
          value={formData.message}
          onChange={handleChange}
          required
          rows={5}
          placeholder={t('contact.form.messagePlaceholder')}
          data-testid="textarea-message"
          aria-required="true"
        />
      </div>

      <Button 
        type="submit" 
        size="lg" 
        className="w-full md:w-auto" 
        data-testid="button-submit-contact"
        disabled={isSubmitting}
      >
        {isSubmitting ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            {t('contact.form.sending') || 'Enviando...'}
          </>
        ) : (
          t('contact.form.submit')
        )}
      </Button>
    </form>
  );
}
```

---

## 📁 File 4: Environment Configuration

**Location:** `osp-contabilidade/.env` (local development)

```bash
# CRM Configuration for local testing
CRM_API_URL=http://localhost:3000/graphql
CRM_API_KEY=your_api_key_here_once_you_generate_it
```

---

## 📁 File 5: Firebase Functions Configuration Script

**Filename:** `configure-firebase-functions.sh`

```bash
#!/bin/bash

# OSP Firebase Functions Configuration Script
# This script sets up your Firebase Functions environment variables

echo "🔧 Configuring Firebase Functions for OSP Website to CRM Integration"
echo ""

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Login to Firebase
echo "🔐 Logging in to Firebase..."
firebase login

# Set CRM API URL
read -p "Enter your CRM API URL (e.g., https://osp-crm.onrender.com/graphql): " CRM_URL
firebase functions:config:set crm.api_url="$CRM_URL"

# Set CRM API Key
read -p "Enter your CRM API Key: " CRM_KEY
firebase functions:config:set crm.api_key="$CRM_KEY"

# Verify configuration
echo ""
echo "✅ Configuration set! Verifying..."
firebase functions:config:get

echo ""
echo "🎉 Configuration complete!"
echo ""
echo "Next steps:"
echo "1. Deploy functions: firebase deploy --only functions"
echo "2. Test the integration"
```

Make it executable:
```bash
chmod +x configure-firebase-functions.sh
```

---

## 🚀 Deployment Commands Cheat Sheet

### Initial Setup
```bash
# 1. Navigate to website folder
cd ~/osp/osp-contabilidade

# 2. Initialize Firebase Functions (if not already done)
firebase init functions

# 3. Install dependencies
cd functions
npm install
cd ..

# 4. Configure environment variables
./configure-firebase-functions.sh
# OR manually:
firebase functions:config:set crm.api_url="https://your-crm.onrender.com/graphql"
firebase functions:config:set crm.api_key="your_api_key"
```

### Local Testing
```bash
# Terminal 1: Start Firebase emulators
firebase emulators:start

# Terminal 2: Start your website dev server
npm run dev

# Test by submitting form at http://localhost:5000/contato
```

### Deploy to Production
```bash
# Deploy functions only
firebase deploy --only functions

# Deploy functions and hosting together
firebase deploy

# View logs
firebase functions:log
```

### Troubleshooting
```bash
# View function logs
firebase functions:log

# View specific function logs
firebase functions:log --only submitContactToCRM

# Test CRM connection
curl https://us-central1-osp-website-2026.cloudfunctions.net/testCRMConnection
```

---

## ✅ Implementation Checklist

Use this to track your progress:

### Pre-Implementation
- [ ] Read the integration plan document
- [ ] CRM deployed to Render.com
- [ ] CRM is accessible and you can log in
- [ ] API key generated in CRM
- [ ] API key stored securely

### Firebase Functions Setup
- [ ] Firebase CLI installed (`npm install -g firebase-tools`)
- [ ] Logged into Firebase (`firebase login`)
- [ ] Functions initialized (`firebase init functions`)
- [ ] Dependencies installed (`cd functions && npm install`)
- [ ] Environment variables configured
- [ ] Code files created (index.ts, package.json)

### Website Updates
- [ ] ContactForm.tsx updated
- [ ] Environment variable added (.env)
- [ ] Local testing completed

### Testing
- [ ] Local emulator testing works
- [ ] Form submission creates person in CRM
- [ ] Form submission creates company in CRM
- [ ] Form submission creates opportunity in CRM
- [ ] Error handling tested
- [ ] Firestore backup still works

### Deployment
- [ ] Functions deployed to Firebase
- [ ] Production website tested
- [ ] Logs monitored for errors
- [ ] First real lead captured successfully!

### Post-Deployment
- [ ] Monitor functions usage (Firebase Console)
- [ ] Check CRM for new leads daily
- [ ] Set up alerts for function errors
- [ ] Document any issues or customizations

---

## 🎯 Quick Start (Copy-Paste Ready)

Once you have your CRM deployed and API key, run these commands:

```bash
# 1. Navigate to website
cd ~/osp/osp-contabilidade

# 2. Create functions folder if not exists
mkdir -p functions/src

# 3. Copy the code from File 1 into functions/src/index.ts

# 4. Copy the code from File 2 into functions/package.json

# 5. Install dependencies
cd functions
npm install
cd ..

# 6. Configure Firebase
firebase functions:config:set crm.api_url="YOUR_CRM_URL/graphql"
firebase functions:config:set crm.api_key="YOUR_API_KEY"

# 7. Test locally
firebase emulators:start

# 8. Deploy to production
firebase deploy --only functions

# 9. Update ContactForm.tsx with File 3 code

# 10. Deploy website
firebase deploy
```

---

## 📞 Need Help?

If you get stuck:

1. **Check Firebase logs:** `firebase functions:log`
2. **Check CRM logs:** In Render.com dashboard → Logs
3. **Test CRM connection:** Use the `testCRMConnection` function
4. **Verify API key:** Try making a manual curl request

**Remember:** This is beginner-friendly! Don't hesitate to ask questions. Each error message will guide us to the solution. 🚀
