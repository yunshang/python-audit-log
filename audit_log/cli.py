import argparse
from audit_log import run_specific_migration

def main():
    parser = argparse.ArgumentParser(description="Audit Log Management")
    parser.add_argument(
        '--run-migration',
        type=str,
        help='Run a specific migration by revision ID'
    )
    
    args = parser.parse_args()

    if args.run_migration:
        run_specific_migration(args.run_migration)
    
if __name__ == "__main__":
    main()