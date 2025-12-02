import streamlit as st
import pandas as pd
from io import BytesIO

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="E-Commerce Solutions Hub",
    page_icon="📦",
    layout="wide"
)

# --- HEADER ---
st.title("🚀 E-Commerce Service Hub")
st.markdown("One-stop solution for GST Filing, Analytics, Reconciliation, and Optimization.")

# --- CUSTOM CSS FOR CARDS ---
# We use this to style the cards to look professional
# Note: Emojis are used for logos as images are not supported in this format easily.
CARD_STYLE = """
<style>
    .platform-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        background-color: #ffffff;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%; /* Ensures cards in a column have same height */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .platform-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    .card-title {
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .card-subtitle {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 15px;
        min-height: 40px; /* Consistent height for subtitles */
    }
    .card-logo {
        font-size: 3em;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        margin-top: auto; /* Push button to the bottom */
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
</style>
"""
st.markdown(CARD_STYLE, unsafe_allow_html=True)


# --- TABS CONFIGURATION ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📑 GST Filing", 
    "📈 Sales Analysis", 
    "↩️ Return Analysis", 
    "🤝 Reconciliation", 
    "✍️ Listing Optimization", 
    "📢 Ads Manager"
])

# --- Helper function to define Meesho upload flow ---
def meesho_upload_form(firm_gstin, filing_period):
    st.header(f"Meesho GSTR-1 Upload for {filing_period}")
    st.info(f"Using Firm GSTIN: **{firm_gstin}**")

    # Display the GSTIN input from the main form for context (or allow editing)
    st.subheader("Required Reports for GST Filing")
    
    # 1. TCS Sales & Return Reports
    st.markdown("#### Reports from Meesho Panel → Payments → Download GST Reports")
    col_tcs1, col_tcs2 = st.columns(2)
    with col_tcs1:
        st.file_uploader("Upload TCS Sales (e.g., tcs_sales.xlsx)", type=['xlsx'], key="meesho_tcs_sales")
    with col_tcs2:
        st.file_uploader("Upload TCS Sales Return (e.g., tcs_sales_return.xlsx)", type=['xlsx'], key="meesho_tcs_returns")

    # 2. Tax Invoice Details
    st.markdown("#### Tax Invoice Details (Meesho Panel → Payments → Tax Invoice)")
    st.warning("Unzip the file and upload only the Excel (Tax_invoice_details.xlsx) file.")
    st.file_uploader("Upload Tax Invoice Details (e.g., Tax_invoice_details.xlsx)", type=['xlsx'], key="meesho_tax_invoice")
    
    st.markdown("---")
    
    # Process button
    if st.button("Process Meesho GSTR-1 Report", type="primary"):
        # Check if all 3 files are uploaded
        if st.session_state.get('meesho_tcs_sales') and st.session_state.get('meesho_tcs_returns') and st.session_state.get('meesho_tax_invoice'):
            st.success(f"Processing GSTR-1 for {filing_period} using {firm_gstin}...")
            # Mock processing and download
            gstr_output = pd.DataFrame({
                'GSTIN': [firm_gstin], 
                'Month': [filing_period], 
                'Status': ['Ready for JSON Conversion'], 
                'B2C': ['Calculated'],
                'Tax': ['Calculated']
            })
            st.dataframe(gstr_output)
            st.download_button("📥 Download GSTR-1 Ready Excel", data="mock_excel_data", file_name="Meesho_GSTR1_Output.xlsx")
        else:
            st.error("Please upload all three required files to run the processing.")


