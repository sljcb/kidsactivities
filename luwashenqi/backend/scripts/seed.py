#!/usr/bin/env python3
"""
KidVenture · Database Seed Script
Fetches 50–100 Bay Area kids activity venues from Google Places + Yelp
and writes them to Supabase.

Usage:
    python scripts/seed.py              # Fetch and write to Supabase
    python scripts/seed.py --dry-run    # Print results, skip DB write
    python scripts/seed.py --limit 50  # Cap at 50 venues
"""
import sys
import asyncio
import argparse
from pathlib import Path

# Allow imports from the backend app package
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from loguru import logger
from app.crawlers.dianping_spider import ingest_bay_area


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed KidVenture venue database")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch venues but skip writing to Supabase",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Maximum number of venues to write (default: no limit)",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    logger.info("=" * 50)
    logger.info("KidVenture Venue Seeder")
    logger.info(f"  dry_run : {args.dry_run}")
    logger.info(f"  limit   : {args.limit or 'none'}")
    logger.info("=" * 50)

    venues = await ingest_bay_area(dry_run=args.dry_run, limit=args.limit)

    logger.info("=" * 50)
    logger.info(f"Done. {len(venues)} venues processed.")
    if args.dry_run:
        logger.info("(DRY RUN — nothing written to Supabase)")
        for i, v in enumerate(venues, 1):
            logger.info(
                f"  {i:3}. [{v.get('region','?'):10}] {v.get('name','')[:40]:40} "
                f"cat={v.get('category','?'):12} "
                f"age={v.get('min_age_months',0)}-{v.get('max_age_months',144)}mo "
                f"rating={v.get('rating') or '-'}"
            )
    logger.info("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
