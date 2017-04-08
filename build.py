from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    visual_versions = [10, 12, 14]
    builder = ConanMultiPackager(username="pbtrung")
    builder.add_common_builds(visual_versions=visual_versions)
    builder.run()