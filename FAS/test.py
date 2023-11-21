import os
import cv2
import numpy as np
import argparse
import warnings
import time

from FAS.src.anti_spoof_predict import AntiSpoofPredict
from FAS.src.generate_patches import CropImage
from FAS.src.utility import parse_model_name

def test(model_dir, device_id, image):
    model_test = AntiSpoofPredict(device_id)
    image_cropper = CropImage()
    result = image
    if result is False:
        return
    image_bbox = model_test.get_bbox(image)
    prediction = np.zeros((1, 3))
    test_speed = 0
    # sum the prediction from single model's result
    for model_name in os.listdir(model_dir):
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": image,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False
        img = image_cropper.crop(**param)
        start = time.time()
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))
        test_speed += time.time()-start

    # draw result of prediction
    RF = None
    label = np.argmax(prediction)
    value = prediction[0][label]/2
    if label == 1:
        print("Real Face. Score: {:.2f}.".format(value))
        RF = True
    else:
        print("Fake Face. Score: {:.2f}.".format(value))
        RF = False
    print("Prediction cost {:.2f} s".format(test_speed))
    if RF:
        print(RF)
    else:
        print(RF)

    return RF


def anti_spoof(image):
    desc = "test"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--device_id",
        type=int,
        default=0,
        help="which gpu id, [0/1/2/3]")
    parser.add_argument(
        "--model_dir",
        type=str,
        default="../FAS/resources/anti_spoof_models",
        help="model_lib used to test")
    args = parser.parse_args()
    result = test(args.model_dir, args.device_id, image)
    return result