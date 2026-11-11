import cv2, numpy as np, glob, os
os.makedirs("clean", exist_ok=True)
for f in sorted(glob.glob("raw-*")):
    im = cv2.imread(f)
    if im.shape[0] > 2000: im = cv2.resize(im, (2000, 2000), interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    sat = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[:, :, 1]
    fg = ((g < 247) | (sat > 30)).astype(np.uint8)
    op = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))   # removes 1-4px lines and label text
    n, lab, st, _ = cv2.connectedComponentsWithStats(op, 8)
    keep = np.zeros_like(op)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 0.004 * op.size: keep[lab == i] = 1
    keep = cv2.dilate(keep, np.ones((13, 13), np.uint8))            # keep anti-aliased edges + soft shadow
    ff = keep.copy(); h, w = keep.shape; msk = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(ff, msk, (0, 0), 1); keep = keep | (1 - ff)       # fill enclosed areas (white screen panels)
    soft = cv2.GaussianBlur(keep.astype(np.float32), (9, 9), 0)[..., None]
    out = (im * soft + 255 * (1 - soft)).astype(np.uint8)
    ys, xs = np.where(keep > 0); pad = 40
    out = out[max(0, ys.min() - pad):ys.max() + pad, max(0, xs.min() - pad):xs.max() + pad]
    cv2.imwrite("clean/" + os.path.basename(f).split(".")[0] + ".png", out)
