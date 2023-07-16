from minidump.minidumpfile import MinidumpFile
from enum import Enum

from chracer.validator import *
from chracer.interface import ChromiumInstanceInterface, Field
from chracer.std import *
from chracer.gfx import *
from chracer.tab import *
from chracer.time import *
from chracer.url import *
from chracer.absl import *
from chracer.common_lib import *



class TabStripModel(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 416

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="TabStripModel"]')
    
    def __getattr__(self, name):
        if name == 'contents_data':
            return Vector(self._mdmp, self._contents_data.va, 8)
        if name == 'group_model':
            return TabGroupModel(self._mdmp, convert_int(self._read_field(self._group_model)))
        if name == 'delegate':
            return convert_int(self._read_field(self._delegate))
        if name == 'tab_strip_ui_was_set':
            return convert_bool(self._read_field(self._tab_strip_ui_was_set))
        if name == 'observers':
            return convert_int(self._read_field(self._observers))
        if name == 'profile':
            return convert_int(self._read_field(self._profile))
        if name == 'closing_all':
            return convert_bool(self._read_field(self._closing_all))
        if name == 'selection_model':
            return ListSelectionMdoel(self._mdmp, self._selection_model.va)
        if name == 'reentrancy_guard':
            return convert_bool(self._read_field(self._reentrancy_guard))
        
    def validate(self, debug=False):
        try:
            assert self.contents_data.validate(debug), "INVALID std::Vector"
            assert self.group_model.validate(debug), "INVALID tab_groups::TabGroupModel"
            assert validate_boolean(convert_int(self._read_field(self._tab_strip_ui_was_set))), "INVALID bool (tab_strip_ui_was_set)"
            assert validate_boolean(convert_int(self._read_field(self._closing_all))), "INVALID bool (closing_all)"
            assert self.selection_model.validate(debug), "INVALID ui::ListSelectionModel"
            assert validate_boolean(convert_int(self._read_field(self._reentrancy_guard))), "INVALID bool (closing_all)"
        except Exception as e:
            if debug: print('TabStripModel -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class TabGroupModel(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 24

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="TabGroupModel"]')
    
    def __getattr__(self, name):
        if name == 'groups':
            return Map(self._mdmp,
                    self._groups.va,
                    16, # TabGroupId 크기
                    8, # unique_ptr<TabGroup> 크기
                    lambda key_data: ''.join(['{:02x}'.format(x) for x in key_data]),
                    lambda value_data: TabGroup(self._mdmp, convert_int(value_data)))



class TabGroupId(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 16

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)

        self._token = Field(va, 0, 16, 'token')

    def __getattr__(self, name):
        if name == 'token':
            return convert_int(self._read_field(self._token))



