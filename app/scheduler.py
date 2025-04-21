from apscheduler.schedulers.background import BackgroundScheduler
from app.services.match_updater import process_matches

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_matches, 'interval', minutes=5)
    scheduler.start()