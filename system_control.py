import os
import ctypes

try:
    from pycaw.pycaw import AudioUtilities
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False

try:
    import keyboard
except ImportError:
    pass

def set_volume(level):
    """Set system volume level (0.0 to 1.0)"""
    if not PYCAW_AVAILABLE: return False
    try:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume
        # Volume level is a scalar from 0.0 to 1.0 where 0.0 is mute and 1.0 is max
        volume.SetMasterVolumeLevelScalar(max(0.0, min(1.0, level)), None)
        return True
    except Exception as e:
        print(f"Error setting volume: {e}")
        return False

def get_volume():
    """Get system volume level (0.0 to 1.0)"""
    if not PYCAW_AVAILABLE: return 0.5
    try:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume
        return volume.GetMasterVolumeLevelScalar()
    except Exception as e:
        print(f"Error getting volume: {e}")
        return 0.5

def mute_volume():
    """Mute system volume"""
    if not PYCAW_AVAILABLE: return False
    try:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume
        volume.SetMute(1, None)
        return True
    except Exception as e:
        print(f"Error muting volume: {e}")
        return False

def lock_screen():
    """Lock the Windows workstation"""
    try:
        ctypes.windll.user32.LockWorkStation()
        return True
    except Exception as e:
        print(f"Error locking screen: {e}")
        return False

def media_play_pause():
    try:
        keyboard.send("play/pause media")
        return True
    except:
        return False

def media_next():
    try:
        keyboard.send("next track")
        return True
    except:
        return False

def media_prev():
    try:
        keyboard.send("previous track")
        return True
    except:
        return False
