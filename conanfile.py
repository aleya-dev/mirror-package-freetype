from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps
from conan.tools.files import rmdir, collect_libs
import os


required_conan_version = ">=2.0"


class FreeTypeConan(ConanFile):
    name = "freetype"
    version = "2.13.2"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaCmakeBase"
    ignore_cpp_standard = True

    exports_sources = "source/*"

    options = {
        "shared": [False, True],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    requires = "zlib/1.3.0@aleya/public", "libpng/1.6.40@aleya/public"

    def configure(self):
        super().configure()

        self.options["zlib"].shared = self.options.shared
        self.options["libpng"].shared = self.options.shared

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["FT_REQUIRE_ZLIB"] = True
        tc.variables["FT_REQUIRE_PNG"] = True
        tc.variables["FT_DISABLE_HARFBUZZ"] = True
        tc.variables["FT_DISABLE_BZIP2"] = True
        tc.variables["FT_DISABLE_BROTLI"] = True
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def package(self):
        super().package()

        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

        if not self.options.shared:
            rmdir(self, os.path.join(self.package_folder, "bin"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_module_file_name", "Freetype")
        self.cpp_info.set_property("cmake_file_name", "freetype")
        self.cpp_info.set_property("cmake_target_name", "Freetype::Freetype")
        self.cpp_info.set_property("cmake_target_aliases", ["freetype"])
        self.cpp_info.set_property("pkg_config_name", "freetype2")
        self.cpp_info.includedirs.append(os.path.join("include", "freetype2"))

        self.cpp_info.libs = collect_libs(self)
