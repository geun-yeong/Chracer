from minidump.minidumpfile import MinidumpFile
from enum import Enum

from chracer.validator import *
from chracer.interface import ChromiumInstanceInterface
from chracer.std import *
from chracer.gfx import *
from chracer.time import *
from chracer.absl import *
from chracer.common_lib import *



class GURL(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 120

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="GURL"]')

    def __getattr__(self, name):
        if name == 'spec':
            return U8String(self._mdmp, self._spec.va)
        if name == 'is_valid':
            return convert_bool(self._read_field(self._is_valid))
        if name == 'parsed':
            return Parsed(self._mdmp, self._parsed.va)
        if name == 'inner_url':
            _ = convert_int(self._read_field(self._inner_url))
            return GURL(self._mdmp, _) if _ else None
    
    def validate(self, debug=False):
        try:
            assert self.spec.validate(debug), "INVALID std::string (spec)"
            assert validate_boolean(convert_int(self._read_field(self._is_valid))), "INVALID bool (is_valid)"
            assert self.parsed.validate(debug), "INVALID url::Parsed (parsed)"
            if convert_int(self._read_field(self._inner_url)):
                assert self.inner_url.validate(debug), "INVALID url::GURL (inner_url)"
        except Exception as e:
            if debug: print('url::GURL -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True
    
    def __str__(self):
        return self.spec.string



class Component(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 8

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="url::Component"]')

    def __getattr__(self, name):
        if name == 'begin':
            return convert_int(self._read_field(self._begin), signed=True)
        if name == 'len':
            return convert_int(self._read_field(self._len), signed=True)

    def validate(self, debug=False):
        try:
            assert self.begin >= 0, "INVALID INTEGER (begin)"
            assert self.len >= -1, "INVALID INTEGER (length)" # if one component is valid, length has bigger than or equal 0, otherwise -1
        except Exception as e:
            if debug: print('url::Component -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class Parsed(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 80

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="url::Parsed"]')
    
    def __getattr__(self, name):
        if name == 'scheme':
            return Component(self._mdmp, self._scheme.va)
        if name == 'username':
            return Component(self._mdmp, self._username.va)
        if name == 'password':
            return Component(self._mdmp, self._password.va)
        if name == 'host':
            return Component(self._mdmp, self._host.va)
        if name == 'port':
            return Component(self._mdmp, self._port.va)
        if name == 'path':
            return Component(self._mdmp, self._path.va)
        if name == 'query':
            return Component(self._mdmp, self._query.va)
        if name == 'ref':
            return Component(self._mdmp, self._ref.va)
        if name == 'potentially_dangling_markup':
            return convert_bool(self._read_field(self._potentially_dangling_markup))
        if name == 'inner_parsed':
            return Parsed(self._mdmp, convert_int(self._read_field(self._inner_parsed)))
    
    def validate(self, debug=False):
        try:
            assert self.scheme.validate(debug), "INVALID url::Component (scheme)"
            assert self.username.validate(debug), "INVALID url::Component (username)"
            assert self.password.validate(debug), "INVALID url::Component (password)"
            assert self.host.validate(debug), "INVALID url::Component (host)"
            assert self.port.validate(debug), "INVALID url::Component (port)"
            assert self.path.validate(debug), "INVALID url::Component (path)"
            assert self.query.validate(debug), "INVALID url::Component (query)"
            assert self.ref.validate(debug), "INVALID url::Component (ref)"
            assert validate_boolean(convert_int(self._read_field(self._potentially_dangling_markup))), "INVALID bool (potentially_dangling_markup)"
        except Exception as e:
            if debug: print('url::Parsed -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class Referrer(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 128

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="content::Referrer"]')

    def __getattr__(self, name):
        if name == 'url':
            return GURL(self._mdmp, self._url.va)
        if name == 'policy':
            return convert_int(self._read_field(self._policy))
    
    def validate(self, debug=False):
        try:
            assert self.url.validate(debug), "INVALID url::GURL (url)"
        except Exception as e:
            if debug: print('url::Referrer -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class Origin(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 56

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="url::Origin"]')

    def __getattr__(self, name):
        if name == 'tuple':
            return SchemeHostPort(self._mdmp, self._tuple.va)

    def validate(self, debug=False):
        try:
            assert self.tuple.validate(debug), "INVALID url::SchemeHostPort (tuple)"
        except Exception as e:
            if debug: print('url::Origin -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class SchemeHostPort(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 50

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="url::SchemeHostPort"]')

    def __getattr__(self, name):
        if name == 'scheme':
            return U8String(self._mdmp, self._scheme.va)
        if name == 'host':
            return U8String(self._mdmp, self._host.va)
        if name == 'port':
            return convert_int(self._read_field(self._port))

    def validate(self, debug=False):
        try:
            assert self.scheme.validate(debug), "INVALID std::string (scheme)"
            assert self.host.validate(debug), "INVALID std::string (host)"
            assert self.port < 65536, "INVALID INTEGER (port)"
        except Exception as e:
            if debug: print('url::SchemeHostPort -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class FaviconStatus(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 136

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="content::FaviconStatus"]')
    
    def __getattr__(self, name):
        if name == 'valid':
            return convert_bool(self._read_field(self._valid))
        if name == 'url':
            return GURL(self._mdmp, self._url.va)
        if name == 'image':
            return Image(self._mdmp, convert_int(self._read_field(self._image)))

    def validate(self, debug=False):
        try:
            assert validate_boolean(convert_int(self._read_field(self._valid))), "INVALID bool (valid)"
            assert self.url.validate(debug), "INVALID url::GURL (url)"
            assert self.image.validate(debug), "INVALID gfx::Image (image)"
        except Exception as e:
            if debug: print('content::FaviconStatus -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class SSLStatus(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 40

    class CTPolicyCompliance(Enum):
        CT_POLICY_COMPLIES_VIA_SCTS = 0
        CT_POLICY_NOT_ENOUGH_SCTS = 1
        CT_POLICY_NOT_DIVERSE_SCTS = 2
        CT_POLICY_BUILD_NOT_TIMELY = 3
        CT_POLICY_COMPLIANCE_DETAILS_NOT_AVAILABLE = 4

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="content::SSLStatus"]')
    
    def __getattr__(self, name):
        if name == 'initialized':
            return convert_bool(self._read_field(self._initialized))
        if name == 'certificate':
            _ = convert_int(self._read_field(self._certificate))
            return X509Certificate(self._mdmp, _) if validate_pointer(self._mdmp, _, False) else None
        if name == 'cert_status':
            return convert_int(self._read_field(self._cert_status))
        if name == 'key_exchange_group':
            return convert_int(self._read_field(self._key_exchange_group))
        if name == 'peer_signature_algorithm':
            return convert_int(self._read_field(self._peer_signature_algorithm))
        if name == 'connection_status':
            return convert_int(self._read_field(self._connection_status))
        if name == 'content_status':
            return convert_int(self._read_field(self._content_status))
        if name == 'pkp_bypassed':
            return convert_bool(self._read_field(self._pkp_bypassed))
        if name == 'ct_policy_compliance':
            return self.CTPolicyCompliance(convert_int(self._read_field(self._ct_policy_compliance)))
    
    def validate(self, debug=False):
        try:
            assert validate_boolean(convert_int(self._read_field(self._initialized))), "INVALID bool (initialized)"
            c = self.certificate
            if c: assert c.validate(debug), "INVALID net::X509Certificate (certificate)"
            assert validate_boolean(convert_int(self._read_field(self._pkp_bypassed))), "INVALID bool (pkp_bypassed)"
            assert self.ct_policy_compliance.value < 5, 'INVALID CTPolicyCompliance (ct_policy_compliance)'
        except Exception as e:
            if debug: print('content::SSLStatus -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class X509Certificate(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 464

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="net::X509Certificate"]')

    def __getattr__(self, name):
        if name == 'subject':
            return CertPrincipal(self._mdmp, self._subject.va)
        if name == 'issuer':
            return CertPrincipal(self._mdmp, self._issuer.va)
        if name == 'valid_start':
            return Time(convert_int(self._read_field(self._valid_start)))
        if name == 'valid_expiry':
            return Time(convert_int(self._read_field(self._valid_expiry)))
        if name == 'serial_number':
            sn = ''

            data = self._read_field(self._serial_number)
            if data[23] < 23:
                sn = data[ : data[23] ]
            else:
                sn_ptr = convert_int(data[:8])
                sn_len = convert_int(data[8:12])
                sn = self._read_from(sn_ptr, sn_len)
            
            sn = sn.hex().upper()
            return ':'.join([sn[i:i+2] for i in range(0, len(sn), 2)])
    
    def validate(self, debug=False):
        try:
            assert self.subject.validate(debug), "INVALID net::CertPrincipal (subject)"
            assert self.issuer.validate(debug), "INVALID net::CertPrincipal (issuer)"
            assert self.valid_start.validate(debug), 'INVALID base::Time (valid_start)'
            assert self.valid_expiry.validate(debug), 'INVALID base::Time (valid_end)'
        except Exception as e:
            if debug: print('net::X509Certificate -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class CertPrincipal(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 192

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./datatypes/datatype[@name="net::CertPrincipal"]')
    
    def __getattr__(self, name):
        if name == 'common_name':
            return U8String(self._mdmp, self._common_name.va)
        if name == 'locality_name':
            return U8String(self._mdmp, self._locality_name.va)
        if name == 'state_or_province_name':
            return U8String(self._mdmp, self._state_or_province_name.va)
        if name == 'country_name':
            return U8String(self._mdmp, self._country_name.va)
        if name == 'street_addresses':
            return Vector(self._mdmp, self._street_addresses.va, 24)
        if name == 'organization_names':
            return Vector(self._mdmp, self._organization_names.va, 24)
        if name == 'organization_unit_names':
            return Vector(self._mdmp, self._organization_unit_names.va, 24)
        if name == 'domain_components':
            return Vector(self._mdmp, self._domain_components.va, 24)

    def validate(self, debug=False):
        try:
            assert self.common_name.validate(debug), "INVALID std::string (common_name)"
            assert self.locality_name.validate(debug), "INVALID std::string (locality_name)"
            assert self.state_or_province_name.validate(debug), "INVALID std::string (state_or_province_name)"
            assert self.country_name.validate(debug), "INVALID std::string (country_name)"
            assert self.street_addresses.validate(debug), "INVALID std::string (street_addresses)"
            assert self.organization_names.validate(debug), "INVALID std::string (organization_names)"
            assert self.organization_unit_names.validate(debug), "INVALID std::string (organization_unit_names)"
            assert self.domain_components.validate(debug), "INVALID std::string (domain_components)"
        except Exception as e:
            if debug: print('net::CertPrincipal -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True