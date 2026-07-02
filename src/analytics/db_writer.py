import sqlite3

DB_PATH = "db/nifty100.db"


class DatabaseWriter:

    @staticmethod
    def write(df):

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        # Clear existing rows
        cursor.execute("DELETE FROM financial_ratios")

        insert_sql = """
        INSERT INTO financial_ratios(

            company_id,
            year,

            net_profit_margin_pct,
            operating_profit_margin_pct,
            return_on_equity_pct,

            debt_to_equity,
            interest_coverage,
            asset_turnover,

            free_cash_flow_cr,
            capex_cr,

            earnings_per_share,
            book_value_per_share,

            dividend_payout_ratio_pct,
            total_debt_cr,
            cash_from_operations_cr,

            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr,

            composite_quality_score

        )
        VALUES(

            ?,?,
            ?,?,?,
            ?,?,?,
            ?,?,
            ?,?,
            ?,?,?,
            ?,?,?,
            ?

        )
        """

        rows = []

        for _, r in df.iterrows():

            rows.append(

                (

                    r["company_id"],
                    r["year"],

                    r["net_profit_margin_pct"],
                    r["operating_profit_margin_pct"],
                    r["return_on_equity_pct"],

                    r["debt_to_equity"],
                    r["interest_coverage"],
                    r["asset_turnover"],

                    r["free_cash_flow_cr"],
                    r["capex_cr"],

                    r["earnings_per_share"],
                    r["book_value_per_share"],

                    r["dividend_payout_ratio_pct"],
                    r["total_debt_cr"],
                    r["cash_from_operations_cr"],

                    r["revenue_cagr_5yr"],
                    r["pat_cagr_5yr"],
                    r["eps_cagr_5yr"],

                    r["composite_quality_score"]

                )

            )

        cursor.executemany(insert_sql, rows)

        conn.commit()

        conn.close()

        print()

        print("=" * 60)

        print("financial_ratios updated successfully")

        print("=" * 60)