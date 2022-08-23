import common

_MARKER_DICT = {
	"@MOSSEAPI@": common.OUT_LIB_NAME
}
_CMAKELISTS_IN = "stub/CMakeLists.txt.stub"
_CMAKELISTS_OUT = common.OUTPUT_DIR + "CMakeLists.txt"


def generate_format_savefile():
	common.file_configure_append(_CMAKELISTS_IN, _MARKER_DICT, _CMAKELISTS_OUT)
