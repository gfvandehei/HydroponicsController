import os
from typing import List
import cv2
import datetime

class CameraStore(object):

    def __init__(self, directory: str, day_pic_time: datetime.time):
        """A camera store is a directory on this machine we will store images in

        :param directory: the directory (absolute path) that pictures will be placed in
        :type directory: str
        :param day_pic_time: the time of day a single photo will be saved for timelapse
        :type day_pic_time: datetime.time
        """
        self._base_dir = directory
        self._day_pic_time = day_pic_time

        self._stream_pic_name = self._base_dir+"/stream.jpg"
        self.last_day_saved: datetime.date = None

        self.format_image_dir()
    
    def format_image_dir(self):
        # check subdir /timelapse exists
        if not os.path.isdir(self._base_dir+"/timelapse"):
            print("/timelapse did not exist, creaeting")
            os.mkdir(self._base_dir+"/timelapse")

    def save_image(self, image_bytes: str):
        current_time = datetime.datetime.now()
        # check if the current day pic is already done
        if current_time.time() > self._day_pic_time:
            if self.last_day_saved is None or self.last_day_saved != current_time.date():
                # write to the daily photo
                print("storing photo for timelapse")
                cv2.imwrite(f"{self._base_dir}/timelapse/{current_time.isoformat()}.jpg", image_bytes)
                self.last_day_saved = current_time.date()

    def list_all_images(self) -> List[str]:
        file_list = os.listdir(self._base_dir+"/timelapse")
        img_files = []
        for f in file_list:
            if f.find(".jpg") != -1:
                img_files.append(f)

        return img_files

    def list_img_dates(self):
        img_files = self.list_all_images()
        dates = []
        for f in img_files:
            iso_string = f.split("_")[0]
            img_date = datetime.datetime.fromisoformat(iso_string)
            dates.append(img_date)
        return img_date

    def json(self):
        return {
            "timelapse_photos": [],
            "path": self._base_dir
        }