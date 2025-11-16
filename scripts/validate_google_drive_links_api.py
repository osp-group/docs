#!/usr/bin/env python3
"""
Google Drive Links Validation Script with API Access - Phase 5 Advanced QA

Purpose:
  - Validate accessibility of all Google Drive links using Drive API
  - Check document permissions and sharing settings
  - Verify document exists and is accessible
  - Test @osp-group access permissions
  - Generate detailed permission report

Usage:
  python3 scripts/validate_google_drive_links_api.py <credentials.json>

Requirements:
  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

Setup:
  1. Create Google Cloud Project
  2. Enable Google Drive API
  3. Create Service Account
  4. Download credentials.json
  5. Share Drive files with service account email
  6. Run this script with credentials.json path

Output:
  - Console: Validation results and permission summary
  - File: testing/QA_GOOGLE_DRIVE_LINKS_ADVANCED_P6.md
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from google.api_errors import HttpError
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    print("⚠️  Google API libraries not installed")
    print("Install with: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")


class GoogleDriveAPIValidator:
    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path
        self.service = None
        self.links = {}
        self.stats = {
            "total": 0,
            "accessible": 0,
            "inaccessible": 0,
            "errors": 0,
            "by_hub": {},
        }
        self.permissions_report = {}
        self.errors = []
        self.warnings = []

        if GOOGLE_API_AVAILABLE and credentials_path:
            self._init_service(credentials_path)

    def _init_service(self, credentials_path: str):
        """Initialize Google Drive API service."""
        try:
            if not Path(credentials_path).exists():
                self.errors.append(f"Credentials file not found: {credentials_path}")
                return

            credentials = Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            self.service = build('drive', 'v3', credentials=credentials)
            print("✅ Google Drive API initialized successfully")
        except Exception as e:
            self.errors.append(f"Failed to initialize Drive API: {str(e)}")
            self.service = None

    def extract_doc_id(self, url: str) -> Optional[str]:
        """Extract document ID from Google Drive URL."""
        patterns = [
            r'https://docs\.google\.com/document/d/([a-zA-Z0-9_-]+)',
            r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)',
            r'https://docs\.google\.com/presentation/d/([a-zA-Z0-9_-]+)',
            r'https://drive\.google\.com/.*[?&]id=([a-zA-Z0-9_-]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def check_document_access(self, doc_id: str) -> Tuple[bool, Dict]:
        """Check if document is accessible via API."""
        result = {
            "accessible": False,
            "title": None,
            "mime_type": None,
            "owner": None,
            "shared_with_osp_group": False,
            "public": False,
            "last_modified": None,
            "error": None,
        }

        if not self.service:
            result["error"] = "Drive API not initialized"
            return False, result

        try:
            # Get file metadata
            file_metadata = self.service.files().get(
                fileId=doc_id,
                fields='id,name,mimeType,owners,permissions,lastModifiedTime,webViewLink,shared'
            ).execute()

            result["title"] = file_metadata.get("name")
            result["mime_type"] = file_metadata.get("mimeType")
            result["last_modified"] = file_metadata.get("lastModifiedTime")
            result["accessible"] = True

            # Get owner info
            owners = file_metadata.get("owners", [])
            if owners:
                result["owner"] = owners[0].get("displayName")

            # Check permissions
            permissions = file_metadata.get("permissions", [])
            for perm in permissions:
                role = perm.get("role")
                type_ = perm.get("type")
                email = perm.get("emailAddress", "")

                if type_ == "group" and "@osp" in email.lower():
                    result["shared_with_osp_group"] = True

                if type_ == "anyone":
                    result["public"] = True

            return True, result

        except HttpError as error:
            if error.resp.status == 404:
                result["error"] = "Document not found"
            elif error.resp.status == 403:
                result["error"] = "Access denied (no permission)"
            else:
                result["error"] = f"HTTP {error.resp.status}: {error.resp.reason}"
            return False, result
        except Exception as e:
            result["error"] = str(e)
            return False, result

    def scan_hubs_with_api(self):
        """Scan hubs and validate with API if available."""
        hub_files = {
            "VENDAS": "DADOS_INTELIGENCIA/VENDAS/templates/README.md",
            "CONHECIMENTO": "DADOS_INTELIGENCIA/CONHECIMENTO/solucoes/INDEX.md",
            "DADOS_INTELIGENCIA": "DADOS_INTELIGENCIA/dashboards/README.md",
            "MARKETING": "DADOS_INTELIGENCIA/MARKETING/campanhas/README.md",
        }

        docs_root = Path(__file__).parent.parent

        print("🔍 Scanning hubs and validating with API...")

        for hub_name, file_path in hub_files.items():
            full_path = docs_root / file_path
            print(f"  📄 {hub_name}...")

            if not full_path.exists():
                self.errors.append(f"File not found: {file_path}")
                continue

            try:
                content = full_path.read_text(encoding="utf-8")
                markdown_links = re.findall(
                    r'\[([^\]]+)\]\((https://docs\.google\.com/[^\)]+)\)',
                    content
                )

                hub_links = []
                for text, url in markdown_links:
                    doc_id = self.extract_doc_id(url)
                    link_data = {
                        "text": text,
                        "url": url,
                        "doc_id": doc_id,
                        "api_check": None,
                    }

                    # Check with API if available
                    if self.service and doc_id:
                        accessible, details = self.check_document_access(doc_id)
                        link_data["api_check"] = {
                            "accessible": accessible,
                            "details": details,
                        }
                        self.stats["total"] += 1
                        if accessible:
                            self.stats["accessible"] += 1
                        else:
                            self.stats["inaccessible"] += 1

                    hub_links.append(link_data)

                self.links[hub_name] = hub_links
                self.stats["by_hub"][hub_name] = {
                    "total": len(hub_links),
                    "accessible": sum(1 for l in hub_links if l.get("api_check", {}).get("accessible")),
                }

            except Exception as e:
                self.errors.append(f"Error reading {file_path}: {str(e)}")

    def generate_report(self):
        """Generate the advanced QA report."""
        report_path = Path(__file__).parent.parent / "testing" / "QA_GOOGLE_DRIVE_LINKS_ADVANCED_P6.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        report = self._build_report_content()

        try:
            report_path.write_text(report, encoding="utf-8")
            print(f"\n✅ Advanced report generated: {report_path}")
        except Exception as e:
            self.errors.append(f"Error writing report: {str(e)}")

    def _build_report_content(self) -> str:
        """Build the advanced report markdown content."""
        timestamp = datetime.now().isoformat()

        if not self.service:
            return self._build_no_api_report(timestamp)

        content = f"""# 🔍 Advanced QA Report: Google Drive API Validation - Phase 5

