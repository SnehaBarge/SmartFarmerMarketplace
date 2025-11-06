import streamlit as st
from database.db_functions import get_data # Import database function

def show_home_page():
    """Renders the main welcome page content."""
    st.image(
        "https://images.unsplash.com/photo-1599759805137-c15e8d7a7a06?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200",
        caption="A vibrant platform connecting farmers and buyers.",
        use_column_width=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True) 
    st.header("👋 Welcome to the Smart Farmer Marketplace!")
    st.write("This platform helps farmers maximize profits by connecting them directly with buyers or renters.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🧰 Tool Sharing", icon="🛠️")
        st.markdown("Rent out unused machinery and tools in your village.")
    with col2:
        st.success("🌾 Crop Sales", icon="💰")
        st.markdown("List your harvested crops for sale at competitive prices.")
    with col3:
        st.warning("🔗 Direct Contact", icon="📞")
        st.markdown("All listings include direct contact information for quick deals.")

    st.markdown('</div>', unsafe_allow_html=True)


def show_db_check_page():
    """Renders the Database Check (Admin) view."""
    st.header("💾 Direct Database View (Read-Only)")
    st.info("This view fetches all current data directly from 'farmermarket.db' using Pandas for instant verification.")
    
    tab_t, tab_c = st.tabs(["🧰 All Tools Data", "🌾 All Crops Data"])
    
    # Tools Database View
    with tab_t:
        st.subheader("Tools Table Contents")
        try:
            # Drop the rowid column for cleaner display in the check
            db_tools_df = get_data("tools").drop(columns=['rowid'])
            st.dataframe(db_tools_df, use_container_width=True)
            st.success(f"Successfully loaded {len(db_tools_df)} tool records.")
        except Exception as e:
            st.error(f"Error loading tools data: {e}")

    # Crops Database View
    with tab_c:
        st.subheader("Crops Table Contents")
        try:
            # Drop the rowid column for cleaner display in the check
            db_crops_df = get_data("crops").drop(columns=['rowid'])
            st.dataframe(db_crops_df, use_container_width=True)
            st.success(f"Successfully loaded {len(db_crops_df)} crop records.")
        except Exception as e:
            st.error(f"Error loading crops data: {e}")