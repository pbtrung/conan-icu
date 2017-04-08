from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "pbtrung")

class IcuConan(ConanFile):
    version = "59rc"
    settings = "os", "compiler", "build_type", "arch"
    requires = "icu/%s@%s/%s" % (version, username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")

    def test(self):
        self.run(os.sep.join([".","bin", "tst_icu"]))
