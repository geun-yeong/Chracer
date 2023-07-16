from minidump.minidumpfile import MinidumpFile
from enum import Enum

from chracer.validator import *
from chracer.interface import ChromiumInstanceInterface
from chracer.gfx import *
from chracer.std import *
from chracer.tab import *
from chracer.profile import *

class BrowserCreateParam(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 168

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="Browser::CreateParams"]')
    
    def __getattr__(self, name):
        if name == 'type':
            return Browser.Type(convert_int(self._read_field(self._type)))
        if name == 'profile':
            return convert_int(self._read_field(self._profile))
        if name == 'trusted_source':
            return convert_bool(self._read_field(self._trusted_source))
        if name == 'omit_from_session_restore':
            return convert_bool(self._read_field(self._omit_from_session_restore))
        if name == 'should_trigger_session_restore':
            return convert_bool(self._read_field(self._should_trigger_session_restore))
        if name == 'initial_bounds':
            return Rect(self._mdmp, self._initial_bounds.va)
        if name == 'initial_origin_specified':
            return Browser.ValueSpecified(convert_int(self._read_field(self._initial_origin_specified)))
        if name == 'initial_workspace':
            return U8String(self._mdmp, self._initial_workspace.va)
        if name == 'initial_visible_on_all_workspaces_state':
            return convert_bool(self._read_field(self._initial_visible_on_all_workspaces_state))
        if name == 'are_tab_groups_enabled':
            return convert_bool(self._read_field(self._are_tab_groups_enabled))
        if name == 'initial_show_state':
            return Browser.WindowShowState(convert_int(self._read_field(self._initial_show_state)))
        if name == 'creation_source':
            return Browser.CreationSource(convert_int(self._read_field(self._creation_source)))
        if name == 'user_gesture':
            return convert_bool(self._read_field(self._user_gesture))
        if name == 'in_tab_dragging':
            return convert_bool(self._read_field(self._in_tab_dragging))
        if name == 'window':
            return convert_int(self._read_field(self._window))
        if name == 'user_title':
            return U8String(self._mdmp, self._user_title.va)
        if name == 'can_resize':
            return convert_bool(self._read_field(self._can_resize))
        if name == 'can_maximize':
            return convert_bool(self._read_field(self._can_maximize))
        if name == 'initial_aspect_ratio':
            return convert_float(self._read_field(self._initial_aspect_ratio))
        if name == 'lock_aspect_ratio':
            return convert_bool(self._read_field(self._lock_aspect_ratio))
        if name == 'app_name':
            return U8String(self._mdmp, self._app_name.va)
        if name == 'skip_window_init_for_testing':
            return convert_bool(self._read_field(self._skip_window_init_for_testing))

    def validate(self, debug=False):
        try:
            assert self.type.value < 6, 'INVALID Type'
            assert validate_pointer(self._mdmp, self.profile, False), 'INVALID POINTER VALUE'
            assert validate_boolean(convert_int(self._read_field((self._trusted_source)))), 'INVALID bool'
            assert validate_boolean(convert_int(self._read_field((self._omit_from_session_restore)))), 'INVALID bool'
            assert validate_boolean(convert_int(self._read_field((self._should_trigger_session_restore)))), 'INVALID bool'
            assert self.initial_bounds.validate(debug), 'INVALID gfx::Rect'
            assert self.initial_origin_specified.value < 3, 'INVALID ValueSpecified value'
            assert self.initial_workspace.validate(debug), 'INVALID std::string'
            assert validate_boolean(convert_int(self._read_field((self._initial_visible_on_all_workspaces_state)))), 'INVALID bool'
            assert validate_boolean(convert_int(self._read_field((self._are_tab_groups_enabled)))), 'INVALID bool'
            assert self.initial_show_state.value < 6, 'INVALID WindowShowState value'
            assert self.creation_source.value < 5, 'INVALID CreationSource value'
            assert validate_boolean(convert_int(self._read_field((self._user_gesture)))), 'INVALID bool'
            assert validate_boolean(convert_int(self._read_field((self._in_tab_dragging)))), 'INVALID bool'
            assert validate_pointer(self._mdmp, self.window), 'INVALID POINTER VALUE'
            assert self.user_title.validate(debug), 'INVALID std::string'
            assert validate_boolean(convert_int(self._read_field((self._can_resize)))), 'INVALID bool'
            assert validate_boolean(convert_int(self._read_field((self._can_maximize)))), 'INVALID bool'
            assert validate_boolean(convert_int(self._read_field((self._lock_aspect_ratio)))), 'INVALID bool'
            assert self.app_name.validate(debug), 'INVALID std::string'
            assert validate_boolean(convert_int(self._read_field((self._skip_window_init_for_testing)))), 'INVALID bool'
        except Exception as e:
            if debug: print('Browser::CreateParams -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class Browser(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 1112

    class Type(Enum):
        TYPE_NORMAL = 0
        TYPE_POPUP = 1
        TYPE_APP = 2
        TYPE_DEVTOOLS = 3
        TYPE_APP_POPUP = 4
        TYPE_PICTURE_IN_PICTURE = 5
    
    class ValueSpecified(Enum):
        kUnknown = 0
        kSpecified = 1
        kUnspecified = 2
    
    class WindowShowState(Enum):
        SHOW_STATE_DEFAULT = 0
        SHOW_STATE_NORMAL = 1
        SHOW_STATE_MINIMIZED = 2
        SHOW_STATE_MAXIMIZED = 3
        SHOW_STATE_INACTIVE = 4
        SHOW_STATE_FULLSCREEN = 5
        SHOW_STATE_END = 6
    
    class CreationSource(Enum):
        kUnknown = 0
        kSessionRestore = 1
        kStartupCreator = 2
        kLastAndUrlsStartupPref = 3
        kDeskTemplate = 4
    
    class CancelDownloadConfirmationState(Enum):
        NOT_PROMPTED = 0
        WAITING_FOR_RESPONSE = 1
        RESPONSE_RECEIVED = 2
    
    class BookmarkBarState(Enum):
        HIDDEN = 0
        SHOW = 1

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="Browser"]')

    def __getattr__(self, name):
        if name == 'create_params':
            return BrowserCreateParam(self._mdmp, self._create_params.va)
        if name == 'type':
            return self.Type(convert_int(self._read_field(self._type)))
        if name == 'profile':
            _ = convert_int(self._read_field(self._profile))
            if Profile(self._mdmp, _).validate(): return Profile(self._mdmp, _)
            if OffTheRecordProfile(self._mdmp, _).validate(): return OffTheRecordProfile(self._mdmp, _)
            return None
        if name == 'profile_keep_alive':
            return convert_int(self._read_field(self._profile_keep_alive))
        if name == 'window':
            return convert_int(self._read_field(self._window))
        if name == 'tab_strip_model_delegate':
            return convert_int(self._read_field(self._tab_strip_model_delegate))
        if name == 'tab_strip_model':
            return TabStripModel(self._mdmp, convert_int(self._read_field(self._tab_strip_model)))
        if name == 'tab_menu_model_delegate':
            return convert_int(self._read_field(self._tab_menu_model_delegate))
        if name == 'app_name':
            return U8String(self._mdmp, self._app_name.va)
        if name == 'is_trusted_source':
            return convert_bool(self._read_field(self._is_trusted_source))
        if name == 'session_id':
            return convert_int(self._read_field(self._session_id))
        if name == 'omit_from_session_restore':
            return convert_bool(self._read_field(self._omit_from_session_restore))
        if name == 'should_trigger_session_restore':
            return convert_bool(self._read_field(self._should_trigger_session_restore))
        if name == 'cancel_download_confirmation_state':
            return self.CancelDownloadConfirmationState(convert_int(self._read_field(self._cancel_download_confirmation_state)))
        if name == 'override_bounds':
            return Rect(self._mdmp, self._override_bounds.va)
        if name == 'initial_show_state':
            return self.WindowShowState(convert_int(self._read_field(self._initial_show_state)))
        if name == 'initial_workspace':
            return U8String(self._mdmp, self._initial_workspace.va)
        if name == 'initial_visible_on_all_workspaces_state':
            return convert_int(self._read_field(self._initial_visible_on_all_workspaces_state))
        if name == 'creation_source':
            return self.CreationSource(convert_int(self._read_field(self._creation_source)))
        if name == 'find_bar_controller':
            return convert_int(self._read_field(self._find_bar_controller))
        if name == 'select_file_dialog':
            return convert_int(self._read_field(self._select_file_dialog))
        if name == 'content_setting_bubble_model_delegate':
            return convert_int(self._read_field(self._content_setting_bubble_model_delegate))
        if name == 'location_bar_model':
            return convert_int(self._read_field(self._location_bar_model))
        if name == 'live_tab_context':
            return convert_int(self._read_field(self._live_tab_context))
        if name == 'synced_window_delegate':
            return convert_int(self._read_field(self._synced_window_delegate))
        if name == 'instant_controller':
            return convert_int(self._read_field(self._instant_controller))
        if name == 'app_controller':
            return convert_int(self._read_field(self._app_controller))
        if name == 'bookmark_bar_state':
            return self.BookmarkBarState(convert_int(self._read_field(self._bookmark_bar_state)))
        if name == 'exclusive_access_manager':
            return convert_int(self._read_field(self._exclusive_access_manager))
        if name == 'extension_window_controller':
            return convert_int(self._read_field(self._extension_window_controller))
        if name == 'command_controller':
            return convert_int(self._read_field(self._command_controller))
        if name == 'window_has_shown':
            return convert_bool(self._read_field(self._window_has_shown))
        if name == 'user_title':
            return U8String(self._mdmp, self._user_title.va)
        if name == 'breadcrumb_manager_browser_agent':
            return convert_int(self._read_field(self._breadcrumb_manager_browser_agent))
        if name == 'keep_alive':
            return convert_int(self._read_field(self._keep_alive))
        if name == 'warn_before_closing_callback':
            return convert_int(self._read_field(self._warn_before_closing_callback))
        if name == 'force_skip_warning_user_on_close':
            return convert_bool(self._read_field(self._force_skip_warning_user_on_close))
        if name == 'extension_browser_window_helper':
            return convert_int(self._read_field(self._extension_browser_window_helper))
        if name == 'creation_timer':
            return TimeTicks(convert_int(self._read_field(self._creation_timer)))
        if name == 'opener_browser':
            return convert_int(self._read_field(self._opener_browser))
        return None

    def validate(self, debug=False):
        try:
            assert self.create_params.validate(debug), 'INVALID Browser::CreateParams'
            assert self.type.value < 6, 'INVALID Type'
            assert validate_pointer(self._mdmp, convert_int(self._read_field(self._profile)), False), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.profile_keep_alive), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.window, False), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.tab_strip_model_delegate), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, convert_int(self._read_field(self._tab_strip_model)), False), 'INVALID POINTER VALUE'
            assert self.tab_strip_model.validate(debug), 'INVALID TabStripModel'
            assert validate_pointer(self._mdmp, self.tab_menu_model_delegate), 'INVALID POINTER VALUE'
            assert self.app_name.validate(debug), 'INVALID std::string'
            assert validate_boolean(convert_int(self._read_field(self._is_trusted_source))), 'INVALID bool'
            assert self.session_id > 0, 'INVALID SessionID'
            assert validate_boolean(convert_int(self._read_field(self._omit_from_session_restore))), 'INVALID bool'
            assert validate_boolean(convert_int(self._read_field(self._should_trigger_session_restore))), 'INVALID bool'
            assert validate_pointer(self._mdmp, self.location_bar_model), 'INVALID POINTER VALUE'
            assert self.cancel_download_confirmation_state.value < 3, 'INVALID CancelDownloadConfirmationState'
            assert self.override_bounds.validate(debug), 'INVALID gfx::Rect'
            assert self.initial_show_state.value < 6, 'INVALID WindowShowState value'
            assert self.initial_workspace.validate(debug), 'INVALID std::string'
            assert validate_boolean(convert_int(self._read_field(self._initial_visible_on_all_workspaces_state))), 'INVALID bool'
            assert self.creation_source.value < 5, 'INVALID CreationSource value'
            assert validate_pointer(self._mdmp, self.find_bar_controller), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.select_file_dialog), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.content_setting_bubble_model_delegate), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.location_bar_model), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.live_tab_context, False), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.synced_window_delegate), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.instant_controller), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.app_controller), 'INVALID POINTER VALUE'
            assert self.bookmark_bar_state.value < 2, 'it is invlaid BookmarkBar::State value'
            assert validate_pointer(self._mdmp, self.exclusive_access_manager), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.extension_window_controller), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.command_controller), 'INVALID POINTER VALUE'
            assert validate_boolean(convert_int(self._read_field(self._window_has_shown))), 'INVALID bool'
            assert self.user_title.validate(debug), 'INVALID std::string'
            assert validate_pointer(self._mdmp, self.breadcrumb_manager_browser_agent), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.keep_alive), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.warn_before_closing_callback), 'INVALID POINTER VALUE'
            assert validate_boolean(convert_int(self._read_field(self._force_skip_warning_user_on_close))), 'INVALID bool'
            assert validate_pointer(self._mdmp, self.extension_browser_window_helper), 'INVALID POINTER VALUE'
            assert validate_pointer(self._mdmp, self.opener_browser), 'INVALID POINTER VALUE'
        except Exception as e:
            if debug: print('Browser -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True