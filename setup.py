import cx_Freeze

executables = [cx_Freeze.Executable("gameloop.py")]

cx_Freeze.setup(
    name="SpeedRunning Challenge",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["assets/"]}},
    executables=executables
)