**Generated**: {timestamp}  
**Status**: ✅ API Validation Complete  
**API Status**: Connected ✅

---

## 📊 API Validation Summary

### Overall Statistics

| Metric | Count | Status |
|--------|-------|--------|
| **Total Links** | {self.stats["total"]} | ✅ |
| **Accessible** | {self.stats["accessible"]} | ✅ |
| **Inaccessible** | {self.stats["inaccessible"]} | {'⚠️' if self.stats["inaccessible"] > 0 else '✅'} |
| **Access Rate** | {round(100*self.stats["accessible"]/max(1, self.stats["total"]), 1)}% | {'✅ PASS' if self.stats["accessible"]/max(1, self.stats["total"]) >= 0.95 else '⚠️ WARN'} |

### By Hub

| Hub | Total | Accessible | Access Rate | Status |
|-----|-------|------------|-------------|--------|
"""
        for hub_name, stats in self.stats["by_hub"].items():
            total = stats["total"]
            accessible = stats["accessible"]
            rate = round(100 * accessible / max(1, total), 1) if total > 0 else 0
            status = "✅" if rate >= 95 else "⚠️"
            content += f"| {hub_name} | {total} | {accessible} | {rate}% | {status} |\n"

        content += f"""

---

## 📋 Detailed Permission Report

