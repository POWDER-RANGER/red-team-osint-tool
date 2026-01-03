from __future__ import annotations

import logging
from typing import Callable
from apscheduler.schedulers.background import BackgroundScheduler

log = logging.getLogger("osinttool")

class JobRunner:
    """Run jobs at intervals using APScheduler."""

    def __init__(self) -> None:
        # Initialize the background scheduler with UTC timezone
        self.sched = BackgroundScheduler(timezone="UTC")

    def add_interval_job(self, func: Callable[[], None], seconds: int, job_id: str) -> None:
        """Schedule a function to run every ``seconds`` seconds.

        If a job with the same ``job_id`` exists it will be replaced.
        """
        self.sched.add_job(func, "interval", seconds=int(seconds), id=job_id, replace_existing=True)

    def start(self) -> None:
        """Start the scheduler."""
        self.sched.start()
        log.info("Scheduler started.")

    def shutdown(self) -> None:
        """Stop the scheduler without waiting for jobs to finish."""
        self.sched.shutdown(wait=False)
        log.info("Scheduler stopped.")
