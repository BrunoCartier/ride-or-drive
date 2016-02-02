# Ride or drive?

A simple question, answered automatically every day :
- **Should I ride or drive to go to work?**

## Cron task
```
# Send weather every working day at 9:15
15 9 * * 1-5 /opt/ride-or-drive/ride_or_drive.py >/dev/null 2>&1
```
