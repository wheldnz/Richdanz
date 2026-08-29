# CLAUDE.md - Data Analyst & BI Portfolio Guidelines

This document provides context, coding standards, UI/UX directives, and BigQuery integration details for Claude when working on this project repository.

---

## 🚀 Project Overview & Objectives

- **Repository**: `wheldnz/richdanz` (GitHub)
- **Goal**: High-impact Data Analyst, BI, and Data Engineering Portfolio Web Application featuring 6 enterprise-grade projects and a modern UI/UX interface.
- **Current Development Focus**:
  1. **UI/UX Enhancement**: Redesign and elevate the visual aesthetics, interactive dashboards, case study presentations, micro-animations, and mobile responsiveness.
  2. **Data Integration**: Connect live BigQuery datasets, SQL query playgrounds, and interactive metric cards into the web interface.
  3. **Performance & Code Quality**: Ensure clean Next.js App Router component architecture and TypeScript safety.

---

## 🛠️ Tech Stack & Commands

| Component | Technology |
| :--- | :--- |
| **Framework** | Next.js 16 (App Router) |
| **UI & Styling** | React 19, Tailwind CSS v4, PostCSS |
| **Animations & 3D** | Framer Motion 12, Three.js (`@react-three/fiber`, `@react-three/drei`) |
| **Icons & Utilities** | `lucide-react`, `marked`, `gray-matter` |
| **Data Warehouse & DB** | Google Cloud BigQuery, PostgreSQL/MySQL compatibility, dbt |
| **Language** | TypeScript 5 (Strict mode) |

### Key Commands
```bash
# Development server (http://localhost:3000)
npm run dev

# Production build check
npm run build

# Production server start
npm run start

# Code linting
npm run lint
```

---

## 📊 BigQuery Credentials & Connection Details

Claude can query or connect to BigQuery using the embedded GCP Service Account key located in this repository.

### GCP Credentials
- **GCP Project ID**: `electracare-dw`
- **Service Account Email**: `airflow-bigquery-sa@electracare-dw.iam.gserviceaccount.com`
- **Key File Path (Relative)**: `./electracare-dw/keys/gcp_key.json`
- **Key File Path (Absolute Windows)**: `c:\Users\USER\Documents\present\potrfolio\electracare-dw\keys\gcp_key.json`
- **Alternative Key File**: `./electracare-dw/electracare-dw-42556543e741.json`

### 1. Claude MCP (Model Context Protocol) Integration Setup
To enable Claude (Claude Desktop / Claude Code) to directly read BigQuery schemas and execute SQL queries, use the following MCP configuration:

```json
{
  "mcpServers": {
    "bigquery": {
      "command": "npx",
      "args": ["-y", "@bytebury/mcp-bigquery"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "./electracare-dw/keys/gcp_key.json",
        "BIGQUERY_PROJECT_ID": "electracare-dw"
      }
    }
  }
}
```

### 2. Node.js / Next.js SDK Integration
When creating API routes in Next.js (`src/app/api/...`), use `@google-cloud/bigquery`:
```typescript
import { BigQuery } from '@google-cloud/bigquery';
import path from 'path';

const bigquery = new BigQuery({
  projectId: 'electracare-dw',
  keyFilename: path.join(process.cwd(), 'electracare-dw', 'keys', 'gcp_key.json'),
});
```

---

## 🎨 UI/UX & Design Guidelines

1. **Aesthetics & Theme**:
   - Modern dark mode / tech-forward palette with high contrast metric displays.
   - Clean typography, glassmorphism cards, subtle gradient borders, and crisp charts.
2. **Interactive Case Studies**:
   - Show business problem, dataset architecture, ERD/Star Schema, SQL queries, DAX formulas, Power BI/web dashboards, and executive insights.
3. **Component Structure**:
   - `src/app/` - Page routes (Next.js App Router).
   - `src/components/` - Reusable UI components (hero, cards, charts, project modals, navbar, footer).
   - `src/lib/` - Utilities and BigQuery/database clients.
4. **Icons & Animations**:
   - Always use `lucide-react` for UI icons.
   - Use `framer-motion` for smooth layout transitions and scroll-triggered animations.

---

## 📁 Repository Structure Map

```text
potrfolio/
├── CLAUDE.md                           # Guidelines & BigQuery context for Claude
├── Data_Analyst_Portfolio_Master_PRD.md # Master specifications document
├── electracare-dw/                     # Enterprise Data Warehouse (dbt, BigQuery & Airflow)
│   └── keys/gcp_key.json               # BigQuery Service Account credentials
├── project-04-ecommerce-insurtech-bi/  # TokoAman.id E-Commerce & Insurtech BI Project
├── src/                                # Next.js 16 Web Portfolio App
│   ├── app/                            # App Router Pages & API Routes
│   ├── components/                     # React UI Components
│   └── lib/                            # Helper utilities
└── public/                             # Public static assets
```

---

## ⚠️ Important Rules for Claude
- **Preserve Existing Functionality**: Do not break existing components or remove existing project case studies.
- **Responsive First**: Ensure all UI edits look great on desktop, tablet, and mobile views.
- **Credentials Security**: Do not push production keys or secret environment variables to public repos without verifying `.gitignore`.
