import json

# Define initial settings (replace with your desired defaults)
bakeTempSetting = 350  # Example temperature in Fahrenheit
bakeTimeSetting = 20   # Example time in minutes

warmTempSetting = 150  # Example temperature in Fahrenheit
warmTimeSetting = 30   # Example time in minutes

# Create the bakeSettings.json file
bakeSettings = {"temp": bakeTempSetting, "time": bakeTimeSetting}
with open("bakeSettings.json", "w") as outfile:
    json.dump(bakeSettings, outfile)

# Create the warmSettings.json file
warmSettings = {"temp": warmTempSetting, "time": warmTimeSetting}
with open("warmSettings.json", "w") as outfile:
    json.dump(warmSettings, outfile)

print("JSON files created successfully!")
