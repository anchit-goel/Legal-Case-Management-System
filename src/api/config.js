let _base = import.meta.env.VITE_BACKEND_URL || '';
if (_base && !_base.startsWith('http')) {
	_base = `https://${_base}`;
}
export const BASE_URL = _base;