class TabGroup(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 48

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="TabGroup"]')
    
    def __getattr__(self, name):
        if name == 'id':
            return TabGroupId(self._mdmp, self._id.va)
        if name == 'visual_data':
            return TabGroupVisualData(self._mdmp, convert_int(self._read_field(self._visual_data)))
        if name == 'tab_count':
            return convert_int(self._read_field(self._tab_count), signed=True)
        if name == 'is_customized':
            return convert_bool(self._read_field(self._is_customized))

    def validate(self, debug=False):
        try:
            assert self.id.validate(debug), "INVALID TabGroupId"
            assert self.visual_data.validate(debug), "INVALID TabGroupVisualData"
            assert self.tab_count < 1, "INVALID integer (tab_count)"
            assert validate_boolean(convert_int(self._read_field(self._is_customized))), "INVALID bool"
        except Exception as e:
            if debug: print('TabGroup -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class TabGroupVisualData(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 32

    class TabGroupColorId(Enum):
        kGrey = 0
        kBlue = 1
        kRed = 2
        kYellow = 3
        kGreen = 4
        kPink = 5
        kPurple = 6
        kCyan = 7
        kOrange = 8

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="tab_groups::TabGroupVisualData"]')

        self._title = Field(va, 0, 24, 'title')
        self._color = Field(va, 0x18, 4, 'color')
        self._is_collapsed = Field(va, 0x1C, 1, 'is_collapsed')

    def __getattr__(self, name):
        if name == 'title':
            return U16String(self._mdmp, self._title.va)
        if name == 'color':
            return TabGroupVisualData.TabGroupColorId(convert_int(self._read_field(self._color)))
        if name == 'is_collapsed':
            return convert_bool(self._read_field(self._is_collapsed))

    def validate(self, debug=False):
        try:
            assert self.title.validate(debug), "INVALID std::string (title)"
            assert self.color.value < 9, 'INVALID TabGroupColorId (color)'
            assert validate_boolean(convert_int(self._read_field(self._is_collapsed))), "INVALID bool (is_collapsed)"
        except Exception as e:
            if debug: print('TabGroupVisualData -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class Tab(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 56

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="TabBase<content::WebContents>"]')

    def __getattr__(self, name):
        if name == 'contents':
            return WebContents(self._mdmp, convert_int(self._read_field(self._contents)))
        if name == 'opener':
            return convert_int(self._read_field(self._opener))
        if name == 'reset_opener_on_active_tab_change':
            return convert_bool(self._read_field(self._reset_opener_on_active_tab_change))
        if name == 'pinned':
            return convert_bool(self._read_field(self._pinned))
        if name == 'blocked':
            return convert_bool(self._read_field(self._blocked))
        if name == 'group':
            absl_opt = Optional(self._mdmp, self._base+0x18, 16)
            return convert_int(absl_opt.data) if absl_opt.engaged else 0
        if name == 'grouphex':
            absl_opt = Optional(self._mdmp, self._base+0x18, 16)
            return absl_opt.data.hex() if absl_opt.engaged else 0

    def validate(self, debug=False):
        try:
            assert self.contents.validate(debug), "INVALID WebContents"
            assert validate_boolean(convert_int(self._read_field(self._reset_opener_on_active_tab_change))), "INVALID bool"
            assert validate_boolean(convert_int(self._read_field(self._pinned))), "INVALID bool"
            assert validate_boolean(convert_int(self._read_field(self._blocked))), "INVALID bool"
        except Exception as e:
            if debug: print('Tab -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class WebContents(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 4448

    class TerminationStatus(Enum):
        TERMINATION_STATUS_NORMAL_TERMINATION = 0
        TERMINATION_STATUS_ABNORMAL_TERMINATION = 1
        TERMINATION_STATUS_PROCESS_WAS_KILLED = 2
        TERMINATION_STATUS_PROCESS_CRASHED = 3
        TERMINATION_STATUS_STILL_RUNNING = 4
        TERMINATION_STATUS_LAUNCH_FAILED = 5
        TERMINATION_STATUS_OOM = 6
        TERMINATION_STATUS_INTEGRITY_FAILURE = 7
        TERMINATION_STATUS_MAX_ENUM = 8
    
    class Visibility(Enum):
        HIDDEN = 0
        OCCLUDED = 1
        VISIBLE = 2
    
    class UserAgentOverrideOption(Enum):
        UA_OVERRIDE_INHERIT = 0
        UA_OVERRIDE_FALSE = 1
        UA_OVERRIDE_TRUE = 2

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="content::WebContentsImpl"]')
    
    def __getattr__(self, name):
        if name == 'opened_by_another_window':
            return convert_bool(self._read_field(self._opened_by_another_window))
        if name == 'primary_frame_tree':
            return FrameTree(self._mdmp, self._primary_frame_tree.va)
        if name == 'primary_main_frame_process_status':
            return self.TerminationStatus(convert_int(self._read_field(self._primary_main_frame_process_status)))
        if name == 'primary_main_frame_process_error_code':
            return convert_int(self._read_field(self._primary_main_frame_process_error_code))
        if name == 'load_state_host':
            return U16String(self._mdmp, self._load_state_host.va)
        if name == 'load_info_timestamp':
            return TimeTicks(convert_int(self._read_field(self._load_info_timestamp)))
        if name == 'upload_size':
            return convert_int(self._read_field(self._upload_size))
        if name == 'upload_position':
            return convert_int(self._read_field(self._upload_position))
        if name == 'last_sent_theme_color':
            absl_opt = Optional(self._mdmp, self._last_sent_theme_color.va, 4)
            return convert_int(absl_opt.data) if absl_opt.engaged else 0
        if name == 'last_sent_background_color':
            absl_opt = Optional(self._mdmp, self._last_sent_background_color.va, 4)
            return convert_int(absl_opt.data) if absl_opt.engaged else 0
        if name == 'visibility':
            return self.Visibility(convert_int(self._read_field(self._visibility)))
        if name == 'maximum_zoom_percent':
            return convert_int(self._read_field(self._maximum_zoom_percent))
        if name == 'minimum_zoom_percent':
            return convert_int(self._read_field(self._minimum_zoom_percent))
        if name == 'zoom_scroll_remainder':
            return convert_float(self._read_field(self._zoom_scroll_remainder))
        if name == 'preferred_size':
            return Size(self._mdmp, self._preferred_size.va)
        if name == 'delayed_open_url_params':
            _ = convert_int(self._read_field(self._delayed_open_url_params))
            return OpenURLParams(self._mdmp, _) if validate_pointer(self._mdmp, _, False) else None
        if name == 'delayed_load_url_params':
            _ = convert_int(self._read_field(self._delayed_load_url_params))
            return LoadURLParams(self._mdmp, _) if validate_pointer(self._mdmp, _, False) else None
        if name == 'currently_playing_video_count':
            return convert_int(self._read_field(self._currently_playing_video_count))
        if name == 'should_override_user_agent_in_new_tabs': 
            return convert_bool(self._read_field(self._should_override_user_agent_in_new_tabs))
        if name == 'renderer_initiated_user_agent_override_option': 
            return self.UserAgentOverrideOption(
            convert_int(self._read_field(self._renderer_initiated_user_agent_override_option)))
        if name == 'using_dark_colors':
            return convert_bool(self._read_field(self._using_dark_colors))
        if name == 'last_screen_orientation_change_time': 
            return TimeTicks(convert_int(self._read_field(self._last_screen_orientation_change_time)))
        if name == 'page_base_background_color':
            absl_opt = Optional(self._mdmp, self._base+0x10C8, 4)
            return int.from_bytes(absl_opt.data, 'little') if absl_opt.engaged else 0
    
    def validate(self, debug=False):
        try:
            assert self.primary_frame_tree.validate(debug), "INVALID FrameTree (primary_frame_tree)"
            assert self.maximum_zoom_percent == 500, "INVALID integer (maximum_zoom_percent)"
            assert self.minimum_zoom_percent == 25, "INVALID integer (minimum_zoom_percent)"
            assert validate_boolean(convert_int(self._read_field(self._opened_by_another_window))), "INVALID bool (opened_by_another_window)"
            assert validate_boolean(convert_int(self._read_field(self._should_override_user_agent_in_new_tabs))), "INVALID bool (should_override_user_agent_in_new_tabs)"
            assert validate_boolean(convert_int(self._read_field(self._using_dark_colors))), "INVALID bool (using_dark_color)"
        except Exception as e:
            if debug: print('WebContents -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class FrameTree(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 1800

    class Type(Enum):
        kPrimary = 0
        kPrerender = 1
        kFencedFrame = 2

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="content::FrameTree"]')
    
    def __getattr__(self, name):
        if name == 'navigator':
            return Navigator(self._mdmp, self._navigator.va)
        if name == 'type':
            return self.Type(convert_int(self._read_field(self._type)))
        if name == 'load_progress':
            return convert_float(self._read_field(self._load_progress))
        if name == 'has_accessed_initial_main_document':
            return convert_bool(self._read_field(self._has_accessed_initial_main_document))
        if name == 'is_being_destroyed':
            return convert_bool(self._read_field(self._is_being_destroyed))
        if name == 'was_shut_down':
            return convert_bool(self._read_field(self._was_shut_down))

    def validate(self, debug=False):
        try:
            assert self.navigator.validate(debug), 'INVALID Navigator (navigator)'
            assert self.type.value < 3, "INVALID Type (type)"
            assert validate_boolean(convert_int(self._read_field(self._has_accessed_initial_main_document))), "INVALID bool (has_accessed_initial_main_document)"
            assert validate_boolean(convert_int(self._read_field(self._is_being_destroyed))), "INVALID bool (is_being_destroyed)"
            assert validate_boolean(convert_int(self._read_field(self._was_shut_down))), "INVALID bool (was_shut_down)"
        except Exception as e:
            if debug: print('FrameTree -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class Navigator(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 448

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="content::Navigator"]')
    
    def __getattr__(self, name):
        if name == 'controller':
            return NavigationController(self._mdmp, self._controller.va)
        if name == 'delegate':
            return convert_int(self._read_field(self._delegate))
        if name == 'metrics_data':
            _ = convert_int(self._read_field(self._metrics_data))
            return NavigationMetricsData(self._mdmp, _) if validate_pointer(self._mdmp, _, False) else None
    
    def validate(self, debug=False):
        try:
            assert self.controller.validate(debug), 'INVALID NavigationController (controller)'
        except Exception as e:
            if debug: print('Navigator -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class NavigationController(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 432

    class NeedsReloadType(Enum):
        kRequestedByClient = 0
        kRestoreSession = 1
        kCopyStateFrom = 2
        kCrashedSubframe = 3
    
    class ReloadType(Enum):
        NONE = 0
        NORMAL = 1
        BYPASSING_CACHE = 2
        ORIGINAL_REQUEST_URL = 3

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="content::NavigationControllerImpl"]')

    def __getattr__(self, name):
        if name == 'entries': 
            return Vector(self._mdmp, self._entries.va, 8)
        if name == 'pending_entry': 
            _ = convert_int(self._read_field(self._pending_entry))
            return NavigationEntry(self._mdmp, _) if validate_pointer(self._mdmp, _, False) else None
        if name == 'failed_pending_entry_id': 
            return convert_int(self._read_field(self._failed_pending_entry_id))
        if name == 'last_committed_entry_index': # 여러 엔트리 중 사용자가 마지막으로 보고 있던 엔트리
            return convert_int(self._read_field(self._last_committed_entry_index), signed=True)
        if name == 'needs_reload': 
            return convert_bool(self._read_field(self._needs_reload))
        if name == 'needs_reload_type': 
            _ = convert_int(self._read_field(self._needs_reload_type))
            return self.NeedsReloadType(_)
        if name == 'pending_reload':
            _ = convert_int(self._read_field(self._pending_reload))
            return self.ReloadType(_)

    def validate(self, debug=False):
        try:
            assert self.entries.validate(debug), 'INVALID std::vector (entries)'
            assert self.last_committed_entry_index < self.entries.entry_count, "INVALID integer (last_committed_entry_index)"
            assert self.last_committed_entry_index >= 0, "INVALID integer (last_committed_entry_index is negative)"
            assert self.needs_reload_type.value < 4, "INVALID NeedsReloadType (needs_reload_type)"
            assert self.pending_reload.value < 4, "INVALID ReloadType (pending_reload)"
        except Exception as e:
            if debug: print('NavigationController -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class NavigationEntry(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 1976

    class TreeNode(ChromiumInstanceInterface):
        _INSTANCE_LAYOUT = '< QQ24s' # parent, frame_entry, children
        _INSTANCE_SIZE = 40

        def __init__(self, mdmp: MinidumpFile, va: int):
            super().__init__(mdmp, va)
            self._load_symbols('./datatypes/datatype[@name="content::NavigationEntryImpl::TreeNode"]')
        
        def __getattr__(self, name):
            if name == 'parent':
                return convert_int(self._read_field(self._parent))
            if name == 'frame_entry':
                _ = convert_int(self._read_field(self._frame_entry))
                return FrameNavigationEntry(self._mdmp, _)
            if name == 'children':
                return Vector(self._mdmp, self._children.va, 8)
        
        def validate(self, debug=False):
            try:
                pass
            except Exception as e:
                if debug: print('NavigationEntry::TreeNode -> 0x{0:X} {1}'.format(self.base, e))
                return False
            return True

    class PageType(Enum):
        PAGE_TYPE_NORMAL = 0
        PAGE_TYPE_ERROR = 1
    
    class PageTransition(Enum):
        PAGE_TRANSITION_FIRST = 0
        PAGE_TRANSITION_LINK = PAGE_TRANSITION_FIRST 
        PAGE_TRANSITION_TYPED = 1
        PAGE_TRANSITION_AUTO_BOOKMARK = 2
        PAGE_TRANSITION_AUTO_SUBFRAME = 3
        PAGE_TRANSITION_MANUAL_SUBFRAME = 4
        PAGE_TRANSITION_GENERATED = 5
        PAGE_TRANSITION_AUTO_TOPLEVEL = 6
        PAGE_TRANSITION_FORM_SUBMIT = 7
        PAGE_TRANSITION_RELOAD = 8
        PAGE_TRANSITION_KEYWORD = 9
        PAGE_TRANSITION_KEYWORD_GENERATED = 10
        PAGE_TRANSITION_LAST_CORE = PAGE_TRANSITION_KEYWORD_GENERATED
        
        PAGE_TRANSITION_BLOCKED = 0x00800000
        PAGE_TRANSITION_FORWARD_BACK = 0x01000000
        PAGE_TRANSITION_FROM_ADDRESS_BAR = 0x02000000
        PAGE_TRANSITION_HOME_PAGE = 0x04000000
        PAGE_TRANSITION_FROM_API = 0x08000000
        PAGE_TRANSITION_CHAIN_START = 0x10000000
        PAGE_TRANSITION_CHAIN_END = 0x20000000
        PAGE_TRANSITION_CLIENT_REDIRECT = 0x40000000
        PAGE_TRANSITION_SERVER_REDIRECT = 0x80000000

        PAGE_TRANSITION_CORE_MASK = 0xFF
        PAGE_TRANSITION_IS_REDIRECT_MASK = 0xC0000000
        PAGE_TRANSITION_QUALIFIER_MASK = 0xFFFFFF00
    
    class RestoreType(Enum):
        kRestored = 0
        kNotRestored = 1
    
    class ReloadType(Enum):
        NONE = 0
        NORMAL = 1
        BYPASSING_CACHE = 2
        ORIGINAL_REQUEST_URL = 3

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="content::NavigationEntryImpl"]')
    
    def __getattr__(self, name):
        if name == 'frame_tree':
            _ = convert_int(self._read_field(self._frame_tree))
            return self.TreeNode(self._mdmp, _)
        if name == 'unique_id':
            return convert_int(self._read_field(self._unique_id), signed=True)
        if name == 'page_type':
            return self.PageType(convert_int(self._read_field(self._page_type)))
        if name == 'virtual_url':
            return GURL(self._mdmp, self._virtual_url.va)
        if name == 'title':
            return U16String(self._mdmp, self._title.va)
        if name == 'favicon':
            return FaviconStatus(self._mdmp, self._favicon.va)
        if name == 'ssl':
            return SSLStatus(self._mdmp, self._ssl.va)
        if name == 'transition_type':
            page_trans_core = self.PageTransition(self._transition_type & self.PageTransition.PAGE_TRANSITION_CORE_MASK.value)
            page_trans_is_redir = self.PageTransition(self._transition_type & self.PageTransition.PAGE_TRANSITION_IS_REDIRECT_MASK.value)
            page_trans_qualifier = self.PageTransition(self._transition_type & self.PageTransition.PAGE_TRANSITION_QUALIFIER_MASK.value)

            ret = []
            ret.append(page_trans_core)
            if page_trans_is_redir.value: ret.append(page_trans_is_redir)
            if page_trans_qualifier.value: ret.append(page_trans_qualifier)

            return ret
        if name == 'user_typed_url':
            return GURL(self._mdmp, self._user_typed_url.va)
        if name == 'restore_type':
            return self.RestoreType(convert_int(self._read_field(self._restore_type)))
        if name == 'original_request_url':
            return GURL(self._mdmp, self._original_request_url.va)
        if name == 'is_overriding_user_agent':
            return convert_bool(self._read_field(self._is_overriding_user_agent))
        if name == 'timestamp':
            return Time(convert_int(self._read_field(self._timestamp)))
        if name == 'http_status_code':
            return convert_int(self._read_field(self._http_status_code), signed=True)
        if name == 'extra_headers':
            return U8String(self._mdmp, self._extra_headers.va)
        if name == 'base_url_for_data_url':
            return GURL(self._mdmp, self._base_url_for_data_url.va)
        if name == 'cached_display_title':
            return U16String(self._mdmp, self._cached_display_title.va)
        if name == 'should_clear_history_list':
            return convert_bool(self._read_field(self._should_clear_history_list))
        if name == 'reload_type':
            return self.ReloadType(convert_int(self._read_field(self._reload_type)))
        if name == 'ssl_error':
            return convert_bool(self._read_field(self._ssl_error))
    
    def validate(self, debug=False):
        try:
            assert self.frame_tree.validate(debug), "INVALID NavigationEntry::TreeNode (frame_tree)"
            assert self.unique_id > 0, "INVALID integer (unique_id)"
            assert self.page_type.value < 2, "INVALID PageType (page_type)"
            assert self.virtual_url.validate(debug), "INVALID GURL (virtual_url)"
            assert self.title.validate(debug), "INVALID std::u16string (title)"
            assert self.favicon.validate(debug), "INVALID FaviconStatus (favicon)"
            assert self.ssl.validate(debug), "INVALID SSLStatus (ssl)"
            assert self.user_typed_url.validate(debug), "INVALID GURL (user_typed_url)"
            assert self.original_request_url.validate(debug), "INVALID GURL (original_request_url)"
            assert self.timestamp.validate(debug=debug)
            assert 100 <= self.http_status_code < 600, "INVALID integer (http_status_code)"
            assert self.base_url_for_data_url.validate(debug), "INVALID GURL (base_url_for_data_url)"
            assert validate_boolean(convert_int(self._read_field(self._is_overriding_user_agent))), "INVALID bool (is_overriding_user_agent)"
            assert validate_boolean(convert_int(self._read_field(self._should_clear_history_list))), "INVALID bool (should_clear_history_list)"
            assert validate_boolean(convert_int(self._read_field(self._ssl_error))), "INVALID bool (ssl_error)"
        except Exception as e:
            if debug:
                print('NavigationEntry -> 0x{0:X} {1}'.format(self.base, e))
                print(e.with_traceback())
            return False
        return True



