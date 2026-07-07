from src.screener.presets import PresetScreeners

screen = PresetScreeners()

presets = {
    "Quality Compounder": screen.quality_compounder(),
    "Value Pick": screen.value_pick(),
    "Growth Accelerator": screen.growth_accelerator(),
    "Dividend Champion": screen.dividend_champion(),
    "Debt-Free Blue Chip": screen.debt_free_blue_chip(),
    "Turnaround Watch": screen.turnaround_watch(),
}

for name, df in presets.items():

    print("=" * 60)
    print(name)
    print("Companies:", len(df))
    print(df[["company_id"]].head())