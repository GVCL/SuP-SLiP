# Code

For more details about the three stages of the SuP-SLiP pipeline, please refer to the individual files:
- [M1: Candidate point recommendation](./methods/m1.py)
- [M2: Nearest neighbor computation](./methods/m2.py)
- [M3: Final annotation generation](./methods/m3.py)

---

For an end-to-end example of point masking, please refer to [this notebook](./toronto3d_point_masking.ipynb). To run the same on your end, you must adjust the paths to your dataset and load binary label arrays (of ground truth and model inference results) as numpy files and update their paths as well.