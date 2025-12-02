import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(page_title="E-Com Service Hub", layout="wide")

st.title("🛍️ E-Commerce Service Assistant")
st.markdown("Automated solutions for Sellers: GST, Analytics, and Optimization.")

# --- Sidebar Navigation ---
menu = ["Sales Analysis", "GST Report Generator", "Return Analysis"]
choice = st.sidebar.selectbox("Select Service", menu)

# --- HELPER FUNCTION: Convert DF to Excel for Download ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# --- MODULE 1: SALES ANALYSIS ---
if choice == "Sales Analysis":
    st.subheader("📊 Sales Data Insights")
    uploaded_file = st.file_uploader("Upload Amazon/Flipkart Sales Report (Excel)", type=["xlsx", "csv"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Basic KPI Display
            # Assuming column names 'Date', 'Order Amount', 'State' exist (You must standardize this)
            col1, col2 = st.columns(2)
            col1.metric("Total Rows", len(df))
            
            # Check if we can find a generic amount column for demo
            possible_amount_cols = [c for c in df.columns if 'amount' in c.lower() or 'price' in c.lower()]
            if possible_amount_cols:
                total_sales = df[possible_amount_cols[0]].sum()
                col2.metric("Total Revenue", f"₹{total_sales:,.2f}")
                
                # Chart
                st.write("### Sales Distribution")
                fig = px.bar(df, x=df.columns[0], y=possible_amount_cols[0], title="Sales Overview")
                st.plotly_chart(fig)
            else:
                st.warning("Could not automatically detect an 'Amount' column. Please check column names.")

            st.dataframe(df.head())

        except Exception as e:
            st.error(f"Error processing file: {e}")

# --- MODULE 2: GST GENERATOR ---
elif choice == "GST Report Generator":
    st.subheader("🧾 GSTR1 Data Preparation")
    st.info("Upload your raw sales report to generate a format suitable for GST filing.")
    
    gst_file = st.file_uploader("Upload Sales Data", key="gst_uploader")
    
    if gst_file:
        df = pd.read_excel(gst_file) # Assuming Excel
        
        # --- LOGIC SIMULATION ---
        # Real GST logic is complex. This is a placeholder example.
        # 1. Filter out Cancelled orders
        # 2. Separate IGST, CGST, SGST based on State
        
        st.write("Processing data for GSTR1...")
        
        # Create a simplified output dataframe
        gst_output = df.copy()
        
        # Example transformation: Add a 'Place of Supply' column if missing
        if 'State' in gst_output.columns:
            gst_output['Place of Supply'] = gst_output['State']
            
        st.success("GSTR1 Draft Generated!")
        st.dataframe(gst_output.head())
        
        # Download Button
        excel_data = to_excel(gst_output)
        st.download_button(
            label="📥 Download GSTR1 Excel",
            data=excel_data,
            file_name="GSTR1_Ready_File.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# --- MODULE 3: RETURN ANALYSIS ---
elif choice == "Return Analysis":
    st.subheader("↩️ Return Analysis")
    st.write("Upload return reports to analyze return reasons and top returning SKUs.")
    # Similar logic to Sales Analysis
