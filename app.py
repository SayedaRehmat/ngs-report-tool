import streamlit as st
import vcf  # pyvcf
import pandas as pd

st.set_page_config(page_title="VCF Variant Summary Tool", layout="wide")
st.title("🧬 VCF Variant Summary Tool (Python + Streamlit)")

uploaded_file = st.file_uploader("Upload a VCF file", type=["vcf"])

def summarize_vcf(reader):
    snvs = 0
    indels = 0
    transitions = 0
    transversions = 0

    for record in reader:
        if record.is_snp:
            snvs += 1
            ref, alt = record.REF, str(record.ALT[0])
            ti_pairs = {("A", "G"), ("G", "A"), ("C", "T"), ("T", "C")}
            if (ref, alt) in ti_pairs:
                transitions += 1
            else:
                transversions += 1
        elif record.is_indel:
            indels += 1

    total = snvs + indels
    ti_tv_ratio = round(transitions / transversions, 2) if transversions > 0 else "N/A"

    summary = pd.DataFrame([{
        "Total Variants": total,
        "SNVs": snvs,
        "Indels": indels,
        "Ti/Tv Ratio": ti_tv_ratio
    }])

    return summary

if uploaded_file is not None:
    with open("temp.vcf", "wb") as f:
        f.write(uploaded_file.read())

    try:
        with open("temp.vcf", "r") as f:
            reader = vcf.Reader(f)
            result_df = summarize_vcf(reader)
            st.subheader("📊 Summary Table")
            st.dataframe(result_df)
    except Exception as e:
        st.error(f"❌ Error parsing VCF file: {e}")
