import streamlit as st
from cyvcf2 import VCF
import pandas as pd

st.title("🧬 VCF Variant Summary Tool")

uploaded_file = st.file_uploader("Upload a VCF file", type=["vcf"])

def get_summary(vcf):
    snv_count = 0
    indel_count = 0
    transitions = 0
    transversions = 0

    for variant in vcf:
        ref = variant.REF
        alt = variant.ALT[0]
        if len(ref) == 1 and len(alt) == 1:
            snv_count += 1
            pair = {ref, alt}
            if pair in [{"A", "G"}, {"C", "T"}]:
                transitions += 1
            else:
                transversions += 1
        else:
            indel_count += 1

    total = snv_count + indel_count
    ti_tv = round(transitions / transversions, 2) if transversions else None
    return pd.DataFrame([{
        "Total Variants": total,
        "SNVs": snv_count,
        "Indels": indel_count,
        "Ti/Tv Ratio": ti_tv
    }])

if uploaded_file is not None:
    with open("temp.vcf", "wb") as f:
        f.write(uploaded_file.read())
    
    vcf = VCF("temp.vcf")
    df_summary = get_summary(vcf)
    st.subheader("📊 Variant Summary")
    st.dataframe(df_summary)
