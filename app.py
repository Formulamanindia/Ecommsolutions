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
    /* Custom styling for the Streamlit button widget */
    .stButton>button {
        width: 100%;
        margin-top: auto; /* Push button to the bottom */
        background-color: #3b82f6; /* Custom Blue */
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


# --- Helper function to define Flipkart GST upload flow (based on user request) ---
def flipkart_gst_upload_form(firm_gstin, filing_period):
    st.header(f"Flipkart GSTR-1 Upload for {filing_period}")
    st.info(f"Using Seller's GSTIN: **{firm_gstin}**")

    st.subheader("Download Path")
    st.markdown("`Flipkart Portal → Report → Tax Reports → Sales report`")

    # Layout for Flipkart GSTIN
    col_gstin_label, col_gstin_input = st.columns([1, 2])
    
    with col_gstin_label:
        st.markdown("GSTIN of Flipkart:")
    with col_gstin_input:
        # This is a constant value for Flipkart's GSTIN (used for B2C/TCS transactions)
        flipkart_gstin_value = "07AACCF0683K1CU"
        st.text_input("GSTIN of Flipkart", value=flipkart_gstin_value, disabled=True, label_visibility="collapsed")
        
    st.subheader(f"Upload Files: ({filing_period})")
    
    # Single file uploader for Sales Report
    st.file_uploader("Sales Report", type=['xlsx', 'csv'], key="flipkart_sales_report", label_visibility="collapsed")
    
    st.markdown("---")
    
    # Process button
    if st.button("Upload", type="primary"):
        if st.session_state.get('flipkart_sales_report'):
            st.success(f"File uploaded and ready for processing against Flipkart GSTIN: {flipkart_gstin_value}.")
            # Mock processing and download
            gstr_output = pd.DataFrame({
                'GSTIN': [firm_gstin], 
                'Month': [filing_period], 
                'Platform': ['Flipkart'], 
                'Status': ['Ready for JSON Conversion']
            })
            st.dataframe(gstr_output)
            st.download_button("📥 Download GSTR-1 Ready Excel", data="mock_excel_data", file_name="Flipkart_GSTR1_Output.xlsx")
        else:
            st.error("Please upload the Sales Report file.")


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
        elif st.session_state['selected_platform'] == 'Flipkart_GST':
            flipkart_gst_upload_form(gstin, period) # Added the new form here

    # B. Show card grid and general uploader if no platform is selected
    else:
        st.subheader("Select Your Sales Platform & Report Type:")
        st.markdown("Upload your raw sales data from any of the following platforms to generate a GSTR-1 ready report.")

        # --- Combined Visual Card and Button Layout (Row 1) ---
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="platform-card" style="margin-bottom: 10px;">
                <div class="card-logo">🛍️</div>
                <div class="card-title">Meesho</div>
                <div class="card-subtitle">B2C</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Import Data", key="meesho_b2c_btn"):
                st.session_state['selected_platform'] = 'Meesho_B2C'
                st.rerun()
        
        with col2:
            st.markdown("""
            <div class="platform-card" style="margin-bottom: 10px;">
                <div class="card-logo">🅰️</div>
                <div class="card-title">Amazon</div>
                <div class="card-subtitle">B2C</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Import Data", key="amazon_b2c_btn"):
                st.session_state['selected_platform'] = 'Amazon_B2C'
                st.info("Amazon specific upload form will appear here soon.")
        
        with col3:
            st.markdown("""
            <div class="platform-card" style="margin-bottom: 10px;">
                <div class="card-logo">🅰️</div>
                <div class="card-title">Amazon B2B</div>
                <div class="card-subtitle">B2B</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Import Data", key="amazon_b2b_btn"):
                st.session_state['selected_platform'] = 'Amazon_B2B'
                st.info("Amazon B2B specific upload form will appear here soon.")

        with col4:
            st.markdown("""
            <div class="platform-card" style="margin-bottom: 10px;">
                <div class="card-logo">🅰️</div>
                <div class="card-title">Amazon B2B</div>
                <div class="card-subtitle">B2B Bulk Upload</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Import Data", key="amazon_b2b_bulk_btn"):
                st.session_state['selected_platform'] = 'Amazon_B2B_Bulk'
                st.info("Amazon B2B Bulk specific upload form will appear here soon.")

        # --- Combined Visual Card and Button Layout (Row 2) ---
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.markdown("""
            <div class="platform-card" style="margin-bottom: 10px;">
                <div class="card-logo">📘</div>
                <div class="card-title">Flipkart</div>
                <div class="card-subtitle">B2C & B2B Sales Report</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Import Data", key="flipkart_sales_btn"):
                st.session_state['selected_platform'] = 'Flipkart_Sales'
                st.info("Flipkart Sales specific upload form will appear here soon.")
        
        with col6:
            st.markdown("""
            <div class="platform-card" style="margin-bottom: 10px;">
                <div class="card-logo">📘</div>
                <div class="card-title">Flipkart</div>
                <div class="card-subtitle">GST Report Format</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Import Data", key="flipkart_gst_btn"):
                st.session_state['selected_platform'] = 'Flipkart_GST'
                st.rerun() # Rerun to show the new Flipkart GST form
        
        with col7:
            st.markdown("""
            <div class="platform-card" style="margin-bottom: 10px;">
                <div class="card-logo">👗</div>
                <div class="card-title">Myntra / Custom</div>
                <div class="card-subtitle">General Sales/Return Excel</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Import Data", key="myntra_report_btn"):
                st.session_state['selected_platform'] = 'Myntra'
                st.info("Myntra specific upload form will appear here soon.")
                
        with col8:
            st.markdown("""
            <div class="platform-card" style="margin-bottom: 10px;">
                <div class="card-logo">⚙️</div>
                <div class="card-title">Generic Custom Excel</div>
                <div class="card-subtitle">For B2C/B2B/Exempt data</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Import Data", key="custom_excel_btn"):
                st.session_state['selected_platform'] = 'Custom_Excel'
                st.info("Custom Excel mapping interface will appear here soon.")
                
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

# --- Helper function to read file metadata for dynamic dropdowns ---
@st.cache_data(show_spinner=False)
def get_file_metadata(uploaded_file, file_key):
    """
    Reads file to get sheet names and columns of the first sheet.
    Uses st.cache_data to speed up subsequent runs with the same file.
    """
    if uploaded_file is None:
        return {'sheets': ['(Upload File First)'], 'columns': ['(Upload File First)']}
    
    # Reset file pointer to the beginning for fresh reading
    uploaded_file.seek(0)
    
    # Check file type
    if uploaded_file.name.endswith('.xlsx'):
        try:
            xls = pd.ExcelFile(uploaded_file)
            sheet_names = xls.sheet_names
            
            # Read the first sheet to get column names
            df = pd.read_excel(uploaded_file, sheet_name=sheet_names[0])
            columns = ['(Select Column)'] + df.columns.tolist()

            return {'sheets': sheet_names, 'columns': columns, 'default_sheet': sheet_names[0]}
        except Exception as e:
            st.error(f"Error reading Excel sheets for {uploaded_file.name}: {e}")
            return {'sheets': ['(Error Reading Sheets)'], 'columns': ['(Error Reading Sheets)']}
    
    elif uploaded_file.name.endswith('.csv'):
        try:
            df = pd.read_csv(uploaded_file)
            columns = ['(Select Column)'] + df.columns.tolist()
            return {'sheets': ['Single Sheet'], 'columns': columns, 'default_sheet': 'Single Sheet'}
        except Exception as e:
            st.error(f"Error reading CSV file {uploaded_file.name}: {e}")
            return {'sheets': ['(Error Reading CSV)'], 'columns': ['(Error Reading CSV)']}

    else:
        return {'sheets': ['Unsupported File'], 'columns': ['Unsupported File']}

# ====================================================================
# --- TAB 4: PAYMENT RECONCILIATION ---
# ====================================================================
with tab4:
    st.header("🤝 Payment Reconciliation")
    st.info("Match your sales data against marketplace payment reports to find missing settlements.")
    
    tab_amz, tab_meesho, tab_flipkart = st.tabs(["Amazon", "Meesho", "Flipkart"])
    
    def render_mapping_controls(platform, report_type, needs_payment_col=False, expanded=False):
        
        # Determine keys for file uploader and state variables
        file_key = f"{platform}_{report_type.lower()}_file"
        sheet_key = f"{platform}_{report_type.lower()}_sheet"
        order_col_key = f"{platform}_{report_type.lower()}_order_col"
        payment_col_key = f"{platform}_{report_type.lower()}_payment_col"
        
        # Set up expander title
        title = f"{report_type} Report: Upload and Define Columns"
        
        with st.expander(title, expanded=expanded):
            
            # 1. File Uploader
            uploaded_file = st.file_uploader(f"Upload {platform} **{report_type}** Report", key=file_key, type=['xlsx', 'csv'])

            metadata = get_file_metadata(uploaded_file, file_key)

            # Initialize states if not present
            if sheet_key not in st.session_state: st.session_state[sheet_key] = metadata['sheets'][0] if metadata['sheets'][0] != '(Upload File First)' else '(Select Sheet)'
            if order_col_key not in st.session_state: st.session_state[order_col_key] = metadata['columns'][0]
            if payment_col_key not in st.session_state: st.session_state[payment_col_key] = metadata['columns'][0]
            
            
            if uploaded_file and metadata['columns'][0] != '(Upload File First)':
                
                # 2. Dynamic Sheet Selection (only for Excel files)
                if uploaded_file.name.endswith('.xlsx'):
                    try:
                        # Use the default sheet name from metadata to select initial index
                        default_index = metadata['sheets'].index(metadata['default_sheet']) if 'default_sheet' in metadata else 0
                        st.selectbox("Select Excel Sheet Name", metadata['sheets'], key=sheet_key, index=default_index)
                    except ValueError:
                         # Fallback if default sheet name isn't in the list (shouldn't happen with correct logic)
                        st.selectbox("Select Excel Sheet Name", metadata['sheets'], key=sheet_key, index=0)
                else:
                    st.markdown(f"**Sheet Name:** *({metadata['sheets'][0]})*")

                # 3. Dynamic Column Selection
                col_order, col_payment = st.columns(2 if needs_payment_col else 1)
                
                # Find index for 'Order ID' placeholder
                default_order_idx = metadata['columns'].index(st.session_state[order_col_key]) if st.session_state[order_col_key] in metadata['columns'] else 0
                
                with col_order:
                    st.selectbox("Order ID Column", metadata['columns'], key=order_col_key, index=default_order_idx)
                
                if needs_payment_col:
                    # Find index for 'Payment Col' placeholder
                    default_payment_idx = metadata['columns'].index(st.session_state[payment_col_key]) if st.session_state[payment_col_key] in metadata['columns'] else 0
                    with col_payment:
                        st.selectbox("Payment Received Column", metadata['columns'], key=payment_col_key, index=default_payment_idx)
            else:
                st.info("Upload an Excel or CSV file above to see sheet and column options.")


    def reconciliation_uploader(platform):
        st.subheader(f"{platform} Reconciliation Files")
        
        # 1. Sales Data (Needs Order ID column only)
        render_mapping_controls(platform, "Sales", needs_payment_col=False, expanded=True)

        # 2. Previous Payments (Needs Order ID and Payment Received columns)
        render_mapping_controls(platform, "Prev_Payments", needs_payment_col=True, expanded=False)

        # 3. Upcoming Payments (Needs Order ID and Payment Received columns)
        render_mapping_controls(platform, "Upcoming_Payments", needs_payment_col=True, expanded=False)
        
        st.divider()
        
        # --- Run Logic ---
        # NOTE: The keys are structured as f"{platform}_{report_type.lower()}_[sheet/order_col/payment_col]"
        
        if st.button(f"Run {platform} Reconciliation", type="primary", key=f"{platform}_run"):
            
            sales_sheet = st.session_state.get(f'{platform}_sales_sheet')
            sales_order_col = st.session_state.get(f'{platform}_sales_order_col')
            
            prev_sheet = st.session_state.get(f'{platform}_prev_payments_sheet')
            prev_order_col = st.session_state.get(f'{platform}_prev_payments_order_col')
            prev_payment_col = st.session_state.get(f'{platform}_prev_payments_payment_col')

            upcoming_sheet = st.session_state.get(f'{platform}_upcoming_payments_sheet')
            upcoming_order_col = st.session_state.get(f'{platform}_upcoming_payments_order_col')
            upcoming_payment_col = st.session_state.get(f'{platform}_upcoming_payments_payment_col')
            
            # Simple validation check (needs more robust checks in a real application)
            if sales_order_col == '(Select Column)':
                st.error("Please ensure you have uploaded the Sales Report and selected the Order ID column.")
            else:
                st.success(f"Starting reconciliation for **{platform}**...")
                
                # Displaying confirmation of parameters
                st.markdown("### Input Parameters Confirmed")
                st.markdown(f"**Sales Data Settings:** Sheet: `{sales_sheet}`, Order Col: `{sales_order_col}`")
                st.markdown(f"**Prev Payment Settings:** Sheet: `{prev_sheet}`, Order Col: `{prev_order_col}`, Payment Col: `{prev_payment_col}`")
                st.markdown(f"**Upcoming Payment Settings:** Sheet: `{upcoming_sheet}`, Order Col: `{upcoming_order_col}`, Payment Col: `{upcoming_payment_col}`")

                # Mock results display
                st.markdown("### Reconciliation Summary (Mock Data)")
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Sales Value", "₹5,00,000")
                c2.metric("Total Payment Received", "₹4,98,000")
                c3.metric("Variance (Missing Payment)", "₹2,000", delta="-₹2,000", delta_color="inverse")
                st.markdown("---")
                st.info("Reconciliation complete! Actual missing transaction details would be displayed here.")

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
