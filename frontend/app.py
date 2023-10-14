import streamlit as st
import requests
import base64
import io

# Streamlit App
st.title("OCR Text Extraction")

# Option 1: Image-Sync POST Request
st.header("Option 1: Image-Sync POST Request")
uploaded_image_sync = st.file_uploader("Upload an image for OCR (Image-Sync)")

if uploaded_image_sync is not None:
    # Display the uploaded image
    st.image(uploaded_image_sync, use_column_width=True)

    # Perform Image-Sync OCR
    if st.button("Perform OCR (Image-Sync)"):
        # Encode the uploaded image as base64
        image_data = base64.b64encode(uploaded_image_sync.read()).decode("utf-8")
        data = {"image_data": image_data}
        response = requests.post("http://web:5001/image-sync", json=data)
        result = response.json()
        st.subheader("OCR Text (Image-Sync):")
        st.write(result["text"])

# Option 2: Image POST Request
st.header("Option 2: Image POST Request")
uploaded_image = st.file_uploader("Upload an image for OCR (Image)")

if uploaded_image is not None:
    # User-defined task name
    task_name = st.text_input("Task Name")

    # Perform Image POST Request
    if st.button("Perform OCR (Image)"):
        if task_name:
            # Encode the uploaded image as base64
            image_data = base64.b64encode(uploaded_image.read()).decode("utf-8")
            data = {"image_data": image_data, "name": task_name}
            response = requests.post("http://web:5001/image", json=data)
            result = response.json()

            # Store the task name and task ID mapping
            st.session_state[task_name] = result["task_id"]
            st.success(f"Task '{task_name}' mapped to Task ID: {result['task_id']}")


# Option 3: Image GET Request
st.header("Option 3: Image GET Request")

# Trigger the GET request when the selectbox is clicked
if st.button("Click to fetch tasks"):
    response = requests.get("http://web:5001/get-tasks")
    result = response.json()
    st.session_state.result = result
    st.session_state.key_ids = list(result.keys())

if 'key_ids' in st.session_state:
    # Create a selectbox and populate it with the fetched data
    selected_task = st.selectbox("Select Task Name", list(st.session_state['key_ids']))

    # Show the selected option
    st.write(f"Selected option: {selected_task}")
    if selected_task:
        if st.button("Get OCR Text"):
            task_id = st.session_state.result[selected_task]
            data = {"task_id": task_id}
            response = requests.get("http://web:5001/image", json=data)
            result = response.json()
            st.subheader("OCR Text:")
            st.write(result["text"])
    else:
        st.write("Click the button above to load data")
