from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibnameConan(ConanFile):
    name = "spidermonkey"
    description = "Keep it short"
    topics = ("conan", "libname", "logging")
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://github.com/original_author/original_lib"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports_sources = ["CMakeLists.txt"]
    generators = "make"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    
    download_url = "http://ftp.mozilla.org/pub/spidermonkey/prereleases/59/pre2/mozjs-59.0.0pre2.tar.bz2"
        
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    
    version = "59.0.0pre2"
    
    requires = (
        "zlib/1.2.11"
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get("http://ftp.mozilla.org/pub/spidermonkey/prereleases/59/pre2/mozjs-59.0.0pre2.tar.bz2")

    def build(self):
        os.mkdir(self._build_subfolder)
        os.chdir(self._build_subfolder)
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir="../mozjs-59.0.0pre2/js/src/")
        os.system('touch ../mozjs-59.0.0pre2/js/src/configure')
        os.system('touch ./config.status')
        autotools.make()

    def package(self):
        os.mkdir(self._build_subfolder)
        os.chdir(self._build_subfolder)
        autotools = AutoToolsBuildEnvironment(self)
        autotools.install()
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