class FrameNavigationEntry(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 0x351

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="content::FrameNavigationEntry"]')
    
    def __getattr__(self, name):
        if name == 'ref_count':
            return convert_int(self._read_field(self._ref_count))
        if name == 'frame_unique_name':
            return U8String(self._mdmp, self._frame_unique_name.va)
        if name == 'item_sequence_number':
            return convert_int(self._read_field(self._item_sequence_number))
        if name == 'document_sequence_number':
            return convert_int(self._read_field(self._document_sequence_number))
        if name == 'navigation_api_key':
            return U8String(self._mdmp, self._navigation_api_key.va)
        if name == 'site_instance':
            return convert_int(self._read_field(self._site_instance))
        if name == 'source_site_instance':
            return convert_int(self._read_field(self._source_site_instance))
        if name == 'url':
            return GURL(self._mdmp, self._url.va)
        if name == 'referrer': 
            return Referrer(self._mdmp, self._referrer.va)
        if name == 'redirect_chain':
            return Vector(self._mdmp, self._redirect_chain.va, 120)
        if name == 'bindings':
            return convert_int(self._read_field(self._bindings))
        if name == 'method':
            return U8String(self._mdmp, self._method.va)
        if name == 'post_id':
            return convert_int(self._read_field(self._post_id))
    
    def validate(self, debug=False):
        try:
            assert self.url.validate(debug), "INVALID GURL (url)"
            assert self.referrer.validate(debug), "INVALID Referrer (referrer)"
            assert self.redirect_chain.validate(debug), "INVALID std::vector (redirect_chain)"
            assert self.method.validate(debug), "INVALID std::string (method)"
        except Exception as e:
            if debug: print('FrameNavigationEntry -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class NavigationMetricsData(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 288

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="content::Navigator::NavigationMetricsData"]')
    
    def __getattr__(self, name):
        if name == 'start_time':
            return TimeTicks(convert_int(self._read_field(self._start_time)))
        if name == 'url':
            return GURL(self._mdmp, self._url.va)



