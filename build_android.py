import os
import subprocess

def set_environment_variables(ndk_path, abi, toolchain_file):
    os.environ['ANDROID_NDK'] = ndk_path
    os.environ['ANDROID_ABI'] = abi
    os.environ['CMAKE_TOOLCHAIN_FILE'] = toolchain_file

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def run_make_command(make_program, makefile_dir):
    original_dir = os.getcwd()
    os.chdir(makefile_dir)
    
    try:
        result = subprocess.run([make_program], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Make Output:", result.stdout.decode('latin-1'))
        print("Make Errors:", result.stderr.decode('latin-1'))
    except subprocess.CalledProcessError as e:
        print("Error running make:", e)
        print("Make Output:", e.stdout.decode('latin-1'))
        print("Make Errors:", e.stderr.decode('latin-1'))
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    # Set the paths
    ndk_path = r"C:\Users\ajx\AppData\Local\Android\Sdk\ndk\26.1.10909125"
    abi = "arm64-v8a"
    make_program = os.path.join(ndk_path, "prebuilt", "windows-x86_64", "bin", "make.exe")
    toolchain_file = os.path.join(ndk_path, "build", "cmake", "android.toolchain.cmake")
    makefile_dir = r"D:\Code\aidlux_aistack_realtime_cm\redis-7.0\src"  # Directory containing the Makefile
    output_dir = os.path.join(makefile_dir, "build", "arm64-v8a")

    # Set environment variables for the NDK
    set_environment_variables(ndk_path, abi, toolchain_file)

    # Create the output directory if it doesn't exist
    create_directory(output_dir)

    # Run the make command
    run_make_command(make_program, makefile_dir)