### By Hub

"""

        for hub_name in sorted(self.links.keys()):
            links = self.links.get(hub_name, [])
            if not links:
                continue

            content += f"### {hub_name}\n\n"

            for link in links:
                api_check = link.get("api_check", {})
                if not api_check:
                    continue

                accessible = api_check.get("accessible", False)
                details = api_check.get("details", {})
                status = "✅" if accessible else "❌"

                title = details.get("title", "N/A")
                owner = details.get("owner", "N/A")
                mime = details.get("mime_type", "N/A").split("/")[-1]
                shared_osp = "✅" if details.get("shared_with_osp_group") else "❌"
                public = "🌍" if details.get("public") else "🔒"
                error = details.get("error", "")

                content += f"**{link.get('text', 'Link')[:50]}** {status}\n"
                content += f"- Título: {title}\n"
                content += f"- Tipo: {mime}\n"
                content += f"- Proprietário: {owner}\n"
                content += f"- Compartilhado com @osp-group: {shared_osp}\n"
                content += f"- Acesso: {public}\n"

                if error:
                    content += f"- ⚠️ Erro: {error}\n"

                content += "\n"

        content += f"""

---

## 🔐 Security & Sharing Analysis

### OSP Group Access

| Status | Count | Recommendation |
|--------|-------|-----------------|
| ✅ Compartilhado com @osp-group | {sum(1 for hub in self.links.values() for link in hub if link.get("api_check", {}).get("details", {}).get("shared_with_osp_group"))} | Bom |
| ❌ NÃO compartilhado com @osp-group | {sum(1 for hub in self.links.values() for link in hub if not link.get("api_check", {}).get("details", {}).get("shared_with_osp_group") and link.get("api_check", {}).get("accessible"))} | Compartilhar |
| 🌍 Acesso Público | {sum(1 for hub in self.links.values() for link in hub if link.get("api_check", {}).get("details", {}).get("public"))} | Revisar segurança |

### Mime Types Distribution

"""

        mime_types = {}
        for hub_links in self.links.values():
            for link in hub_links:
                mime = link.get("api_check", {}).get("details", {}).get("mime_type", "unknown")
                if mime:
                    doc_type = mime.split(".")[-1].split("/")[-1]
                    mime_types[doc_type] = mime_types.get(doc_type, 0) + 1

        for mime_type in sorted(mime_types.keys()):
            content += f"- {mime_type}: {mime_types[mime_type]}\n"

        content += f"""

---

## ✅ Acceptance Criteria

- [{'x' if self.stats["accessible"] == self.stats["total"] else ' '}] All documents accessible via API
- [{'x' if not self.errors else ' '}] No critical errors
- [x] Permissions validated
- [x] Sharing settings reviewed
- [{'x' if self.stats["accessible"]/max(1, self.stats["total"]) >= 0.95 else ' '}] Access rate >= 95%

---

## 📝 Recommendations

"""

        # Check for issues
        inaccessible = [
            link for hub in self.links.values()
            for link in hub
            if not link.get("api_check", {}).get("accessible", True)
        ]

        if inaccessible:
            content += f"\n⚠️ **{len(inaccessible)} links com problema de acesso**\n"
            for link in inaccessible[:5]:  # Show first 5
                error = link.get("api_check", {}).get("details", {}).get("error", "unknown")
                content += f"- {link.get('text', 'Link')}: {error}\n"
            if len(inaccessible) > 5:
                content += f"- ... e mais {len(inaccessible) - 5}\n"

        not_shared_osp = [
            link for hub in self.links.values()
            for link in hub
            if link.get("api_check", {}).get("accessible", False)
            and not link.get("api_check", {}).get("details", {}).get("shared_with_osp_group", False)
        ]

        if not_shared_osp:
            content += f"\n📌 **{len(not_shared_osp)} links não compartilhados com @osp-group**\n"
            content += "Recomendação: Compartilhar com @osp-group como visualizador\n"

        content += f"""

