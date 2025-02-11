from celery import Celery
import SerialToml
import shutil
import subprocess
from pathlib import Path

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0'  # 使用 Redis 作为结果存储
)


def run_cpp_exe(executable, code_dir, docker_image, test_file, expected_output_file, test_id, time_limit, memory_limit=128):
    try:
        with open(test_file) as input_file, open(expected_output_file) as expected_file:
            run_cmd = [
                "docker", "run", "--rm", "-i",
                "-v", f"./{code_dir}:/sandbox",  # 挂载代码目录到 Docker 容器
                "--memory", f"{memory_limit}m",  # 限制内存 todo
                "--cpus", "1",  # 限制 CPU 
                docker_image, f"/sandbox/{executable}", "<", test_file, ">", ".out"
            ]
            run_result = subprocess.run(
                run_cmd, capture_output=True, text=True, timeout=time_limit)
            if run_result.returncode != 0:
                # 运行失败
                return {"test_id": test_id, "status": "error", "message": run_result.stderr, "color": "purple",
                        "code": "RE"}
            else:
                actual_output = run_result.stdout
                src_path = "./.out"
                dst_path = "../.out" # todo
                shutil.copy(src_path, dst_path)
                expected_output = expected_file.read().strip()
                if actual_output == expected_output:
                    return {"test_id": test_id, "status": "success", "color": "green", "code": "AC"}
                else:
                    return {"test_id": test_id, "status": "failed", "expected": expected_output,
                            "actual": actual_output, "message": "Wrong answer", "color": "red", "code": "WA"}
    except subprocess.TimeoutExpired:
        return {"test_id": test_id, "status": "error", "message": "Time limit exceeded", "color": "blue", "code": "TLE"}
    except subprocess.CalledProcessError as e:
        if "memory" in e.stderr.lower():
            return {"test_id": test_id, "status": "error", "message": "Memory limit exceeded", "color": "yellow",
                    "code": "MLE"}


def run_py(executable, code_dir, docker_image, test_file, expected_output_file, test_id, time_limit):
    try:
        with open(test_file) as input_file, open(expected_output_file) as expected_file:
            run_cmd = [
                "docker", "run", "--rm", "-i",
                "-v", f"./{code_dir}:/sandbox",  # 挂载代码目录到 Docker 容器
                "--memory", "128m",  # 限制内存
                "--cpus", "0.5",  # 限制 CPU
                docker_image, f"python3 {executable}", "<", test_file
            ]
            run_result = subprocess.run(
                run_cmd, timeout=time_limit, stdin=input_file, capture_output=True, text=True)
            if run_result.returncode != 0:
                # 运行失败
                return {"test_id": test_id, "status": "error", "message": run_result.stderr, "color": "purple",
                        "code": "ER"}
            else:
                actual_output = run_result.stdout.strip()
                expected_output = expected_file.read().strip()
                if actual_output == expected_output:
                    return {"test_id": test_id, "status": "success", "color": "green", "code": "AC"}
                else:
                    return {"test_id": test_id, "status": "failed", "expected": expected_output,
                            "actual": actual_output, "message": "Wrong answer", "color": "red", "code": "WA"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Time limit exceeded", "color": "blue", "code": "TLE"}
    except subprocess.CalledProcessError as e:
        if "memory" in e.stderr.lower():
            return {"status": "error", "message": "Memory limit exceeded", "color": "yellow", "code": "MLE"}


@celery_app.task
def judge_work(problem_id, username, code, language, time_limit=2):
    try:
        cpu_limit = SerialToml.cp_cpu_limit
        mem_limit = SerialToml.cp_mem_limit
        code_dir = Path(f"./TestSamples/{problem_id}")
        code_dir.mkdir(parents=True, exist_ok=True)
        code_file = code_dir / f"{username}.{language}"
        container_code_dir = "/sandbox"
        docker_image = "sandbox"
        with open(code_file, 'w') as f:
            f.write(code)

        # cpp
        if language == "cpp":
            executable = f"{username}"
            # cmp_checker = ["g++","/checker."]
            compile_cmd = [
                "docker", "run", "--rm",
                "-v", f"./{code_dir}:/sandbox",  # 挂载代码目录到 Docker 容器
                "--memory", f"{mem_limit}m",  # 限制内存
                "--cpus", cpu_limit,  # 限制 CPU
                docker_image, "g++",
                f"/sandbox/{code_file.name}",
                "-o", f"/sandbox/{executable}"
            ]
            compile_result = subprocess.run(
                compile_cmd, capture_output=True, text=True, timeout=SerialToml.cp_time_limit)
            if compile_result.returncode != 0:
                return_ls = [
                    {"status": "error", "message": compile_result.stderr, "results": "Compile error", "test_id": "0",
                     "color": "black", "code": "CE"}]
                # 编译失败, 返回错误信息
                return return_ls
            # 运行测试用例
            test_results = []
            for test_file in code_dir.glob(f"{problem_id}-*.in"):
                test_id = test_file.stem.split("-")[-1]
                expected_output_file = code_dir / f"{problem_id}-{test_id}.out"
                # 确保输出文件存在
                if not expected_output_file.exists():
                    test_results.append(
                        {"test_id": test_id, "status": "error", "message": "Missing expected output"})
                    continue
                test_results.append(
                    run_cpp_exe(executable, code_dir, docker_image, test_file, expected_output_file, test_id,
                                time_limit))
            return {"status": "completed", "results": test_results}

        # python
        elif language == "py":
            test_results = []
            for test_file in code_dir.glob(f"{problem_id}-*.in"):
                test_id = test_file.stem.split("-")[-1]
                expected_output_file = code_dir / f"{problem_id}-{test_id}.out"
                # 确保输出文件存在
                if not expected_output_file.exists():
                    test_results.append(
                        {"test_id": test_id, "status": "error", "message": "Missing expected output"})
                    continue
                test_results.append(
                    run_py(code_file.name, code_dir, docker_image, test_file, expected_output_file, test_id,
                           time_limit))
                print(test_results)
            return {"status": "completed", "results": test_results}

        else:
            return {"status": "error", "message": f"Unsupported language: {language}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
