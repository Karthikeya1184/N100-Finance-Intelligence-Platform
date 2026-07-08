import pandas as pd

from src.screener.presets import PresetScreeners
from src.screener.scoring import CompositeScorer
from src.screener.exporter import ScreenerExporter


screen = PresetScreeners()

score = CompositeScorer()

presets = {

    "Quality Compounder": screen.quality_compounder(),

    "Value Pick": screen.value_pick(),

    "Growth Accelerator": screen.growth_accelerator(),

    "Dividend Champion": screen.dividend_champion(),

    "Debt Free Blue Chip": screen.debt_free_blue_chip(),

    "Turnaround Watch": screen.turnaround_watch(),

}

writer = pd.ExcelWriter(

    "output/screener_output.xlsx",

    engine="openpyxl"

)

for name, df in presets.items():

    df = score.score(df)

    df = df.sort_values(

        "composite_quality_score",

        ascending=False

    )

    df.to_excel(

        writer,

        sheet_name=name[:31],

        index=False

    )

writer.close()

ScreenerExporter.colour_file(

    "output/screener_output.xlsx"

)

print()

print("screener_output.xlsx created")