import cv2

file_path = 'test/img2/20230615131504.bmp'

input_image = cv2.imread(file_path)

from boxdetect import config

cfg = config.PipelinesConfig()

# important to adjust these values to match the size of boxes on your image
cfg.width_range = (10, 100)
cfg.height_range = (10, 100)

# the more scaling factors the more accurate the results but also it takes more time to processing
# too small scaling factor may cause false positives
# too big scaling factor will take a lot of processing time
cfg.scaling_factors = [1.0]

# w/h ratio range for boxes/rectangles filtering
cfg.wh_ratio_range = (0.5, 1.8)

# range of groups sizes to be returned
cfg.group_size_range = (1, 100)

# for this image we will use rectangles as a kernel for morphological transformations
cfg.morph_kernels_type = 'rectangles'  # 'lines'

# num of iterations when running dilation tranformation (to engance the image)
cfg.dilation_iterations = 0

from boxdetect.pipelines import get_boxes

rects, grouping_rects, image, output_image = get_boxes(
    file_path, cfg=cfg, plot=False)

from boxdetect.img_proc import draw_rects, get_image

out_img = draw_rects(get_image(file_path), rects, thickness=3)
