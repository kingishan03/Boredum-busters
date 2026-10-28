Daily website automation

The Windows scheduled task "Boredom-Busters Daily Website" publishes one offline mini app each day at midnight. The first run is scheduled for the next midnight. If the computer is off at that time, Windows will run the missed task when it is available again.

The computer must be on and the Windows account signed in. No API key, external service, or Python package is required; the generator uses Python's standard library.

The generated site is added to the homepage gallery and websbase.txt. Generated pages are stored under daily-apps/sites, and daily-apps/state.json tracks the last run.

To stop future additions, run daily-apps\remove_daily_task.ps1 in PowerShell. Existing generated websites are left in place.
