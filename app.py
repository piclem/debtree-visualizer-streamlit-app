"""
import os
import streamlit as st
import subprocess

# Title for the app
st.title('Ubuntu Package Dependency Visualizer')

# Input field for the package name
package_name = st.text_input('Enter the package name you want to visualize:')
"""
import os
import streamlit as st
import subprocess

# Title for the app
st.title('Ubuntu Package Dependency Visualizer')

# Function to get the list of installed packages using dpkg-query
@st.cache_data
def get_installed_packages():
    try:
        # Run dpkg-query to get a list of installed packages
        result = subprocess.run(['dpkg-query', '-W', '-f=${binary:Package}\n'], capture_output=True, text=True)
        packages = result.stdout.splitlines()
        return sorted(packages)
    except Exception as e:
        st.error("Error fetching installed packages.")
        return []

# Fetch the list of installed packages
installed_packages = get_installed_packages()

# Package selection with autocompletion (dropdown with installed packages)
package_name = st.selectbox('Select the package to visualize its dependencies:', installed_packages)


# Button to trigger visualization
if st.button('Show Dependencies'):

    if package_name:
        # Use the debtree tool to generate package dependency graph
        try:
            st.write(f"Generating dependency tree for: `{package_name}`...")

            # Command to run the debtree and save the output as an image
            cmd = f'debtree --with-suggests {package_name} | dot -T png -o /tmp/{package_name}_dependency_tree.png'

            # Execute the command
            subprocess.run(cmd, shell=True, check=True)

            # Display the generated dependency image in the Streamlit app
            st.image(f'/tmp/{package_name}_dependency_tree.png')

        except subprocess.CalledProcessError as e:
            st.error(f"Error generating the dependency tree for `{package_name}`. Please make sure the package exists.")
    else:
        st.warning("Please enter a package name.")

