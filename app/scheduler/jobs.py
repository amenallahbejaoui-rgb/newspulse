
from apscheduler.schedulers.background import BackgroundScheduler

from ..pipeline import run_pipeline


scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(
        run_pipeline,
        "interval",
        minutes=30,
        id="newspulse_pipeline",
        replace_existing=True,
    )

    scheduler.start()

    print("NewsPulse scheduler started")
    print("Pipeline will run every 30 minutes")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("NewsPulse scheduler stopped")
