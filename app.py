import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.set_page_config(
    page_title="GDP bình quân đầu người",
    page_icon="🌍"
)

st.title("🌍 GDP Bình Quân Đầu Người")

countries = {
    "Việt Nam": "VNM",
    "Hoa Kỳ": "USA",
    "Nhật Bản": "JPN",
    "Trung Quốc": "CHN",
    "Hàn Quốc": "KOR",
    "Thái Lan": "THA",
    "Singapore": "SGP",
    "Indonesia": "IDN",
    "Anh": "GBR",
    "Pháp": "FRA"
}

country_name = st.selectbox(
    "Chọn quốc gia",
    list(countries.keys())
)

country_code = countries[country_name]

url = (
    f"https://api.worldbank.org/v2/country/"
    f"{country_code}/indicator/NY.GDP.PCAP.CD"
    f"?format=json&per_page=100"
)

try:
    response = requests.get(url)
    data = response.json()

    records = []

    for item in data[1]:
        if item["value"] is not None:
            records.append({
                "Year": int(item["date"]),
                "GDP_PER_CAPITA": item["value"]
            })

    df = pd.DataFrame(records)

    df = df.sort_values("Year")

    st.subheader("📊 Bảng dữ liệu")
    st.dataframe(df)

    latest_value = df["GDP_PER_CAPITA"].iloc[-1]

    st.metric(
        "GDP bình quân đầu người mới nhất",
        f"${latest_value:,.0f}"
    )

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(
        df["Year"],
        df["GDP_PER_CAPITA"],
        marker="o"
    )

    ax.set_title(
        f"GDP bình quân đầu người - {country_name}"
    )

    ax.set_xlabel("Năm")
    ax.set_ylabel("USD/người")

    ax.grid(True)

    st.pyplot(fig)

except Exception as e:
    st.error(f"Lỗi: {e}")
