import sqlite3
import pandas as pd
import streamlit as st

DB = "db/nifty100.db"


@st.cache_data(ttl=600)
def run_query(query):

    conn = sqlite3.connect(DB)

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_companies():

    return run_query(
        "SELECT * FROM companies"
    )


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    if year:

        query = f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{ticker}'
        AND year='{year}'
        """

    else:

        query = f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{ticker}'
        """

    return run_query(query)


@st.cache_data(ttl=600)
def get_pl(ticker):

    return run_query(

        f"""
        SELECT *
        FROM profitandloss
        WHERE company_id='{ticker}'
        """
    )


@st.cache_data(ttl=600)
def get_bs(ticker):

    return run_query(

        f"""
        SELECT *
        FROM balancesheet
        WHERE company_id='{ticker}'
        """
    )


@st.cache_data(ttl=600)
def get_cf(ticker):

    return run_query(

        f"""
        SELECT *
        FROM cashflow
        WHERE company_id='{ticker}'
        """
    )


@st.cache_data(ttl=600)
def get_sectors():

    return run_query(

        "SELECT * FROM sectors"
    )


@st.cache_data(ttl=600)
def get_peers(group_name):

    return run_query(

        f"""
        SELECT *
        FROM peer_groups
        WHERE peer_group_name='{group_name}'
        """
    )


@st.cache_data(ttl=600)
def get_valuation(ticker):

    return run_query(

        f"""
        SELECT *
        FROM market_cap
        WHERE company_id='{ticker}'
        """
    )


@st.cache_data(ttl=600)
def get_latest_ratios(year=None):

    if year:

        return run_query(f"""
        SELECT *
        FROM financial_ratios
        WHERE year='{year}'
        """)

    return run_query("""
    SELECT *
    FROM financial_ratios
    """)


@st.cache_data(ttl=600)
def get_company_profile(ticker):

    query = f"""
    SELECT
        c.company_name,
        c.id,
        c.about_company,
        s.broad_sector,
        s.sub_sector
    FROM companies c
    LEFT JOIN sectors s
    ON c.id = s.company_id
    WHERE c.id = '{ticker}'
    """

    return run_query(query)


@st.cache_data(ttl=600)
def get_pros_cons(ticker):

    query = f"""
    SELECT *
    FROM prosandcons
    WHERE company_id='{ticker}'
    """

    return run_query(query)


@st.cache_data(ttl=600)
def get_peer_groups():

    return run_query("""
        SELECT DISTINCT peer_group_name
        FROM peer_groups
        ORDER BY peer_group_name
    """)


@st.cache_data(ttl=600)
def get_peer_companies(group):

    return run_query(f"""
        SELECT
            p.company_id,
            c.company_name,
            p.is_benchmark
        FROM peer_groups p
        LEFT JOIN companies c
        ON p.company_id=c.id
        WHERE p.peer_group_name='{group}'
        ORDER BY company_name
    """)


@st.cache_data(ttl=600)
def get_peer_ratios(group):

    return run_query(f"""
        SELECT
            fr.*,
            c.company_name,
            pg.is_benchmark
        FROM financial_ratios fr
        LEFT JOIN companies c
            ON fr.company_id=c.id
        LEFT JOIN peer_groups pg
            ON fr.company_id=pg.company_id
        WHERE pg.peer_group_name='{group}'
    """)