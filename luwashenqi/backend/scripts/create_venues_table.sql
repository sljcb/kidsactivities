-- KidVenture: venues table
-- Run this in Supabase SQL Editor → New Query

CREATE TABLE IF NOT EXISTS venues (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name              VARCHAR(200) NOT NULL,
    city              VARCHAR(50)  NOT NULL,
    neighborhood      VARCHAR(100),
    region            VARCHAR(50)  CHECK (region IN ('sf', 'peninsula', 'south_bay', 'east_bay', 'north_bay')),
    address           TEXT,
    lat               FLOAT        CHECK (lat  BETWEEN 37.0 AND 38.5),
    lng               FLOAT        CHECK (lng  BETWEEN -123.0 AND -121.0),
    category          VARCHAR(50),
    venue_type        VARCHAR(20)  DEFAULT 'outdoor' CHECK (venue_type IN ('indoor', 'outdoor', 'both')),
    min_age_months    INTEGER      NOT NULL DEFAULT 0   CHECK (min_age_months BETWEEN 0 AND 200),
    max_age_months    INTEGER      NOT NULL DEFAULT 144 CHECK (max_age_months BETWEEN 0 AND 200),
    age_note          TEXT,
    hours             JSONB,       -- e.g. {"monday": "9am-5pm", "default": "9am-6pm"}
    admission         JSONB,       -- e.g. {"child": 15.00, "adult": 20.00}
    phone             VARCHAR(30),
    website           TEXT,
    images            JSONB        DEFAULT '[]',
    rating            FLOAT        CHECK (rating BETWEEN 0 AND 5),
    review_count      INTEGER      DEFAULT 0,
    google_place_id   VARCHAR(255) UNIQUE,
    yelp_id           VARCHAR(255),
    parking_info      TEXT,
    stroller_friendly BOOLEAN      DEFAULT true,
    has_restrooms     BOOLEAN      DEFAULT true,
    data_source       VARCHAR(20)  DEFAULT 'manual' CHECK (data_source IN ('mock', 'google_places', 'yelp', 'manual')),
    is_active         BOOLEAN      DEFAULT true,
    created_at        TIMESTAMPTZ  DEFAULT now(),
    updated_at        TIMESTAMPTZ  DEFAULT now()
);

-- Indexes for fast filtering
CREATE INDEX IF NOT EXISTS idx_venues_is_active   ON venues (is_active);
CREATE INDEX IF NOT EXISTS idx_venues_region       ON venues (region)   WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_venues_category     ON venues (category) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_venues_city         ON venues (city)     WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_venues_coords       ON venues (lat, lng) WHERE is_active = true;

-- Auto-update updated_at on row change
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER venues_updated_at
    BEFORE UPDATE ON venues
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
