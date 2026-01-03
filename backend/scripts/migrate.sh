#!/bin/bash
#
# Database Migration Helper Script
#
# Usage:
#   ./scripts/migrate.sh upgrade    # Apply all pending migrations
#   ./scripts/migrate.sh downgrade  # Rollback last migration
#   ./scripts/migrate.sh status     # Show current migration status
#   ./scripts/migrate.sh history    # Show migration history
#   ./scripts/migrate.sh reset      # Reset database (DANGEROUS - dev only!)
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}Warning: Virtual environment not activated${NC}"
    echo "Activating venv..."
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create .env file with DATABASE_URL"
    exit 1
fi

# Load DATABASE_URL from .env
export $(grep -v '^#' .env | grep DATABASE_URL | xargs)

if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}Error: DATABASE_URL not set in .env${NC}"
    exit 1
fi

echo -e "${GREEN}Using database:${NC} ${DATABASE_URL%%@*}@***"

# Main command switch
case "$1" in
    upgrade)
        echo -e "${GREEN}Applying migrations...${NC}"
        alembic upgrade head
        echo -e "${GREEN}Migrations applied successfully!${NC}"
        ;;
    
    downgrade)
        echo -e "${YELLOW}Rolling back last migration...${NC}"
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            alembic downgrade -1
            echo -e "${GREEN}Rollback complete${NC}"
        else
            echo "Cancelled"
        fi
        ;;
    
    status)
        echo -e "${GREEN}Current migration status:${NC}"
        alembic current
        echo ""
        echo -e "${GREEN}Pending migrations:${NC}"
        alembic heads
        ;;
    
    history)
        echo -e "${GREEN}Migration history:${NC}"
        alembic history --verbose
        ;;
    
    reset)
        echo -e "${RED}WARNING: This will DROP all tables and data!${NC}"
        echo -e "${YELLOW}This should ONLY be used in development${NC}"
        read -p "Are you ABSOLUTELY sure? Type 'yes' to confirm: " confirm
        if [ "$confirm" = "yes" ]; then
            echo -e "${YELLOW}Downgrading to base...${NC}"
            alembic downgrade base
            echo -e "${GREEN}Upgrading to head...${NC}"
            alembic upgrade head
            echo -e "${GREEN}Database reset complete${NC}"
        else
            echo "Cancelled"
        fi
        ;;
    
    create)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Migration name required${NC}"
            echo "Usage: ./scripts/migrate.sh create <migration_name>"
            exit 1
        fi
        echo -e "${GREEN}Creating new migration: $2${NC}"
        alembic revision --autogenerate -m "$2"
        echo -e "${YELLOW}Please review the generated migration file before applying!${NC}"
        ;;
    
    *)
        echo "Usage: $0 {upgrade|downgrade|status|history|reset|create}"
        echo ""
        echo "Commands:"
        echo "  upgrade    - Apply all pending migrations"
        echo "  downgrade  - Rollback last migration"
        echo "  status     - Show current migration status"
        echo "  history    - Show migration history"
        echo "  reset      - Reset database (dev only!)"
        echo "  create     - Create new migration"
        exit 1
        ;;
esac