class OpenURLParams(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 713

    class PageTransition(Enum):
        PAGE_TRANSITION_FIRST = 0
        PAGE_TRANSITION_LINK = PAGE_TRANSITION_FIRST 
        PAGE_TRANSITION_TYPED = 1
        PAGE_TRANSITION_AUTO_BOOKMARK = 2
        PAGE_TRANSITION_AUTO_SUBFRAME = 3
        PAGE_TRANSITION_MANUAL_SUBFRAME = 4
        PAGE_TRANSITION_GENERATED = 5
        PAGE_TRANSITION_AUTO_TOPLEVEL = 6
        PAGE_TRANSITION_FORM_SUBMIT = 7
        PAGE_TRANSITION_RELOAD = 8
        PAGE_TRANSITION_KEYWORD = 9
        PAGE_TRANSITION_KEYWORD_GENERATED = 10
        PAGE_TRANSITION_LAST_CORE = PAGE_TRANSITION_KEYWORD_GENERATED,
        PAGE_TRANSITION_CORE_MASK = 0xFF
        PAGE_TRANSITION_BLOCKED = 0x00800000
        PAGE_TRANSITION_FORWARD_BACK = 0x01000000
        PAGE_TRANSITION_FROM_ADDRESS_BAR = 0x02000000
        PAGE_TRANSITION_HOME_PAGE = 0x04000000
        PAGE_TRANSITION_FROM_API = 0x08000000
        PAGE_TRANSITION_CHAIN_START = 0x10000000
        PAGE_TRANSITION_CHAIN_END = 0x20000000
        PAGE_TRANSITION_CLIENT_REDIRECT = 0x40000000
        PAGE_TRANSITION_SERVER_REDIRECT = -2147483648
        PAGE_TRANSITION_IS_REDIRECT_MASK = -1073741824
        PAGE_TRANSITION_QUALIFIER_MASK = -256

    class ReloadType(Enum):
        NONE = 0
        NORMAL = 1
        BYPASSING_CACHE = 2
        ORIGINAL_REQUEST_URL = 3

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="content::OpenURLParams"]')

    def __getattr__(self, name):
        if name == 'url':
            return GURL(self._mdmp, self._url.va)
        if name == 'referrer':
            return Referrer(self._mdmp, self._referrer.va)
        if name == 'initiator_process_id':
            return convert_int(self._read_field(self._initiator_process_id))
        if name == 'redirect_chain':
            return Vector(self._mdmp, self._redirect_chain.va)
        if name == 'extra_headers':
            return U8String(self._mdmp, self._extra_headers.va)
        if name == 'transition':
            return self.PageTransition(convert_int(self._read_field(self._transition)))
        if name == 'href_translate':
            return U8String(self._mdmp, self._href_translate.va)
        if name == 'reload_type':
            return self.ReloadType(convert_int(self._read_field(self._reload_type)))
        if name == 'is_pdf':
            return convert_bool(self._read_field(self._is_pdf))



