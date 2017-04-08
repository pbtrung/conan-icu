from conans import ConanFile, ConfigureEnvironment
import os
from conans.tools import download, unzip

class IcuConan(ConanFile):
    description = "International Components for Unicode (ICU)"
    name = "icu"
    version = "59rc"
    branch = "master"
    license = "http://source.icu-project.org/repos/icu/icu/tags/release-58-1/LICENSE"
    url = "https://github.com/pbtrung/conan-icu"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        zip_name = "icu4c-%s-src.zip" % self.version.replace(".", "_")
        url = "http://download.icu-project.org/files/icu4c/%s/%s" % (self.version, zip_name)
        download(url, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def config(self):
        if self.settings.compiler == "Visual Studio" and \
           self.options.shared and "MT" in str(self.settings.compiler.runtime):
            self.options.shared = False

    def build(self):
        if self.settings.os == "Windows":
            self.build_windows()
        else:
            self.build_with_configure()

    def build_windows(self):
        sln_file = "%s\\icu\\source\\allinone\\allinone.sln" % self.conanfile_directory
        if self.settings.arch == "x86_64":
            arch = "x64"
        else:
            arch = "Win32"

        # upgrade projects
        command_line = "/upgrade"
        self.run("devenv %s %s" % (sln_file, command_line))

        # and build
        command_line = "/build \"Release|%s\" /project i18n" % arch
        self.run("devenv %s %s" % (sln_file, command_line))

    def build_with_configure(self):
        flags = '--prefix=%s --enable-tests=no --enable-samples=no' % self.package_folder
        if self.options.shared == 'True':
            flags += ' --disable-static --enable-shared'
        else:
            flags += ' --enable-static --disable-shared'

        if self.settings.build_type == 'Debug':
            flags += ' --enable-debug --disable-release'

        if self.settings.os == 'Macos':
            target_os = 'MacOSX'
        else:
            target_os = 'Linux'

        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        self.run("chmod +x icu/source/runConfigureICU icu/source/configure icu/source/install-sh")
        self.run("%s icu/source/runConfigureICU %s %s" % (env.command_line, target_os, flags))
        self.run("%s make" % env.command_line)
        self.run("%s make install" % env.command_line)

    def package(self):
        self.copy("*.h", "include", src="icu/include", keep_path=True)

        if self.settings.os == "Windows":
            if self.settings.arch == "x86_64":
                build_suffix = "64"
            else:
                build_suffix = ""

            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=("icu/bin%s" % build_suffix), keep_path=False)

            self.copy(pattern="*.lib", dst="lib", src=("icu/lib%s" % build_suffix), keep_path=False)

        else:
            self.copy( '*icu*.so', dst='lib', keep_path=False )
            self.copy( '*icu*.a', dst='lib', keep_path=False )
            self.copy( '*icu*.dylib', dst='lib', keep_path=False )

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["icuin", "icuuc", "icudt"]
        else:
            self.cpp_info.libs = ["icui18n", "icuuc", "icudata"]