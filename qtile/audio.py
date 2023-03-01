# holy shit i dont believe this
# I wrote my own audio mixer (KEKW)
# For use with Qtile tiling manager


import subprocess as sh
# TODO : add function to switch devices and print status
class my_audio_mixer:
    
    def __init__(self) -> None:
        self.sinks = []
        self.sources = []
        self.master_sink = None
        self.master_source = None
        self.load_config()
        # self.set_master_dev() # needs to find its purpose
    
    def pactl_get(self,tokens):
        res = sh.run(tokens,capture_output=True,check=True).stdout
        res = res.decode('ASCII').replace('\t','')
        if "Name: " in res:
            out =  res.split("Name: ")[1:]
            return [dev[:-1] for dev in out]
        else:
            return res[:-1]
    
    def load_config(self):
        """
        grabs the default audio drivers.
        TODO: maybe useful to add flexibility and change the default source and sink
        """
        get_DefSink = ['pactl', 'get-default-sink']
        get_DefSrce = ['pactl', 'get-default-source']

        self.master_sink = self.pactl_get(get_DefSink)
        self.master_source = self.pactl_get(get_DefSrce)
    
    def set_master_dev(self):
        pass

    def set_master_sink_volume(self, volume: int):
        # 'pactl set-sink-volume alsa_output.pci-0000_00_1f.3.analog-stereo +10%'
        set_cmd = ('pactl',
                    'set-sink-volume',
                    self.master_sink, 
                    str(volume)+'%')
        sh.run(set_cmd,shell=True)

    def set_master_source_volume(self, volume: int):
        # 'pactl set-source-volume alsa_output.pci-0000_00_1f.3.analog-stereo +10%'
        set_cmd = ['pactl',
                    'set-source-volume',
                    self.master_source,
                    str(volume)+'%']
        sh.run(set_cmd,check=True)

    def get_master_sink_volume(self):
        # 'pactl get-sink-volume alsa_output.pci-0000_00_1f.3.analog-stereo +10%'
        get_cmd = ['pactl',
                    'get-sink-volume',
                    self.master_sink]
        res = sh.run(get_cmd,check=True,capture_output=True).stdout.decode('ASCII')
        res = res.split('/')[1].replace(' ','').replace('%','')
        res = int(res)
        return res

    def get_master_source_volume(self):
        # 'pactl get-source-volume alsa_output.pci-0000_00_1f.3.analog-stereo +10%'
        get_cmd = ('pactl',
                    'get-source-volume',
                    self.master_source )
        res = sh.run(get_cmd,check=True,capture_output=True).stdout.decode('ASCII')
        res = res.split('/')[1].replace(' ','').replace('%','')
        res = int(res)
        return res
    
    def delta_master_sink_volume(self,incr:bool, delta_volume: int = 2):
        # 'pactl set-sink-volume alsa_output.pci-0000_00_1f.3.analog-stereo +10%'
        oper = '+' if incr else '-'
        set_cmd = ('pactl',
                    'set-sink-volume',
                    self.master_sink, 
                    oper+str(delta_volume)+'%')
        vol = self.get_master_sink_volume()
        if vol <= 99 and incr:
            sh.run(set_cmd,check=True)
        elif not incr:
            sh.run(set_cmd,check=True)

    def delta_master_source_volume(self,incr:bool, delta_volume: int = 2):
        # 'pactl set-source-volume alsa_output.pci-0000_00_1f.3.analog-stereo +10%'
        oper = '+' if incr else '-'
        set_cmd = ('pactl',
                    'set-source-volume',
                    self.master_source,
                    oper+str(delta_volume)+'%')
        sh.run(set_cmd,check=True)
    
    def enable_sink(self):
        set_cmd = ('pactl', 
                    'set-sink-mute',
                    self.master_sink,
                    'toggle')
        sh.run(set_cmd,check=True)


if __name__ == '__main__':        
    am = my_audio_mixer()
    am.set_master_sink_volume(39)
    am.delta_master_sink_volume(True)
    am.delta_master_sink_volume(False)
    am.delta_master_sink_volume(False)
    # am.enable_sink()

    res = am.get_master_sink_volume()
    print(res)
    res = am.get_master_source_volume()
    print(res)


    print("-"*10)
    print(am.sinks)
    print(am.sources)
    print("-"*10)


