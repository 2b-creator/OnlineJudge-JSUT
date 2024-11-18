from celery import Celery
import subprocess
import os
import shutil
from pathlib import Path

celery_app = Celery('tasks', broker='redis://localhost:6379/0')


def run_cpp_exe(executable, code_dir, docker_image, test_file, expected_output_file, test_id):
    with open(test_file) as input_file, open(expected_output_file) as expected_file:
        run_cmd = [
            "docker", "run", "--rm",
            "-v", f"{code_dir}:/sandbox",  # 挂载代码目录到 Docker 容器
            "--memory", "128m",  # 限制内存
            "--cpus", "0.5",  # 限制 CPU
            docker_image, f"./{executable}"
        ]
        run_result = subprocess.run(run_cmd, stdin=input_file, capture_output=True, text=True)
        if run_result.returncode != 0:
            # 运行失败
            return {"test_id": test_id, "status": "error", "message": run_result.stderr}
        else:
            actual_output = run_result.stdout.strip()
            expected_output = expected_file.read().strip()
            if actual_output == expected_output:
                return {"test_id": test_id, "status": "success"}
            else:
                return {"test_id": test_id, "status": "failed", "expected": expected_output, "actual": actual_output}


def run_py(executable, code_dir, docker_image, test_file, expected_output_file, test_id):
    with open(test_file) as input_file, open(expected_output_file) as expected_file:
        run_cmd = [
            "docker", "run", "--rm",
            "-v", f"{code_dir}:/sandbox",  # 挂载代码目录到 Docker 容器
            "--memory", "128m",  # 限制内存
            "--cpus", "0.5",  # 限制 CPU
            docker_image, f"python3 {executable}"
        ]
        run_result = subprocess.run(run_cmd, stdin=input_file, capture_output=True, text=True)
        if run_result.returncode != 0:
            # 运行失败
            return {"test_id": test_id, "status": "error", "message": run_result.stderr}
        else:
            actual_output = run_result.stdout.strip()
            expected_output = expected_file.read().strip()
            if actual_output == expected_output:
                return {"test_id": test_id, "status": "success"}
            else:
                return {"test_id": test_id, "status": "failed", "expected": expected_output, "actual": actual_output}


@celery_app.task
def judge_work(problem_id, user_id, code, language):
    try:
        code_dir = Path(f"./{problem_id}")
        code_dir.mkdir(parents=True, exist_ok=True)
        code_file = code_dir / f"{user_id}.{language}"
        container_code_dir = "/sandbox"
        docker_image = "gcc_sandbox"
        with open(code_file, 'w') as f:
            f.write(code)

        # cpp
        if language == "cpp":
            executable = f"{user_id}.out"

            compile_cmd = [
                "docker", "run", "--rm",
                "-v", f"{code_dir}:/sandbox",  # 挂载代码目录到 Docker 容器
                "--memory", "128m",  # 限制内存
                "--cpus", "0.5",  # 限制 CPU
                docker_image, "g++",
                f"{container_code_dir}/{code_file.name}",
                "-o", f"{container_code_dir}/{executable}"
            ]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_result.returncode != 0:
                # 编译失败，返回错误信息
                return {"status": "error", "message": compile_result.stderr}
            # 运行测试用例
            test_results = []
            for test_file in code_dir.glob(f"{problem_id}-*.in"):
                test_id = test_file.stem.split("-")[-1]
                expected_output_file = code_dir / f"{problem_id}-{test_id}.out"
                # 确保输出文件存在
                if not expected_output_file.exists():
                    test_results.append({"test_id": test_id, "status": "error", "message": "Missing expected output"})
                    continue
                test_results.append(
                    run_cpp_exe(executable, code_dir, docker_image, test_file, expected_output_file, test_id))
            return {"status": "completed", "results": test_results}

        # python
        elif language == "py":
            test_results = []
            for test_file in code_dir.glob(f"{problem_id}-*.in"):
                test_id = test_file.stem.split("-")[-1]
                expected_output_file = code_dir / f"{problem_id}-{test_id}.out"
                # 确保输出文件存在
                if not expected_output_file.exists():
                    test_results.append({"test_id": test_id, "status": "error", "message": "Missing expected output"})
                    continue
                test_results.append(
                    run_py(code_file.name, code_dir, docker_image, test_file, expected_output_file, test_id))

        else:
            return {"status": "error", "message": f"Unsupported language: {language}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
