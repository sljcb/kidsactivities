# 🧪 Test · Test Plan
## KidVenture · v1.0

> **I am the Test Engineer.** My job is to catch bugs before they reach users. With limited solo-dev resources, I focus on **keeping core flows alive** using a **risk-priority** test strategy.

---

## 1. Strategy Overview

### Test Pyramid

```
        /\
       /E2E\          Automated E2E (3 core flows)
      /──────\
     / Integr. \      API endpoint tests (all endpoints)
    /────────────\
   /   Unit Tests  \   Core business logic functions
  /────────────────\
```

### Priority Matrix

| Priority | Scenario | Strategy |
|----------|----------|----------|
| P0 🔴 | Core recommendation flow | Must pass before every deploy |
| P1 🟠 | Favorites, detail page, navigation | Regression before each release |
| P2 🟡 | Corrections, secondary filters | Weekly regression |
| P3 ⚪ | Edge cases, extreme data | Monthly or ad-hoc |

---

## 2. Test Cases

### TC-01 Home Recommendation (P0)

| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| TC-01-01 | Normal recommendation | Select age "3 yr" + city "San Francisco", search | Returns ≥ 1 venue, cards fully populated |
| TC-01-02 | Multi-child switch | Add 2 children, toggle between them | List refreshes, age badge updates |
| TC-01-03 | No results fallback | Select remote area + extreme age (0 months) | Empty state illustration, no crash |
| TC-01-04 | Age boundary | Test 0, 1, 143, 144 months | All return valid results, no error |
| TC-01-05 | Stacked filters | "Indoor" + "Within 5 mi" simultaneously | Results correctly filtered |
| TC-01-06 | Weather filter | Toggle "Indoor" on rainy day | Only indoor venues shown |

### TC-02 Venue Detail (P0)

| ID | Scenario | Expected |
|----|----------|----------|
| TC-02-01 | Detail completeness | Name/address/hours/admission/age note all rendered |
| TC-02-02 | Hours accuracy | Open/closed badge matches current time |
| TC-02-03 | Navigate tap | Opens Google Maps / Apple Maps with correct coordinates |
| TC-02-04 | Image load failure | Shows placeholder image, no blank screen |
| TC-02-05 | Parking & stroller info | Displays parking and stroller accessibility tags |

### TC-03 Location & Region (P1)

| ID | Scenario | Expected |
|----|----------|----------|
| TC-03-01 | GPS success | Auto-detects city/region, shows "X mi away" |
| TC-03-02 | GPS denied | Falls back to manual city picker, no error |
| TC-03-03 | Manual city select | Selecting "Oakland" updates recommendations |
| TC-03-04 | Region filter | "South Bay" shows San Jose, Cupertino, etc. |
| TC-03-05 | GPS timeout (>10s) | Timeout message, manual selection prompt |

### TC-04 Favorites (P1)

| ID | Scenario | Expected |
|----|----------|----------|
| TC-04-01 | Add favorite | Tap 💾, icon fills orange, appears in favorites list |
| TC-04-02 | Remove favorite | Tap again, icon grays, removed from list |
| TC-04-03 | Not logged in | Prompt login, no crash |
| TC-04-04 | Favorites order | Most recently added first |

### TC-05 User Corrections (P2)

| ID | Scenario | Expected |
|----|----------|----------|
| TC-05-01 | Submit correction | Fill and submit, shows "Thanks for the feedback!" |
| TC-05-02 | Empty field | Validation error, cannot submit |
| TC-05-03 | Duplicate submission | Shows "You've already submitted this correction" |

---

### 2.2 API Tests (Integration)

#### `GET /v1/venues/recommend`

```
✅ Valid params → 200 + correct data structure
✅ Missing required (child_age) → 400 + clear error
✅ Negative age / age > 200 → 400
✅ Invalid city → 404 or empty list
✅ page=0 or page_size>50 → 400
✅ Pagination: page=2 has no overlap with page=1
✅ lat/lng valid → results sorted by distance
✅ lat/lng out of Bay Area range → 400
✅ Response time < 1000ms (p95)
✅ free_only=true → all results have $0 child admission
```

#### `GET /v1/venues/{id}`

```
✅ Valid UUID → 200 + full data
✅ Non-existent UUID → 404
✅ Invalid ID format → 400
✅ is_active=false venue → 404
```

---

### 2.3 Data Quality Tests (P1)

```
After each data ingestion run:

Completeness:
□ name is non-empty, length 1–200
□ lat/lng within Bay Area bounds (lat: 37.0–38.0, lng: -122.7–-121.5)
□ min_age_months <= max_age_months
□ rating 0.0–5.0
□ images URLs return HTTP 200

Freshness:
□ Every venue's updated_at is within last 8 days (alert if older)

Deduplication:
□ No duplicate google_place_id entries
□ Same name + same coords (within 100m) triggers merge alert
```

---

### 2.4 Performance Tests (P1)

| Test | Tool | Target |
|------|------|--------|
| API concurrency | k6 | 50 concurrent, p95 < 800ms |
| First load | Lighthouse | LCP < 2.5s (mobile 4G) |
| Image loading | Chrome DevTools | All lazy-loaded, no blocking |
| DB queries | EXPLAIN ANALYZE | No full table scans in recommend |

---

### 2.5 Compatibility (P2)

| Dimension | Coverage |
|-----------|----------|
| Browsers | Chrome 100+, Safari 15+, Firefox 110+ |
| iOS | iOS 16+ (iPhone SE, 14, 15) |
| Android | Android 12+ (Pixel, Samsung Galaxy) |
| Viewports | 375px, 390px, 768px (tablet), 1440px |

---

### 2.6 Security Tests (P1)

```
□ SQL injection: inject in city/neighborhood params → blocked
□ XSS: inject script in correction field → escaped
□ Unauthorized: no token → 401 on favorites
□ Privilege escalation: user A token for user B favorites → 403
□ Rate limit: same IP > 100/min → 429
□ Location data: not persisted in DB
□ COPPA: no child PII collected or stored
```

---

## 3. Release Quality Gate

Before any release, ALL of these must be green:

```
✅ P0 test cases: 100% pass
✅ P1 test cases: 95%+ pass
✅ Zero Severity 1 bugs (crash / data loss)
✅ API coverage: 100%
✅ Performance: recommend API p95 < 800ms
✅ iOS + Android smoke test pass
✅ Security: no high-severity vulnerabilities
✅ Lighthouse mobile score ≥ 75
```

---

## 4. Bug Severity

| Severity | Definition | Response Time |
|----------|-----------|---------------|
| **S1** 🔴 | Core flow crash, data loss, unusable | Fix within 2 hours |
| **S2** 🟠 | Feature broken, workaround exists | Fix same day |
| **S3** 🟡 | UX issue, core not affected | Fix in next release |
| **S4** ⚪ | Visual / copy nit | Batch fix |

---

## 5. Test Tooling

| Purpose | Tool |
|---------|------|
| Unit tests | Vitest (FE) / pytest (BE) |
| E2E | Playwright (Web) |
| API tests | httpx + pytest / Postman |
| Performance | k6 |
| Mobile automation | Detox (Expo) |
| Bug tracking | GitHub Issues + custom labels |
| Data quality | Python scripts + scheduled alerts |

---

*Test Log: pending...*
