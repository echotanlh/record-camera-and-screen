import re
import RunCMD
from RunCMD import run_cmd

class DevicesInfo():

    def __init__(self):
        list_devices_cmd = 'ffmpeg -list_devices true -f dshow -i dummy'
        # status, output = subprocess.getstatusoutput(list_devices_cmd)
        output_err, output_str = run_cmd(list_devices_cmd)
        self.video_devices , self.voice_devices = self.extract_devices_info(''.join(output_err))
        
    def get_device_info(self, text_list):
        device_list = []
        if text_list and len(text_list) % 2 == 0:
            i=0
            while i < len(text_list):
                step = 2 
                device = []
                device_name = text_list[i].strip()
                device.append(device_name.replace('"',''))
                alternative_name_text = text_list[i+1]
                alter_re = re.search(r'"(.+)"',alternative_name_text)
                if alter_re:
                    device_alternative_name = alter_re.group(1)
                    device.append(device_alternative_name)
                device_list.append(device)
                i+=step
        return device_list
        
    def extract_devices_info(self,devices_txt):    
        device_line = []
        # print(dir(re))
        results = re.findall(r'\[[^\]]+\]([^\[]+)',devices_txt)
        # results.pop(0)
        video_devices_spos=-1
        voice_devices_spos=-1
        for i in range(len(results)):
            txt = results[i]
            # print(txt.strip())
            if txt.find('DirectShow video devices') >= 0:
                video_devices_spos = i
            if txt.find('DirectShow audio devices') >=0:
                voice_devices_spos = i  

        video_devices = self.get_device_info(results[video_devices_spos+1:voice_devices_spos])     
        voice_devices = self.get_device_info(results[voice_devices_spos+1:])   

        return video_devices , voice_devices

