from utils.config import Config

cfg = Config()

print("Theme:", cfg.get("theme"))
print("Output:", cfg.get("output_folder"))