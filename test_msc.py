from carriers.msc import MSCSchedule

engine = MSCSchedule()

results = engine.search_schedule(
    "Karachi",
    "Jebel Ali"
)

print(results)