class LoadURLParams(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 1054

    class LoadURLType(Enum):
        LOAD_TYPE_DEFAULT = 0
        LOAD_TYPE_HTTP_POST = 1
        LOAD_TYPE_DATA = 2
    
    class PageTransition(Enum):
        PAGE_TRANSITION_FIRST = 0
        PAGE_TRANSITION_LINK = PAGE_TRANSITION_FIRST 
        PAGE_TRANSITION_TYPED = 1
        PAGE_TRANSITION_AUTO_BOOKMARK = 2
        PAGE_TRANSITION_AUTO_SUBFRAME = 3
        PAGE_TRANSITION_MANUAL_SUBFRAME = 4
        PAGE_TRANSITION_GENERATED = 5
        PAGE_TRANSITION_AUTO_TOPLEVEL = 6
        PAGE_TRANSITION_FORM_SUBMIT = 7
        PAGE_TRANSITION_RELOAD = 8
        PAGE_TRANSITION_KEYWORD = 9
        PAGE_TRANSITION_KEYWORD_GENERATED = 10
        PAGE_TRANSITION_LAST_CORE = PAGE_TRANSITION_KEYWORD_GENERATED
        
        PAGE_TRANSITION_BLOCKED = 0x00800000
        PAGE_TRANSITION_FORWARD_BACK = 0x01000000
        PAGE_TRANSITION_FROM_ADDRESS_BAR = 0x02000000
        PAGE_TRANSITION_HOME_PAGE = 0x04000000
        PAGE_TRANSITION_FROM_API = 0x08000000
        PAGE_TRANSITION_CHAIN_START = 0x10000000
        PAGE_TRANSITION_CHAIN_END = 0x20000000
        PAGE_TRANSITION_CLIENT_REDIRECT = 0x40000000
        PAGE_TRANSITION_SERVER_REDIRECT = 0x80000000

        PAGE_TRANSITION_CORE_MASK = 0xFF
        PAGE_TRANSITION_IS_REDIRECT_MASK = 0xC0000000
        PAGE_TRANSITION_QUALIFIER_MASK = 0xFFFFFF00

    class ReloadType(Enum):
        NONE = 0
        NORMAL = 1
        BYPASSING_CACHE = 2
        ORIGINAL_REQUEST_URL = 3

    class UserAgentOverrideOption(Enum):
        UA_OVERRIDE_INHERIT = 0
        UA_OVERRIDE_FALSE = 1
        UA_OVERRIDE_TRUE = 2

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="content::NavigationController::LoadURLParams"]')
    
    def __getattr__(self, name):
        if name == 'url':
            return GURL(self._mdmp, self._url.va)
        if name == 'initiator_process_id':
            return convert_int(self._read_field(self._initiator_process_id))
        if name == 'load_type':
            return self.LoadURLType(convert_int(self._read_field(self._load_type)))
        if name == 'transition_type':
            transition_type = convert_int(self._read_field(self._transition_type))
            page_trans_core = self.PageTransition(transition_type & self.PageTransition.PAGE_TRANSITION_CORE_MASK.value)
            page_trans_is_redir = self.PageTransition(transition_type & self.PageTransition.PAGE_TRANSITION_IS_REDIRECT_MASK.value)
            page_trans_qualifier = self.PageTransition(transition_type & self.PageTransition.PAGE_TRANSITION_QUALIFIER_MASK.value)

            ret = []
            ret.append(page_trans_core)
            if page_trans_is_redir.value: ret.append(page_trans_is_redir)
            if page_trans_qualifier.value: ret.append(page_trans_qualifier)
            return ret
        if name == 'referrer':
            return Referrer(self._mdmp, self._referrer.va)
        if name == 'redirect_chain':
            return Vector(self._mdmp, self._redirect_chain.va)
        if name == 'extra_headers':
            return U8String(self._mdmp, self._extra_headers.va)
        if name == 'override_user_agent':
            return self.UserAgentOverrideOption(convert_int(self._read_field(self._override_user_agent)))
        if name == 'base_url_for_data_url':
            return GURL(self._mdmp, self._base_url_for_data_url.va)
        if name == 'virtual_url_for_data_url':
            return GURL(self._mdmp, self._virtual_url_for_data_url.va)
        if name == 'post_content_type':
            return U8String(self._mdmp, self._post_content_type.va)
        if name == 'reload_type':
            return self.ReloadType(convert_int(self._read_field(self._reload_type)))
        if name == 'is_form_submission':
            return convert_bool(self._read_field(self._is_form_submission))
        if name == 'is_pdf':
            return convert_bool(self._read_field(self._is_pdf))



class ListSelectionMdoel(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 80

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="ui::ListSelectionModel"]')

    def __getattr__(self, name):
        if name == 'active':
            absl_opt = Optional(self._mdmp, self._active.va, 8)
            return convert_int(absl_opt.data) if absl_opt.engaged else -1
        if name == 'anchor':
            absl_opt = Optional(self._mdmp, self._anchor.va, 8)
            return convert_int(absl_opt.data) if absl_opt.engaged else -1