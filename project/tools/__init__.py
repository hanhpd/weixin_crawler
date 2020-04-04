def restart():
    import os
    import sys
    print(sys.executable)
    print(([sys.executable]+sys.argv))
    os.execl(sys.executable, "python.exe", *sys.argv)

