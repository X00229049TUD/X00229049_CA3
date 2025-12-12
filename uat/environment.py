import os
from datetime import datetime

def after_step(context, step):
    if step.status == "failed":
        if hasattr(context, "driver"):
            os.makedirs("uat/screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"uat/screenshots/{step.name}_{timestamp}.png"
            context.driver.save_screenshot(filename)

def after_all(context):
    if hasattr(context, "driver"):
        context.driver.quit()