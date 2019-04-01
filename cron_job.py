from crontab import CronTab

cron = CronTab()

job = cron.new(command='python image_retrieval.py')
job.minute.every(1)  # can change according to requirement (hours, week, month, etc.)

cron.write()
print("Job created")

for job in cron:
    print(job)

cron.remove(job)
print("Job removed")

for job in cron:
    print(job)
