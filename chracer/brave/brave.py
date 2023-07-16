from enum import Enum
from minidump.minidumpfile import MinidumpFile

from chracer.interface import ChromiumInstanceInterface, Field
from chracer.tab import *
from chracer.std import *
from chracer.time import *
from chracer.gfx import *

class BraveBrowser(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0x398

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

        #self._create_params = Field(va, 0x138, 160, 'create_params')
        self._type = Field(va, 0x1B8, 4, 'type')
        self._profile = Field(va, 0x1C0, 8, 'profile')
        self._profile_keep_alive = Field(va, 0x1C8, 8, 'profile_keep_alive')
        self._window = Field(va, 0x1D0, 8, 'window')
        self._tab_strip_model_delegate = Field(va, 0x1D8, 8, 'tab_strip_model_delegate')
        self._tab_strip_model = Field(va, 0x1E0, 8, 'tab_strip_model')
        self._tab_menu_model_delegate = Field(va, 0x1E8, 8, 'tab_menu_model_delegate')
        self._app_name = Field(va, 0x1F0, 24, 'app_name')
        self._is_trusted_source = Field(va, 0x208, 1, 'is_trusted_source')
        self._session_id = Field(va, 0x20C, 4, 'session_id')
        self._omit_from_session_restore = Field(va, 0x210, 1, 'omit_from_session_restore')
        self._should_trigger_session_restore = Field(va, 0x211, 1, 'should_trigger_session_restore')
        self._location_bar_model = Field(va, 0x218, 8, 'location_bar_model')
        self._scheduled_updates = Field(va, 0x220, 24, 'scheduled_updates')
        self._cancel_download_confirmation_state = Field(va, 0x238, 4, 'cancel_download_confirmation_state')
        self._override_bounds = Field(va, 0x23C, 16, 'override_bounds')
        self._initial_show_state = Field(va, 0x24C, 4, 'initial_show_state')
        self._initial_workspace = Field(va, 0x250, 24, 'initial_workspace')
        self._initial_visible_on_all_workspace = Field(va, 0x268, 1, 'initial_visible_on_all_workspaces_state')
        self._creation_source = Field(va, 0x26C, 4, 'creation_source')
        self._find_bar_controller = Field(va, 0x310, 8, 'find_bar_controller')
        self._location_bar_model_delegate = Field(va, 0x328, 8, 'location_bar_model_delegate')
        self._live_tab_context = Field(va, 0x330, 8, 'live_tab_context')
        self._synced_window_delegate = Field(va, 0x338, 8, 'synced_window_delegate')
        self._instant_controller = Field(va, 0x340, 8, 'instant_controller')
        self._bookmark_bar_state = Field(va, 0x358, 4, 'bookmark_bar_state')
        self._exclusive_access_manager = Field(va, 0x360, 8, 'exclusive_access_manager')
        self._extension_window_controller = Field(va, 0x368, 8, 'extension_window_controller')
        self._command_controller = Field(va, 0x370, 8, 'command_controller')
        self._window_has_shown = Field(va, 0x378, 1, 'window_has_shown')
        self._user_title = Field(va, 0x380, 24, 'user_title')
    
    @property
    def type(self): return self.Type(convert_int(self._read_field(self._type)))
    @property
    def profile(self): return convert_int(self._read_field(self._profile))
    @property
    def profile_keep_alive(self): return convert_int(self._read_field(self._profile_keep_alive))
    @property
    def window(self): return convert_int(self._read_field(self._window))
    @property
    def tab_strip_model_delegate(self): return convert_int(self._read_field(self._tab_strip_model_delegate))
    @property
    def tab_strip_model(self): return TabStripModel(self._mdmp, convert_int(self._read_field(self._tab_strip_model)))
    @property
    def tab_menu_model_delegate(self): return convert_int(self._read_field(self._tab_menu_model_delegate))
    @property
    def app_name(self): return U8String(self._mdmp, self._app_name.va)
    @property
    def is_trusted_source(self): return convert_bool(self._read_field(self._is_trusted_source))
    @property
    def session_id(self): return convert_int(self._read_field(self._session_id))
    @property
    def omit_from_session_restore(self): return convert_bool(self._read_field(self._omit_from_session_restore))
    @property
    def should_trigger_session_restore(self): return convert_bool(self._read_field(self._should_trigger_session_restore))
    @property
    def location_bar_model(self): return convert_int(self._read_field(self._location_bar_model))
    @property
    def cancel_download_confirmation_state(self): return self.CancelDownloadConfirmationState(convert_int(self._read_field(self._cancel_download_confirmation_state)))
    @property
    def override_bounds(self): return Rect(self._mdmp, self._override_bounds.va)
    @property
    def initial_show_state(self): return self.WindowShowState(convert_int(self._read_field(self._initial_show_state)))
    @property
    def initial_workspace(self): return U8String(self._mdmp, self._initial_workspace.va)
    @property
    def initial_visible_on_all_workspaces_state(self): return convert_bool(self._read_field(self._initial_visible_on_all_workspace))
    @property
    def creation_source(self): return self.CreationSource(convert_int(self._read_field(self._creation_source)))
    @property
    def find_bar_controller(self): return convert_int(self._read_field(self._find_bar_controller))
    @property
    def location_bar_model_delegate(self): return convert_int(self._read_field(self._location_bar_model_delegate))
    @property
    def live_tab_context(self): return convert_int(self._read_field(self._live_tab_context))
    @property
    def synced_window_delegate(self): return convert_int(self._read_field(self._synced_window_delegate))
    @property
    def instant_controller(self): return convert_int(self._read_field(self._instant_controller))
    @property
    def bookmark_bar_state(self): return self.BookmarkBarState(convert_int(self._read_field(self._bookmark_bar_state)))
    @property
    def exclusive_access_manager(self): return convert_int(self._read_field(self._exclusive_access_manager))
    @property
    def extension_window_controller(self): return convert_int(self._read_field(self._extension_window_controller))
    @property
    def command_controller(self): return convert_int(self._read_field(self._command_controller))
    @property
    def window_has_shown(self): return convert_bool(self._read_field(self._window_has_shown))
    @property
    def user_title(self): return U8String(self._mdmp, self._user_title.va)

    def validate(self, debug=False):
        try:
            assert self.type.value < 6, "INVALID Type (type)"
            assert validate_pointer(self._mdmp, self.profile, False), "INVALID POINTER VALUE (profile)"
            assert validate_rw_page(self._mdmp, self.profile), "INVALID PAGE (profile)"
            assert validate_pointer(self._mdmp, self.window, False), 'INVALID POINTER VALUE (window)'
            assert validate_rw_page(self._mdmp, self.window), "INVALID PAGE (window)"
            assert self.tab_strip_model.validate(debug), "INVALID TabStripModel (tab_strip_model)"
            assert self.app_name.validate(debug), "INVALID std::string (app_name)"
            assert validate_boolean(convert_int(self._read_field(self._is_trusted_source))), "INVLAID bool (is_trusted_source)"
            assert self.session_id > 0, "INVALID SessionID (session_id)"
            assert validate_boolean(convert_int(self._read_field(self._should_trigger_session_restore))), "INVLAID bool (should_trigger_session_restore)"
            assert validate_boolean(convert_int(self._read_field(self._omit_from_session_restore))), "INVLAID bool (omit_from_session_restore)"
            assert self.cancel_download_confirmation_state.value < 3, "INVALID CancelDownloadConfirmationState (cancel_download_confirmation_state)"
            assert self.override_bounds.validate(debug), "INVALID gfx::Rect (override_bounds)"
            assert self.initial_show_state.value < 7, "INVALID WindowShowState (initial_show_state)"
            assert self.initial_workspace.validate(debug), "INVALID std::string (initial_workspace)"
            assert validate_boolean(convert_int(self._read_field(self._initial_visible_on_all_workspace))), "INVLAID bool (initial_visible_on_all_workspace)"
            assert self.creation_source.value < 5, "INVALID CreationSource (creation_source)"
            assert validate_pointer(self._mdmp, self.live_tab_context, False), 'INVALID POINTER VALUE (live_tab_context)'
            assert validate_rw_page(self._mdmp, self.live_tab_context), "INVALID PAGE (live_tab_context)"
            assert validate_pointer(self._mdmp, self.instant_controller, False), "INVALID POINTER VALUE (instant_controller)"
            assert validate_rw_page(self._mdmp, self.instant_controller), "INVALID PAGE (instant_controller)"
            assert self.bookmark_bar_state.value < 2, "INVALID BookmarkBarState (bookmark_bar_state)"
            assert validate_pointer(self._mdmp, self.exclusive_access_manager), "INVALID POINTER VALUE (exclusive_access_manager)"
            assert validate_pointer(self._mdmp, self.extension_window_controller), "INVALID POINTER VALUE (extension_window_controller)"
            assert validate_pointer(self._mdmp, self.command_controller), "INVALID POINTER VALUE (command_controller)"
            assert validate_boolean(convert_int(self._read_field(self._window_has_shown))), "INVLAID bool (window_has_shown)"
            assert self.user_title.validate(debug), "INVALID std::string (user_title)"
        except Exception as e:
            if debug: print('BraveBrowser-> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class BraveWebContents(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)

        self._primary_frame_tree = Field(va, 0x1C8 - 0x48, 1800, 'primary_frame_tree')
    
    @property
    def primary_frame_tree(self): return FrameTree(self._mdmp, self._primary_frame_tree.va)



class BraveTab(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 56
    
    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)

        self._contents = Field(va, 0, 8, 'contents')
        self._opener = Field(va, 8, 8, 'opener')
        self._reset_opener_on_active_tab_change = Field(va, 0x10, 1, 'reset_opener_on_active_tab_change')
        self._pinned = Field(va, 0x11, 1, 'pinned')
        self._blocked = Field(va, 0x12, 1, 'blocked')
        self._group = Field(va, 0x18, 32, 'group')
    
    @property
    def contents(self): return BraveWebContents(self._mdmp, convert_int(self._read_field(self._contents)))
    @property
    def reset_opener_on_active_tab_change(self): return convert_bool(self._read_field(self._reset_opener_on_active_tab_change))
    @property
    def pinned(self): return convert_bool(self._read_field(self._pinned))
    @property
    def blocked(self): return convert_bool(self._read_field(self._blocked))
    @property
    def group(self):
        absl_opt = Optional(self._mdmp, self._base+0x18, 16)
        return int.from_bytes(absl_opt.data, 'little') if absl_opt.engaged else 0
    @property
    def grouphex(self):
        absl_opt = Optional(self._mdmp, self._base+0x18, 16)
        return absl_opt.data.hex() if absl_opt.engaged else 0

    def validate(self, debug=False):
        try:
            assert validate_pointer(self._mdmp, convert_int(self._read_field(self._contents)), False), 'INVALID POINTER VALUE (contents)'
            assert validate_rw_page(self._mdmp, convert_int(self._read_field(self._contents))), 'INVALID POINTER VALUE (contents is not heap)'
            assert self.contents.validate(debug), "INVALID WebContents"
            assert validate_boolean(convert_int(self._read_field(self._pinned))), "INVALID bool"
            assert validate_boolean(convert_int(self._read_field(self._blocked))), "INVALID bool"
        except:
            return False
        return True



class BraveNavigationEntry(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0

    class TreeNode(ChromiumInstanceInterface):
        _INSTANCE_LAYOUT = '< QQ24s' # parent, frame_entry, children
        _INSTANCE_SIZE = 40

        def __init__(self, mdmp: MinidumpFile, va: int):
            super().__init__(mdmp, va)

            self._parent = Field(va, 0, 8, 'parent')
            self._frame_entry = Field(va, 8, 8, 'frame_entry')
            self._children = Field(va, 0x10, 24, 'children')
        
        @property
        def frame_entry(self):
            _ = convert_int(self._read_field(self._frame_entry))
            return BraveFrameNavigationEntry(self._mdmp, _)
    
    class PageType(Enum):
        PAGE_TYPE_NORMAL = 0
        PAGE_TYPE_ERROR = 1

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)

        self._frame_tree = Field(va, 0x38, 8, 'frame_tree')
        self._unique_id = Field(va, 0x40, 4, 'unique_id')
        self._page_type = Field(va, 0x44, 4, 'page_type')
        self._virtual_url = Field(va, 0x48, 120, 'virtual_url')
        self._title = Field(va, 0xC8, 24, 'title')
        self._favicon = Field(va, 0xE0, 136, 'favicon')
        self._user_typed_url = Field(va, 0x198, 120, 'user_typed_url')
        self._original_request_url = Field(va, 0x218, 120, 'original_request_url')
        self._timestamp = Field(va, 0x298, 8, 'timestamp')
        self._http_status_code = Field(va, 0x2A0, 4, 'http_status_code')
    
    @property
    def frame_tree(self):
        _ = convert_int(self._read_field(self._frame_tree))
        return self.TreeNode(self._mdmp, _)
    @property
    def unique_id(self): return convert_int(self._read_field(self._unique_id))
    @property
    def page_type(self): return NavigationEntry.PageType(convert_int(self._read_field(self._page_type)))
    @property
    def virtual_url(self): return GURL(self._mdmp, self._virtual_url.va)
    @property
    def title(self): return U16String(self._mdmp, self._title.va)
    @property
    def favicon(self): return FaviconStatus(self._mdmp, self._favicon.va)
    @property
    def user_typed_url(self): return GURL(self._mdmp, self._user_typed_url.va)
    @property
    def original_request_url(self): return GURL(self._mdmp, self._original_request_url.va)
    @property
    def timestamp(self): return Time(convert_int(self._read_field(self._timestamp)))
    @property
    def http_status_code(self): return convert_int(self._read_field(self._http_status_code))



class BraveFrameNavigationEntry(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0x351

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        
        self._url = Field(va, 0x60, 120, 'url')
        self._redirect_chain = Field(va, 0x2B0, 24, 'redirect_chain')
        self._method = Field(va, 0x2E8, 24, 'method')

    @property
    def url(self):
        return GURL(self._mdmp, self._url.va)
    @property
    def redirect_chain(self):
        return Vector(self._mdmp, self._redirect_chain.va, 120)
    @property
    def method(self):
        return U8String(self._mdmp, self._method.va)