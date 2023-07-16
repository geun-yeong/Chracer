from enum import Enum
from minidump.minidumpfile import MinidumpFile

from chracer.interface import ChromiumInstanceInterface, Field
from chracer.tab import *
from chracer.std import *
from chracer.time import *
from chracer.gfx import *

class EdgeBrowserCreateParams(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0x128

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)

        self._type = Field(va, 0, 4, 'type')
        self._profile = Field(va, 0x10, 8, 'profile')
        self._trusted_source = Field(va, 0x20, 1, 'trusted_source')
        self._omit_from_session_restore = Field(va, 0x21, 1, 'omit_from_session_restore')
        self._should_trigger_session_restore = Field(va, 0x22, 1, 'should_trigger_session_restore')
        self._initial_bounds = Field(va, 0x24, 16, 'initial_bounds')
        self._can_resize = Field(va, 0x118, 1, 'can_resize')
        self._can_maximize = Field(va, 0x119, 1, 'can_maximize')
        self._initial_aspect_ratio = Field(va, 0x124, 4, 'initial_aspect_ratio')

    
    @property
    def type(self): return EdgeBrowser.Type(convert_int(self._read_field(self._type)))
    @property
    def profile(self): return convert_int(self._read_field(self._profile))
    @property
    def trusted_source(self): return convert_bool(self._read_field(self._trusted_source))
    @property
    def omit_from_session_restore(self): return convert_bool(self._read_field(self._omit_from_session_restore))
    @property
    def should_trigger_session_restore(self): return convert_bool(self._read_field(self._should_trigger_session_restore))
    @property
    def initial_bounds(self): return Rect(self._mdmp, self._initial_bounds.va)
    @property
    def can_resize(self): return convert_bool(self._read_field(self._can_resize))
    @property
    def can_maximize(self): return convert_bool(self._read_field(self._can_maximize))
    @property
    def initial_aspect_ratio(self): return convert_float(self._read_field(self._initial_aspect_ratio))

    def validate(self, debug=False):
        try:
            assert self.type.value < 6, 'INVALID Type (type)'
            assert validate_pointer(self._mdmp, self.profile, False), 'INVALID POINTER VALUE (profile)'
            assert validate_rw_page(self._mdmp, self.profile), 'INVALID POINTER VALUE (profile is not heap)'
            assert validate_boolean(convert_int(self._read_field(self._trusted_source))), 'INVALID bool (trusted_source)'
            assert validate_boolean(convert_int(self._read_field(self._omit_from_session_restore))), 'INVALID bool (omit_from_session_restore)'
            assert validate_boolean(convert_int(self._read_field(self._should_trigger_session_restore))), 'INVALID bool (should_trigger_session_restore)'
            assert self.initial_bounds.validate(debug), 'INVALID gfx::Rect (initial_bounds)'
            assert validate_boolean(convert_int(self._read_field(self._can_resize))), 'INVALID bool (can_resize)'
            assert validate_boolean(convert_int(self._read_field(self._can_maximize))), 'INVALID bool (can_maximize)'
            assert self.initial_aspect_ratio > 0.0, 'INVALID float (initial_aspect_ratio)'
        except Exception as e:
            if debug: print('EdgeBrowserCreateParams -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True

class EdgeBrowser(ChromiumInstanceInterface):
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

        self._create_params = Field(va, 0x128, 0, 'create_params')
        self._type = Field(va, 0x2D0, 4, 'type')
        self._profile = Field(va, 0x2E0, 8, 'profile')
        self._profile_keep_alive = Field(va, 0x2E8, 8, 'profile_keep_alive')
        self._window = Field(va, 0x2F0, 8, 'window')
        self._tab_strip_model_delegate = Field(va, 0x2F8, 8, 'tab_strip_model_delegate')
        self._tab_strip_model = Field(va, 0x300, 8, 'tab_strip_model')
        self._tab_menu_model_delegate = Field(va, 0x308, 8, 'tab_menu_model_delegate')
        self._app_name = Field(va, 0x310, 24, 'app_name')
        self._is_trusted_source = Field(va, 0x328, 1, 'is_trusted_source')
        self._session_id = Field(va, 0x32C, 4, 'session_id')
        self._omit_from_session_restore = Field(va, 0x330, 1, 'omit_from_session_restore')
        self._should_trigger_session_restore = Field(va, 0x331, 1, 'should_trigger_session_restore')
        self._location_bar_model = Field(va, 0x338, 8, 'location_bar_model')
        self._window_has_shown = Field(va, 0x508, 1, 'window_has_shown')
        self._user_title = Field(va, 0x510, 24, 'user_title')
    
    @property
    def create_params(self): return EdgeBrowserCreateParams(self._mdmp, self._create_params.va)
    @property
    def type(self): return self.Type(convert_int(self._read_field(self._type)))
    @property
    def profile(self): return convert_int(self._read_field(self._profile))
    @property
    def tab_strip_model(self):
        tsm = TabStripModel(self._mdmp, convert_int(self._read_field(self._tab_strip_model)))
        tsm._tab_strip_ui_was_set = Field(tsm.base, 0x38, 1, 'tab_strip_ui_was_set')
        tsm._closing_all = Field(tsm.base, 0xD0, 1, 'closing_all')
        tsm._reentrancy_guard = Field(tsm.base, 0x138, 1, 'reentrancy_guard')
        return tsm
    @property
    def session_id(self): return convert_int(self._read_field(self._session_id))
    @property
    def user_title(self): return U8String(self._mdmp, self._user_title.va)

    def validate(self, debug=False):
        try:
            assert self.create_params.validate(debug), 'INVALID EdgeBrowserCreateParams (create_params)'
            assert self.create_params.profile == self.profile, 'INVALID POINTER VALUE (it is not same to create_params.profile)'
            assert self.type.value < 6, 'INVALID Type (type)'
            assert validate_pointer(self._mdmp, self.profile, False), 'INVALID POINTER VALUE (profile)'
            assert validate_rw_page(self._mdmp, self.profile), 'INVALID POINTER VALUE (profile is not heap)'
            assert validate_pointer(self._mdmp, self.tab_strip_model.base, False), 'INVALID POINTER VALUE (tab_strip_model)'
            assert validate_rw_page(self._mdmp, self.tab_strip_model.base), 'INVALID POINTER VALUE (tab_strip_model)'
            assert self.tab_strip_model.validate(debug), 'INVALID TabStripModel (tab_strip_model)'
            assert self.session_id > 0, 'INVALID SessionID (session_id)'
            assert self.user_title.validate(debug), 'INVALID U8String (user_title)'
            assert validate_boolean(convert_int(self._read_field(self._is_trusted_source))), 'INVALID bool (is_trusted_source)'
            assert validate_boolean(convert_int(self._read_field(self._omit_from_session_restore))), 'INVALID bool (omit_from_session_restore)'
            assert validate_boolean(convert_int(self._read_field(self._should_trigger_session_restore))), 'INVALID bool (should_trigger_session_restore)'
            assert validate_boolean(convert_int(self._read_field(self._window_has_shown))), 'INVALID bool (window_has_shown)'
            assert convert_bool(self._read_field(self._window_has_shown)) == True, 'INVALID bool (window_has_shown is not true)'
        except Exception as e:
            if debug: print('EdgeBrowser -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True
    


class EdgeTab(ChromiumInstanceInterface):
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
    def contents(self): return EdgeWebContents(self._mdmp, convert_int(self._read_field(self._contents)))
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
            assert validate_boolean(convert_int(self._read_field(self._reset_opener_on_active_tab_change))), "INVALID bool (reset_opener_on_active_tab_change)"
            assert validate_boolean(convert_int(self._read_field(self._pinned))), "INVALID bool (pinned)"
            assert validate_boolean(convert_int(self._read_field(self._blocked))), "INVALID bool (blocked)"
        except Exception as e:
            if debug: print('EdgeTab -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class EdgeWebContents(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)

        self._primary_frame_tree = Field(va, 0x180, 1800, 'primary_frame_tree')
    
    @property
    def primary_frame_tree(self): return FrameTree(self._mdmp, self._primary_frame_tree.va)

    def validate(self, debug=False):
        try:
            self.primary_frame_tree.validate(debug), 'INVALID FrameTree (primary_frame_tree)'
        except Exception as e:
            if debug: print('EdgeWebContents -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class EdgeNavigationEntry(ChromiumInstanceInterface):
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
            return EdgeFrameNavigationEntry(self._mdmp, _)
    
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
        #self._favicon = Field(va, 0xC8, 136, 'favicon')
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

    def validate(self, debug=False):
        try:
            assert validate_pointer(self._mdmp, convert_int(self._read_field(self._frame_tree)), False), 'INVALID POINTER VALUE (frame_tree)'
            assert validate_rw_page(self._mdmp, convert_int(self._read_field(self._frame_tree))), 'INVALID POINTER VALUE (frame_tree is not heap)'
            assert self.frame_tree.validate(debug), 'INVLAID TreeNode (frame_tree)'
            assert self.unique_id > 0, 'INVALID integer (unique_id)'
            assert self.virtual_url.validate(debug), 'INVALID GURL (virtual_url)'
            assert self.title.validate(debug), 'INVALID U16String (title)'
            assert self.timestamp.validate(debug=debug), 'INVALID base::Time (timestamp)'
            assert self.user_typed_url.validate(debug), 'INVALID GURL (user_typed_url)'
            assert self.original_request_url.validate(debug), 'INVALID GURL (original_request_url)'
            assert self.http_status_code >= 200, 'INVALID integer (http_status_code)'
        except Exception as e:
            if debug: print('EdgeNavigationEntry -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class EdgeFrameNavigationEntry(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0x351

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        
        self._url = Field(va, 0x60, 120, 'url')
        self._method = Field(va, 0x2E8, 24, 'method')

    @property
    def url(self):
        return GURL(self._mdmp, self._url.va)
    @property
    def method(self):
        return U8String(self._mdmp, self._method.va)