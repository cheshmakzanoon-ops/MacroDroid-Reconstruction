def run_controls(root):
    root = root.resolve()
    def run(argv):
        return subprocess.run(argv, cwd=another)
