import streamlit as st
from fpdf import FPDF

# ---------------------
# 🎨 Styling
# ---------------------
st.set_page_config(page_title="Audio Bookmark Generator", page_icon="🔖")

st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        h1, h3 { color: #1f4e79; }
        .stButton > button { background-color: #1f4e79; color: white; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🔖 Audio Bookmark Generator</h1>", unsafe_allow_html=True)
st.markdown("Create audio or video bookmarks and download a clean PDF report.")

# ---------------------
# 📘 Tutorial
# ---------------------
with st.expander("📘 How to Use This App"):
    st.markdown("""
    1. **Upload** an `.mp4` or `.m4a` file (optional – just for context).
    2. **Add bookmarks** using start time, end time, and a title.
    3. Use the ✏️ **Edit** or 🗑 **Delete** buttons to update your list.
    4. Click **Generate PDF Report** to download a summary.
    """)

# ---------------------
# 📁 Session State
# ---------------------
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# ---------------------
# 📤 File Upload (Optional)
# ---------------------
uploaded_file = st.file_uploader("Upload an audio or video file (.mp4 or .m4a)", type=["mp4", "m4a"])
if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

# ---------------------
# ➕ Add Bookmark
# ---------------------
with st.form("add_bookmark"):
    st.subheader("Add a Bookmark")
    start = st.text_input("Start Time (HH:MM:SS)", "00:00:00")
    end = st.text_input("End Time (HH:MM:SS)", "00:00:10")
    title = st.text_input("Bookmark Title", "Intro")
    if st.form_submit_button("Add Bookmark"):
        st.session_state.bookmarks.append((start, end, title))
        st.success("Bookmark added!")

# ---------------------
# ✏️ Edit / Delete Bookmarks
# ---------------------
if st.session_state.bookmarks:
    st.subheader("Current Bookmarks")

    for i, (start, end, title) in enumerate(st.session_state.bookmarks):
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(f"**{i+1}.** {title} ({start} to {end})")

        if col2.button("✏️ Edit", key=f"edit_{i}"):
            st.session_state.edit_index = i
            st.session_state.edit_start = start
            st.session_state.edit_end = end
            st.session_state.edit_title = title

        if col3.button("🗑 Delete", key=f"delete_{i}"):
            st.session_state.bookmarks.pop(i)
            st.rerun()


# ---------------------
# 📝 Edit Form
# ---------------------
if st.session_state.edit_index is not None:
    st.subheader("Edit Bookmark")
    with st.form("edit_form"):
        new_start = st.text_input("Start time", value=st.session_state.edit_start)
        new_end = st.text_input("End time", value=st.session_state.edit_end)
        new_title = st.text_input("Bookmark title", value=st.session_state.edit_title)
        if st.form_submit_button("Update Bookmark"):
            i = st.session_state.edit_index
            st.session_state.bookmarks[i] = (new_start, new_end, new_title)
            st.session_state.edit_index = None
            st.rerun()


# ---------------------
# 📄 Generate PDF
# ---------------------
def generate_pdf(bookmarks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Audio Bookmarks", ln=True, align="C")
    pdf.ln(10)
    for i, (start, end, title) in enumerate(bookmarks, 1):
        pdf.multi_cell(0, 10, txt=f"{i}. {title}\nStart: {start}   End: {end}\n")
    return pdf.output(dest="S").encode("latin-1")

if st.session_state.bookmarks:
    st.subheader("Export Your Work")
    if st.button("📄 Generate PDF Report"):
        pdf_bytes = generate_pdf(st.session_state.bookmarks)
        st.download_button("Download PDF", pdf_bytes, file_name="bookmarks.pdf")

# ---------------------
# 🔻 Footer
# ---------------------
st.markdown("---")
st.markdown("Made with ❤️ by Danielle Khaitas")
