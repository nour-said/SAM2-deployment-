# import streamlit as st
# import numpy as np
# import cv2
# from PIL import Image
# from streamlit_image_coordinates import streamlit_image_coordinates

# # ---------------------------
# # segmentation function
# # ---------------------------
# def super_segment(img, point):

#     x, y = point

#     result = img.copy()

#     # مثال بسيط — ارسم دايرة مكان الضغط
#     cv2.circle(result, (x, y), 40, (255, 0, 0), -1)

#     return result


# # ---------------------------
# # UI
# # ---------------------------

# st.title("Interactive Segmentation UI")

# uploaded = st.file_uploader("Upload image", type=["jpg", "png"])

# if uploaded:

#     image = Image.open(uploaded).convert("RGB")
#     img_np = np.array(image)

#     st.subheader("Click on image")

#     coords = streamlit_image_coordinates(image)

#     if coords:

#         x = coords["x"]
#         y = coords["y"]

#         st.write(f"Clicked point: ({x}, {y})")

#         result = super_segment(img_np, (x, y))

#         st.subheader("Result")

#         st.image(result)
import streamlit as st
import numpy as np
import cv2
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# ---------------------------
# segmentation function
# ---------------------------
def super_segment(img, point):

    x, y = point
    result = img.copy()

    cv2.circle(result, (x, y), 40, (255, 0, 0), -1)

    return result


# ---------------------------
# session memory
# ---------------------------
if "clicked_point" not in st.session_state:
    st.session_state.clicked_point = None


# ---------------------------
# UI
# ---------------------------

st.title("Interactive Segmentation UI")

uploaded = st.file_uploader("Upload image", type=["jpg", "png"])

if uploaded:

    image = Image.open(uploaded).convert("RGB")
    img_np = np.array(image)

    st.subheader("Click ONCE on image")

    # 👇 يسمح بالضغط مرة واحدة فقط
    if st.session_state.clicked_point is None:

        coords = streamlit_image_coordinates(image)

        if coords:
            st.session_state.clicked_point = (coords["x"], coords["y"])

    # 👇 لو النقطة محفوظة
    if st.session_state.clicked_point:

        x, y = st.session_state.clicked_point

        st.success(f"Point locked: ({x}, {y})")

        result = super_segment(img_np, (x, y))

        st.subheader("Result")
        st.image(result)

        # زر reset
        if st.button("Reset"):
            st.session_state.clicked_point = None
