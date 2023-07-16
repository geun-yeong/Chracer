from minidump.minidumpfile import MinidumpFile

from chracer.validator import *
from chracer.interface import ChromiumInstanceInterface
from chracer.std import *
from chracer.time import *

class Profile(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0x218

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="ProfileImpl"]')
    
    def __getattr__(self, name):
        if name == 'path':
            return U16String(self._mdmp, self._path.va)
        if name == 'path_creation_time':
            return Time(convert_int(self._read_field(self._path_creation_time)))
        if name == 'io_task_runner':
            return convert_int(self._read_field(self._io_task_runner))
        if name == 'schema_registry_service':
            return convert_int(self._read_field(self._schema_registry_service))
        if name == 'user_cloud_policy_manager':
            return convert_int(self._read_field(self._user_cloud_policy_manager))
        if name == 'profile_policy_connector':
            return convert_int(self._read_field(self._profile_policy_connector))
        if name == 'pref_registry':
            return convert_int(self._read_field(self._pref_registry)) 
        if name == 'prefs':
            return convert_int(self._read_field(self._prefs))
        if name == 'dummy_otr_prefs':
            return convert_int(self._read_field(self._dummy_otr_prefs))
        if name == 'extension_special_storage_policy':
            return convert_int(self._read_field(self._extension_special_storage_policy))
        if name == 'otr_profiles':
            return convert_int(self._read_field(self._otr_profiles))
        if name == 'start_time':
            return Time(convert_int(self._read_field(self._start_time)))
        if name == 'key':
            return convert_int(self._read_field(self._key))
        if name == 'media_device_id_salt':
            return convert_int(self._read_field(self._media_device_id_salt))
        if name == 'delegate':
            return convert_int(self._read_field(self._delegate))
    
    def validate(self, debug=False):
        try:
            assert self.path.validate(debug), "INVALID std::string (path)"
            assert validate_pointer(self._mdmp, self.io_task_runner, False), "INVALID POINTER VALUE (io_task_runner)"
            assert validate_pointer(self._mdmp, self.schema_registry_service, False), "INVALID POINTER VALUE (schema_registry_service)"
            assert validate_pointer(self._mdmp, self.user_cloud_policy_manager, False), "INVALID POINTER VALUE (user_cloud_policy_manager)"
            assert validate_pointer(self._mdmp, self.profile_policy_connector, False), "INVALID POINTER VALUE (profile_policy_connector)"
            assert validate_pointer(self._mdmp, self.pref_registry, False), "INVALID POINTER VALUE (pref_registry)" 
            assert validate_pointer(self._mdmp, self.prefs, False), "INVALID POINTER VALUE (prefs)"
            assert validate_pointer(self._mdmp, self.dummy_otr_prefs), "INVALID POINTER VALUE (dummy_otr_prefs)"
            assert validate_pointer(self._mdmp, self.extension_special_storage_policy), "INVALID POINTER VALUE (extension_special_storage_policy)"
            assert validate_pointer(self._mdmp, self.key, False), "INVALID POINTER VALUE (key)"
            assert validate_pointer(self._mdmp, self.media_device_id_salt, False), "INVALID POINTER VALUE (media_device_id_salt)"
            assert validate_pointer(self._mdmp, self.delegate, False), "INVALID POINTER VALUE (delegate)"
        except Exception as e:
            if debug: print('Profile -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True

class OffTheRecordProfile(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0x13C

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="OffTheRecordProfileImpl"]')
    
    def __getattr__(self, name):
        if name == 'profile':
            return convert_int(self._read_field(self._profile))
        if name == 'profile_keep_alive':
            return convert_int(self._read_field(self._profile_keep_alive))
        if name == 'otr_profile_id':
            return U8String(self._mdmp, self._otr_profile_id.va)
        if name == 'prefs':
            return convert_int(self._read_field(self._prefs))
        if name == 'track_zoom_subscription':
            return convert_int(self._read_field(self._track_zoom_subscription))
        if name == 'parent_default_zoom_level_subscription':
            return convert_int(self._read_field(self._parent_default_zoom_level_subscription))
        if name == 'start_time':
            return Time(self._start_time)
        if name == 'key':
            return convert_int(self._read_field(self._key))
        if name == 'last_selected_directory':
            return U8String(self._mdmp, self._last_selected_directory.va)
        if name == 'main_frame_navigations':
            return convert_int(self._read_field(self._main_frame_navigations))
        
    def validate(self, debug=False):
        try:
            assert validate_pointer(self._mdmp, self.profile, False), "INVALID POINTER VALUE (profile)"
            assert validate_pointer(self._mdmp, self.profile_keep_alive, False), "INVALID POINTER VALUE (profile_keep_alive)"
            assert self.otr_profile_id.validate(debug), "INVALID std::string (otr_profile_id)"
            assert validate_pointer(self._mdmp, self.prefs, False), "INVALID POINTER VALUE (prefs)"
            assert validate_pointer(self._mdmp, self.key, False), "INVALID POINTER VALUE (key)"
            assert self.last_selected_directory.validate(debug), "INVALID std::string (last_selected_directory)"
        except Exception as e:
            if debug: print('OffTheRecordProfile -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True
