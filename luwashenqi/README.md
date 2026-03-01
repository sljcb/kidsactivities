# 🐣 KidVenture

> Discover the best kid-friendly places in the Bay Area, filtered by your child's age.

## Project Structure

```
kidventure/
├── apps/
│   ├── web/          # Next.js 14 (Web)
│   └── mobile/       # Expo React Native (App)
├── packages/
│   ├── types/        # Shared TypeScript types
│   ├── api-client/   # Shared API hooks
│   └── ui/           # Shared UI components
├── backend/          # FastAPI + data ingestion pipeline
└── docs/             # Team design docs (see parent directory)
```

## Quick Start

### Web

```bash
pnpm install
pnpm dev:web
# http://localhost:3000
```

### Backend API

```bash
cd backend
cp .env.example .env   # Fill in your API keys
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://localhost:8000/docs
```

### Mobile App

```bash
cd apps/mobile
pnpm install
pnpm start             # Scan QR with Expo Go
```

## Environment Variables

See `backend/.env.example`:
- Supabase URL + Key (database)
- Upstash Redis (cache)
- Google Places API Key
- Yelp Fusion API Key

## Design Docs

See parent directory:
- `00_AI_Manager.md` — Project overview
- `01_PM_PRD.md` — Product requirements
- `02_BE_Architecture.md` — Backend architecture
- `03_FE_Architecture.md` — Frontend architecture
- `04_Designer_Spec.md` — Design system
- `05_Test_Plan.md` — Test plan
