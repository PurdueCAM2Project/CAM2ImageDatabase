from crontab import CronTab

cron = CronTab()

job = cron.new(command='python image_retrieval.py')
job.every(1).month  # can change according to requirement (hours, week, month, etc.)

cron.write()
print("Job created")