# ====================================================================
# --- TAB 1: GST FILING SERVICES (NEW CARD LAYOUT & LOGIC) ---
# ====================================================================
with tab1:
    st.header("GSTR1 Data Preparation")
    
    # --- 1. Mandatory GST Inputs ---
    st.subheader("Firm Details and Filing Period")
    col_g1, col_g2 = st.columns(2)
    
    current_year = pd.Timestamp.now().year
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    years = [current_year, current_year - 1, current_year - 2]
    
    with col_g1:
        gstin = st.text_input("Firm GSTIN", key="firm_gstin", placeholder="Enter your 15-digit GSTIN")
    
    with col_g2:
        period = st.selectbox("Filing Month & Year", [f"{m} - {y}" for y in years for m in months], key="filing_period")

    # Initialize session state for platform selection
    if 'selected_platform' not in st.session_state:
        st.session_state['selected_platform'] = 'None'
    
    # Check for mandatory inputs and stop rendering if missing
    if not gstin or len(gstin) != 15: # Basic GSTIN length check
        st.warning("Please enter a valid 15-digit GSTIN and select the Filing Period to proceed with data upload.")
        st.session_state['selected_platform'] = 'None' # Reset platform selection if GSTIN is cleared
        st.stop() # Stop rendering the rest of the tab until inputs are provided

    st.markdown("---") # Separator after mandatory inputs

    # --- 2. Conditional Rendering ---
    
    # A. Show BACK button and specific form if a platform is selected
    if st.session_state['selected_platform'] != 'None':
        if st.button("⬅️ Back to Platform Selection"):
            st.session_state['selected_platform'] = 'None'
            st.rerun() # Rerun to show the card grid again
        
        # Display the specific form
        if st.session_state['selected_platform'] == 'Meesho_B2C':
            meesho_upload_form(gstin, period)

    # B. Show card grid and general uploader if no platform is selected
    else:
        st.subheader("Select Your Sales Platform & Report Type:")
        st.markdown("Upload your raw sales data from any of the following platforms to generate a GSTR-1 ready report.")

        # --- Functional Buttons (Invisible, used for state change) ---
        # The buttons must be defined before the HTML to execute the logic first
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Import Data for Meesho B2C", key="meesho_b2c"):
                st.session_state['selected_platform'] = 'Meesho_B2C'
                st.rerun()
        
        with col2:
            if st.button("Import Data for Amazon B2C", key="amazon_b2c"):
                st.session_state['selected_platform'] = 'Amazon_B2C'
                st.info("Amazon specific upload form will appear here soon.")
        
        with col3:
            if st.button("Import Data for Amazon B2B", key="amazon_b2b"):
                st.session_state['selected_platform'] = 'Amazon_B2B'
                st.info("Amazon B2B specific upload form will appear here soon.")

        with col4:
            if st.button("Import Data for Amazon B2B Bulk", key="amazon_b2b_bulk"):
                st.session_state['selected_platform'] = 'Amazon_B2B_Bulk'
                st.info("Amazon B2B Bulk specific upload form will appear here soon.")

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            if st.button("Import Data for Flipkart Sales", key="flipkart_sales"):
                st.session_state['selected_platform'] = 'Flipkart_Sales'
                st.info("Flipkart Sales specific upload form will appear here soon.")
        
        with col6:
            if st.button("Import Data for Flipkart GST", key="flipkart_gst"):
                st.session_state['selected_platform'] = 'Flipkart_GST'
                st.info("Flipkart GST specific upload form will appear here soon.")
        
        with col7:
            if st.button("Import Data for Myntra", key="myntra_report"):
                st.session_state['selected_platform'] = 'Myntra'
                st.info("Myntra specific upload form will appear here soon.")
                
        with col8:
            if st.button("Import Data for Custom Excel", key="custom_excel"):
                st.session_state['selected_platform'] = 'Custom_Excel'
                st.info("Custom Excel mapping interface will appear here soon.")


        # --- Visual Card Layout (HTML) ---
        # NOTE: The functional buttons above need to be visually aligned with these cards in Streamlit
        st.markdown("""
        <div style="display: flex; gap: 15px; margin-bottom: 20px;">
            <div style="flex: 1;">
                <div class="platform-card">
                    <div class="card-logo">🛍️</div>
                    <div class="card-title">Meesho</div>
                    <div class="card-subtitle">B2C</div>
                </div>
            </div>
            <div style="flex: 1;">
                <div class="platform-card">
                    <div class="card-logo">🅰️</div>
                    <div class="card-title">Amazon</div>
                    <div class="card-subtitle">B2C</div>
                </div>
            </div>
            <div style="flex: 1;">
                <div class="platform-card">
                    <div class="card-logo">🅰️</div>
                    <div class="card-title">Amazon B2B</div>
                    <div class="card-subtitle">B2B</div>
                </div>
            </div>
            <div style="flex: 1;">
                <div class="platform-card">
                    <div class="card-logo">🅰️</div>
                    <div class="card-title">Amazon B2B</div>
                    <div class="card-subtitle">B2B Bulk Upload</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="display: flex; gap: 15px; margin-bottom: 20px;">
            <div style="flex: 1;">
                <div class="platform-card">
                    <div class="card-logo">📘</div>
                    <div class="card-title">Flipkart</div>
                    <div class="card-subtitle">B2C & B2B Sales Report</div>
                </div>
            </div>
            <div style="flex: 1;">
                <div class="platform-card">
                    <div class="card-logo">📘</div>
                    <div class="card-title">Flipkart</div>
                    <div class="card-subtitle">GST Report Format</div>
                </div>
            </div>
            <div style="flex: 1;">
                <div class="platform-card">
                    <div class="card-logo">👗</div>
                    <div class="card-title">Myntra / Custom</div>
                    <div class="card-subtitle">General Sales/Return Excel</div>
                </div>
            </div>
            <div style="flex: 1;">
                <div class="platform-card">
                    <div class="card-logo">⚙️</div>
                    <div class="card-title">Generic Custom Excel</div>
                    <div class="card-subtitle">For B2C/B2B/Exempt data</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

        # --- General Uploader Section ---
        st.subheader("Alternatively, drag & drop any sales report file here")
        
        col_upload, col_download = st.columns([3, 1])

        with col_upload:
            uploaded_gst = st.file_uploader(
                "Upload your sales report (Excel/CSV)", 
                type=['xlsx', 'csv'], 
                key="gst_general_file",
                label_visibility="collapsed"
            )
        
        with col_download:
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button("Download GSTR Ready File", data="mock_data", file_name="GSTR_Ready_File.csv", key="download_gst_mock")

        
        # --- Processing Logic after General Upload ---
        if uploaded_gst:
            st.success("File uploaded successfully! Processing and mapping to GSTR-1 format...")
            
            try:
                if uploaded_gst.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_gst)
                else:
                    df = pd.read_excel(uploaded_gst)

                # Mock GST processing
                gstr_output = pd.DataFrame({
                    'GSTIN': [gstin], 
                    'Invoice No': ['INV001', 'INV002'], 
                    'B2C_Sales': [2500, 0], 
                    'B2B_Sales': [0, 5000],
                    'Tax Rate': ['18%', '5%'],
                    'HSN Code': ['8471', '8517']
                })

                st.markdown("### GSTR-1 Preview (B2C & B2B Summary)")
                st.dataframe(gstr_output)
                
                def to_excel(df):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='GSTR1_Output')
                    processed_data = output.getvalue()
                    return processed_data

                excel_data = to_excel(gstr_output)

                st.download_button(
                    label="📥 Download GSTR-1 Ready Excel",
                    data=excel_data,
                    file_name="GSTR1_Ready_Output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            except Exception as e:
                st.error(f"Error reading file: {e}")


# ====================================================================
# --- TAB 2: SALES ANALYSIS (Logic omitted for brevity) ---
# ====================================================================
with tab2:
    st.header("📊 Sales Performance Analytics")
    st.write("This tab will contain dynamic charts for Revenue Trend, SKU Performance, and Regional Sales using Plotly.")

# ====================================================================
# --- TAB 3: RETURN ANALYSIS (Logic omitted for brevity) ---
# ====================================================================
with tab3:
    st.header("↩️ Return & Refund Analysis")
    st.write("This tab will show key metrics on Return Percentage and Top 10 returned SKUs.")

# ====================================================================
# --- TAB 4: PAYMENT RECONCILIATION (Logic omitted for brevity) ---
# ====================================================================
with tab4:
    st.header("🤝 Payment Reconciliation")
    st.info("Match your sales data against marketplace payment reports to find missing settlements.")
    
    tab_amz, tab_meesho, tab_flipkart = st.tabs(["Amazon", "Meesho", "Flipkart"])
    
    def reconciliation_uploader(platform):
        st.subheader(f"{platform} Reconciliation Files")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**1. Sales Data**")
            st.file_uploader(f"Upload {platform} **Sales Report**", key=f"{platform}_sales", type=['xlsx', 'csv'])
        with col2:
            st.markdown("**2. Previous Payments**")
            st.file_uploader(f"Upload {platform} **Settlement/Prev Payments**", key=f"{platform}_prev", type=['xlsx', 'csv'])
        with col3:
            st.markdown("**3. Upcoming Payments**")
            st.file_uploader(f"Upload {platform} **Upcoming Payments**", key=f"{platform}_upcoming", type=['xlsx', 'csv'])
        
        st.divider()
        if st.button(f"Run {platform} Reconciliation", key=f"{platform}_run"):
            st.success(f"Reconciliation for **{platform}** complete!")
            st.markdown("### Reconciliation Summary (Mock Data)")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Sales Value", "₹5,00,000")
            c3.metric("Variance (Missing Payment)", "₹2,000", delta="-₹2,000", delta_color="inverse")

    with tab_amz:
        reconciliation_uploader("Amazon")
    with tab_meesho:
        reconciliation_uploader("Meesho")
    with tab_flipkart:
        reconciliation_uploader("Flipkart")

# ====================================================================
# --- TAB 5: LISTING OPTIMIZATION (Logic omitted for brevity) ---
# ====================================================================
with tab5:
    st.header("✍️ Listing Optimization Tool")
    st.write("This tab helps generate SEO-friendly titles and descriptions using target keywords.")

# ====================================================================
# --- TAB 6: ADS MANAGER (Logic omitted for brevity) ---
# ====================================================================
with tab6:
    st.header("📢 Ads Performance Manager")
    st.write("This tab will allow you to analyze ACOS (Advertising Cost of Sales) and optimize campaigns.")
