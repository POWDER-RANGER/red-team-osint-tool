import argparse

from osinttool.cli import run_once, run_daemon, show_recent
from osinttool.config import load_config


def main() -> None:
    """Entrypoint for the red-team OSINT tool CLI."""
    parser = argparse.ArgumentParser(prog="red-team-osint-tool")
    parser.add_argument("--config", default="config.yml", help="Path to configuration file")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    subparsers.add_parser("once", help="Run all sources once and exit")
    subparsers.add_parser("daemon", help="Run sources on intervals as a daemon")
    recent_parser = subparsers.add_parser("recent", help="Show recent evidence records")
    recent_parser.add_argument("--limit", type=int, default=25, help="Number of records to display")

    args = parser.parse_args()

    if args.cmd == "once":
        run_once(args.config)
    elif args.cmd == "daemon":
        run_daemon(args.config)
    elif args.cmd == "recent":
        cfg = load_config(args.config)
        show_recent(cfg.app.db_path, args.limit)


if __name__ == "__main__":
    main()