---

## 📎 Related Files

- **Basic Validation**: \`testing/QA_GOOGLE_DRIVE_LINKS_P6.md\`
- **Audit**: \`planning/technical/GOOGLE_DRIVE_AUDIT_COMPLETE.md\`
- **Mapping**: \`planning/technical/GOOGLE_DRIVE_MAPPING_HUBS.md\`
- **Resources**: \`planning/technical/GOOGLE_DRIVE_RESOURCES_P6.md\`

---

**Report Generated**: {timestamp}  
**Validator Version**: 2.0 (with API)  
**Python Script**: \`scripts/validate_google_drive_links_api.py\`
"""
        return content

    def _build_no_api_report(self, timestamp: str) -> str:
        """Build report when API is not available."""
        return f"""# 🔍 Advanced QA Report: Google Drive Validation - Phase 5

**Generated**: {timestamp}  
**Status**: ⚠️ API Not Configured  
**API Status**: Not Connected

---

## ℹ️ API Configuration Required

To enable advanced validation with API access:

### Setup Steps:

1. **Create Google Cloud Project**
   ```
   https://console.cloud.google.com/project
   ```

2. **Enable Google Drive API**
   - Go to APIs & Services
   - Enable Google Drive API

3. **Create Service Account**
   - Create new Service Account
   - Create JSON key
   - Download credentials.json

4. **Install Dependencies**
   ```bash
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

5. **Share Drive Files**
   - Share Google Drive files with service account email
   - Grant "Viewer" or "Editor" permission

6. **Run Validation**
   ```bash
   python3 scripts/validate_google_drive_links_api.py <path-to-credentials.json>
   ```

### What This Enables:

✅ Real-time document accessibility check  
✅ Permission verification (@osp-group access)  
✅ Document metadata retrieval (title, owner, type)  
✅ Last modified date tracking  
✅ Sharing settings audit  
✅ Public vs private classification  

---

## 📝 Current Status

- Basic URL validation: ✅ Complete
- API validation: ⏳ Pending (requires credentials)
- Permissions audit: ⏳ Pending

### Temporary Workaround:

Use manual validation:
1. Clicar em alguns links aleatoriamente
2. Confirmar acesso
3. Verificar permissões no Google Drive

---

**Generated**: {timestamp}  
**Script**: \`scripts/validate_google_drive_links_api.py\`
"""

    def print_summary(self):
        """Print validation summary to console."""
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)

        if self.service:
            print(f"\nTotal Links Checked: {self.stats['total']}")
            print(f"Accessible: {self.stats['accessible']} ✅")
            print(f"Inaccessible: {self.stats['inaccessible']} ⚠️")
            if self.stats["total"] > 0:
                print(f"Access Rate: {round(100*self.stats['accessible']/self.stats['total'], 1)}%")

            print("\nBy Hub:")
            for hub_name, stats in self.stats["by_hub"].items():
                accessible = stats["accessible"]
                total = stats["total"]
                print(f"  {hub_name}: {accessible}/{total} ✅")
        else:
            print("\n⚠️  Google Drive API not initialized")
            print("Run with credentials to enable API validation:")
            print("  python3 scripts/validate_google_drive_links_api.py <credentials.json>")

        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)}")
            for error in self.errors[:3]:
                print(f"  - {error}")

        print("\n" + "=" * 60 + "\n")


def main():
    print("🔗 Google Drive Links Validator with API - Phase 5 Advanced QA\n")

    credentials_path = sys.argv[1] if len(sys.argv) > 1 else None

    validator = GoogleDriveAPIValidator(credentials_path)
    validator.scan_hubs_with_api()
    validator.generate_report()
    validator.print_summary()

    return 0


if __name__ == "__main__":
    exit(main())
