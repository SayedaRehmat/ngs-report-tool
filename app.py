import streamlit as st
import vcf  # <- PyVCF
import pandas as pd

st.title("🧬 VCF Variant Summary Tool")

uploaded_file = st.file_uploader("Upload a VCF file", type=["vcf"])

def summarize_vcf(reader):
    snvs = 0
    indels = 0
    ti = 0
    tv = 0

    for record in reader:
        if record.is_snp:
            snvs += 1
            ref, alt = record.REF, record.ALT[0]
            pair = {ref, str(alt)}
            if pair in [{"A", "G"}, {"C", "T"}]:
                ti += 1
            else:
                tv += 1
        elif record.is_indel:
            indels += 1

    total = snvs + indels
    ti_tv = round(ti / tv, 2) if tv else None

    return pd.DataFrame([{
        "Total Variants": total,
        "SNVs": snvs,
        "Indels": indels,
        "Ti/Tv Ratio": ti_tv
    }])

if uploaded_file is not None:
    with open("temp.vcf", "wb") as f:
        f.write(uploaded_file.read())

    with open("temp.vcf", "r") as f:
        vcf_reader = vcf.Reader(f)
        summary_df = summarize_vcf(vcf_reader)
        st.subheader("📊 Variant Summary")
        st.dataframe(summary_df)
