# 🎨 Designer · Design System
## KidVenture · v1.0

> **I am the Designer.** My job is to make this product look good, feel easy, and carry emotion. For a family product, the vibe should be: **warm, trustworthy, and fun** — not cold or corporate.

---

## 1. Brand Identity

### Design Pillars
> **"No more guessing where to take the kids."**

Three keywords: **Warm** · **Playful** · **Precise**

- **Warm**: Colors, illustrations, and copy should feel like family, not a database
- **Playful**: Tasteful use of color and motion to reflect the joy of play
- **Precise**: Clear information hierarchy — parents should find what they need in 10 seconds

---

## 2. Color System

### Primary Palette

| Name | HEX | Usage |
|------|-----|-------|
| Sunset Orange (brand) | `#FF6B35` | CTAs, key badges, logo accent |
| Golden Yellow | `#FFB800` | Stars, rating highlights |
| Nature Green | `#52C41A` | Open status, outdoor tags |
| Sky Blue | `#1890FF` | Navigation, links, indoor tags |

### Neutrals

| Name | HEX | Usage |
|------|-----|-------|
| Primary text | `#1A1A1A` | Headings, important info |
| Secondary text | `#666666` | Subtitles, descriptions |
| Hint text | `#999999` | Placeholders, disabled |
| Divider | `#F0F0F0` | Card borders, list separators |
| Page background | `#F7F8FA` | Page bg |
| Card background | `#FFFFFF` | Cards |

### Age Tier Colors (for badges)

| Age Tier | Background | Text | Feeling |
|----------|-----------|------|---------|
| Baby (0–1) | `#FFF0F6` | `#C41D7F` | Soft pink |
| Toddler (2–3) | `#FFF7E6` | `#D46B08` | Warm orange |
| Preschool (4–6) | `#F0F5FF` | `#2F54EB` | Curious blue |
| School Age (7–12) | `#F6FFED` | `#389E0D` | Energetic green |

---

## 3. Typography

### Font Stack

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Type Scale

| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Display | 28px | Bold 700 | 1.3 | Page titles |
| H1 | 22px | Bold 700 | 1.4 | Venue name (detail) |
| H2 | 18px | Semibold 600 | 1.4 | Card title, section header |
| H3 | 16px | Medium 500 | 1.5 | Subtitle, label |
| Body | 14px | Regular 400 | 1.6 | Descriptions, reviews |
| Caption | 12px | Regular 400 | 1.5 | Distance, time, meta |
| Micro | 10px | Regular 400 | 1.4 | Fine print (use sparingly) |

---

## 4. Spacing (8px base unit)

```
4px   – tight (icon-to-text)
8px   – small (badge padding)
12px  – base (within cards)
16px  – standard (page padding, card gaps)
24px  – large (section spacing)
32px  – xl (page top padding)
```

---

## 5. Component Specs

### 5.1 Venue Card

```
┌──────────────────────────────────────────────┐  ← rounded-xl, shadow-sm
│ [Photo 343×160px, rounded-lg, object-cover]  │
│                                    [💾]       │  ← bookmark button 28×28
├──────────────────────────────────────────────┤
│ Bay Area Discovery Museum                     │  ← H2 18px Bold
│ [🏛️ Museum] [Ages 2–8] ⭐ 4.7 (382)          │  ← badges + rating
│ 📍 Sausalito  ·  2.3 mi away                 │  ← caption 12px
│ Open today 9 AM – 5 PM  ✅                   │  ← green open indicator
│ 🅿️ Free parking · ♿ Stroller OK              │  ← amenity tags
└──────────────────────────────────────────────┘
```

### 5.2 Age Picker

```
┌──────────────────────────────────────────────┐
│  Child's Age                                  │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │
│  │  🍼  │ │  🐣  │ │  🎨  │ │  🚴  │        │
│  │ Baby │ │Toddler│ │Preschool│ │School │    │
│  │ 0–1  │ │ 2–3  │ │ 4–6  │ │ 7–12 │        │
│  └──────┘ └──────┘ └──────┘ └──────┘        │
└──────────────────────────────────────────────┘
```

Selected: `#FF6B35` bg, white text, slight scale-up animation

### 5.3 Age Match Badge

```
[✅ Perfect fit]    → green bg, white text (90–100 score)
[👍 Good fit]       → orange bg, white text (70–89)
[⚠️ Okay fit]      → yellow bg, dark text (50–69)
```

### 5.4 Buttons

| Type | Height | Radius | Color |
|------|--------|--------|-------|
| Primary | 48px | 24px | `#FF6B35` orange |
| Secondary | 44px | 22px | White + orange border |
| Ghost | 40px | 20px | No border, orange text |
| Navigate | 52px | 16px | `#1890FF` blue |

---

## 6. Iconography & Illustrations

### Icons
- Style: Lucide linear icons
- Sizes: 16px / 20px / 24px
- Color: Primary text or brand color, max 2 colors

### Category Icons

| Category | Icon |
|----------|------|
| Indoor Play | 🎡 |
| Museum / Science | 🏛️ |
| Park / Nature | 🌿 |
| Restaurant | 🍽️ |
| Library | 📚 |
| Sports / Active | ⛹️ |
| Farm / Animals | 🌻 |
| Swimming / Water | 🏊 |
| Playground | 🛝 |

### Empty States
- No results: Cartoon bear scratching head, "No matches found. Try a different area or age?"
- Empty favorites: Cartoon kid peeking, "No favorites yet — start exploring!"

---

## 7. Motion Guidelines

| Type | Duration | Easing |
|------|----------|--------|
| Page transition | 250ms | ease-in-out |
| Card appear (list) | 300ms | ease-out (stagger 50ms) |
| Button press | 100ms | linear |
| Filter toggle | 200ms | ease |
| Modal popup | 300ms | spring (0.34, 1.56, 0.64, 1) |

**Rule: Animations must have purpose. No animation during slow loading.**

---

## 8. Mobile Responsiveness

- Minimum viewport: **375px** (iPhone SE)
- Design at: **390px** (iPhone 14)
- Bottom safe area: account for iOS Home Indicator (34px)
- Touch targets: minimum **44×44px** (Apple HIG)
- Support Dynamic Type (accessibility)

---

## 9. Design Tools & Handoff

| Tool | Purpose |
|------|---------|
| Figma | Primary design tool (components + prototypes) |
| shadcn/ui Figma kit | Reference for component mapping |

### Handoff Standards
1. Every page: mobile (390px) + desktop (1440px)
2. Complete states: default, loading, empty, error
3. Assets: 2x export, SVG (icons) + WebP (photos)
4. All reusable components as Figma Components

---

*Designer Log: pending...*
