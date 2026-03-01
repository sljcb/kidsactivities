# 🤖 AI Manager · KidVenture Project Overview

> **I am the AI Manager for this project.** I coordinate all roles, align deliverables, flag risks, and keep everyone in sync.

---

## 1. Product One-Liner

> **KidVenture** — Helps Bay Area parents discover the best kid-friendly places, filtered by child's age and neighborhood. No more guessing.

---

## 2. Team Roles & Deliverables

| Role | Responsibility | Key Deliverables | Document |
|------|---------------|-----------------|----------|
| **PM** | Requirements, user stories, priorities | PRD, user journey | `01_PM_PRD.md` |
| **BE** | Server, API, data scraping, database | Architecture, API spec | `02_BE_Architecture.md` |
| **FE** | Web + App implementation | Tech stack, component spec | `03_FE_Architecture.md` |
| **Designer** | Visual style, UX design | Design system, component guide | `04_Designer_Spec.md` |
| **Test** | Quality assurance, test cases | Test plan, bug severity spec | `05_Test_Plan.md` |

---

## 3. Project Milestones

```
Week 1–2   ▶ Requirements freeze + tech stack confirmed (PM + BE + FE)
Week 3–4   ▶ Design v1 + Data scraping PoC (Designer + BE)
Week 5–8   ▶ MVP sprint (BE + FE in parallel)
Week 9     ▶ Beta testing + regression (Test)
Week 10    ▶ Bug fixes + soft launch (all hands)
Week 11+   ▶ Data ops + iteration
```

---

## 4. Key Risks & Mitigation

| Risk | Level | Mitigation |
|------|-------|-----------|
| Google Places API cost overrun | 🔴 High | Cache aggressively, use Yelp Fusion as supplement, monitor quota daily |
| Yelp scraping TOS issues | 🟠 Med | Use official Yelp Fusion API (free tier: 5000 calls/day) |
| Data quality (stale hours/prices) | 🟠 Med | Weekly refresh + user correction mechanism |
| App Store rejection (iOS) | 🟠 Med | Prepare compliance materials 2 weeks ahead |
| COPPA / children's privacy | 🔴 High | Do NOT collect data from children; only parents use the app; no tracking of minors |
| Solo dev resource constraint | 🟠 Med | MVP = web only, App deferred to v1.1 |

---

## 5. Core Technical Decisions (AI Manager Rulings)

1. **Data Sources**: Google Places API (primary) + Yelp Fusion API (reviews) + manual curation
2. **MVP Form**: Mobile-first responsive web (Next.js), React Native App in Phase 2
3. **Age Tiers**: 0–1 yr, 2–3 yr, 4–6 yr, 7–12 yr (4 tiers, extensible)
4. **Geography**: Bay Area → City → Neighborhood (SF, San Jose, Oakland, Palo Alto, Fremont, Mountain View, Berkeley, Cupertino, Sunnyvale, Santa Clara, etc.)
5. **Recommendation Engine**: v1 rule-based scoring, v2 LLM personalization
6. **Language**: English primary, Chinese (Simplified) as stretch goal (large Chinese parent community in Bay Area)

---

## 6. Sprint #1 Assignments

- **PM**: Complete 5 parent interviews, output Top 10 user stories
- **BE**: Google Places API PoC, validate data for Bay Area kids venues
- **FE**: Scaffold Next.js project, integrate Google Maps
- **Designer**: Low-fi wireframes (home + venue detail)
- **Test**: Draft test strategy, define regression scope

---

## 7. Communication Protocol

- Daily async standup: Each role appends to their doc's log section
- Blocked items: Mark `🚨 BLOCKED` at top of doc, AI Manager responds within 24h
- Versioning: `v0.x` = internal, `v1.0` = public launch

---

*AI Manager is always online. Ready to sync.*
