import cv2
import numpy as np
import os

# Define the directories.
ld_dir = "output_images/ld/"
muse_dir = "output_images/muse/"
output_dir = "output_images/"

# Get the sorted lists of files in the given directories.
ld_files = sorted(os.listdir(ld_dir))
muse_files = sorted(os.listdir(muse_dir))

# Iterate over each pair of files.
for ld_file, muse_file in zip(ld_files, muse_files):
    ld_path = ld_dir + ld_file
    muse_path = muse_dir + muse_file

    # Open the image files.
    img1_color = cv2.imread(muse_path)  # Image to be aligned.
    img2_color = cv2.imread(ld_path)  # Reference image.

    # Check if the images are read properly
    if img1_color is None or img2_color is None:
        print(f"Error reading one or both images: {muse_path}, {ld_path}")
        continue

    # Convert to grayscale.
    img1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)
    height, width = img2.shape

    # Create ORB detector with 5000 features.
    orb_detector = cv2.ORB_create(5000)

    # Find keypoints and descriptors.
    kp1, d1 = orb_detector.detectAndCompute(img1, None)
    kp2, d2 = orb_detector.detectAndCompute(img2, None)

    # Match features between the two images.
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match the two sets of descriptors.
    matches = matcher.match(d1, d2)

    # Sort matches on the basis of their Hamming distance.
    matches.sort(key=lambda x: x.distance)

    # Take the top 90 % matches forward.
    matches = matches[: int(len(matches) * 0.9)]
    no_of_matches = len(matches)

    # Define empty matrices of shape no_of_matches * 2.
    p1 = np.zeros((no_of_matches, 2))
    p2 = np.zeros((no_of_matches, 2))

    for i in range(len(matches)):
        p1[i, :] = kp1[matches[i].queryIdx].pt
        p2[i, :] = kp2[matches[i].trainIdx].pt

    try:
        # Find the homography matrix.
        homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)

        # Use this matrix to transform the
        # colored image wrt the reference image.
        transformed_img = cv2.warpPerspective(img1_color, homography, (width, height))

    except cv2.error as e:
        print(f"Error occurred when processing {muse_file} and {ld_file}: {str(e)}")
        continue

    # Construct the output file path
    output_file = output_dir + os.path.basename(ld_file)

    # Save the output.
    cv2.imwrite(output_file, transformed_img)
