#find out how to call it from python directly or subprocess (subprocess)
import subprocess

def subprocess_run(input_tar, tmpOutputFolder):
    subprocess.call(['python', '-m', 'rpviz.cli', input_tar, tmpOutputFolder])
