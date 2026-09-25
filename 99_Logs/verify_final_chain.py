import json
import pandas as pd

import json
import traceback

OUT = r"D:\humanbrain\humanbrain\99_Logs\verify_final.out"
lines = []
try:
    B = r"D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS"
    e = json.load(open(B + r"\04_CIS\e05_statistics.json"))
    k = e["system_enrichment"]["K"]["50"]
    lines.append("K=50 observed: %s" % k["observed"])
    for name, v in k["systems"].items():
        lines.append("   %-8s z_B=%7.2f  p_B=%.4g  enr_B=%.2f"
                     % (name, v["z_B"], v["p_B"], v["enrichment_B"]))
    lines.append("battery_b: %s" % e["battery_b"])
    lines.append("rank_stability: %s" % e["rank_stability"])
except Exception:
    lines.append(traceback.format_exc())

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
