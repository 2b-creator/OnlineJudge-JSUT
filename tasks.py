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
                docker_image, f"/sandbox/{executable}"
            ]
            try:
                run_result = subprocess.run(
                    run_cmd, capture_output=True, text=True, timeout=time_limit, stdin=input_file)
            except subprocess.TimeoutExpired:
                return {"test_id": test_id, "status": "error", "message": "Time limit exceeded", "color": "blue", "code": "TLE", "judge_score": 0}
            except subprocess.CalledProcessError as e:
                if "memory" in e.stderr.lower():
                    return {"test_id": test_id, "status": "error", "message": "Memory limit exceeded", "color": "black",
                            "code": "MLE", "judge_score": 0}

            if run_result.returncode != 0:
                # 运行失败
                return {"test_id": test_id, "status": "error", "message": run_result.stderr, "color": "purple",
                        "code": "RE"}
            else:
                # actual_output = run_result.stdout
                with open(code_dir/"sandbox"/".out", "w") as wr:
                    wr.write(run_result.stdout)
                # src_path = "./.out"
                # dst_path = "../.out" # todo
                # shutil.copy(src_path, dst_path)
                # expected_output = expected_file.read().strip()
                checker_cmd = [f"./{code_dir}/checker",
                               test_file, f"./{code_dir}/sandbox/.out", expected_output_file]
                try:
                    check_result = subprocess.run(
                        checker_cmd, capture_output=True, timeout=SerialToml.checker_time_limit, text=True)
                except subprocess.TimeoutExpired:
                    return {"test_id": test_id, "status": "error", "message": "Checker time limit exceeded", "color": "black", "code": "UKE", "judge_score": 0}

                if check_result.returncode == SerialToml.checker_max_score:
                    return {"test_id": test_id, "status": "success", "color": "green", "code": "AC", "judge_score": check_result.returncode}
                else:
                    return {"test_id": test_id, "status": "failed", "message": "Wrong answer", "color": "red", "code": "WA", "judge_score": check_result.returncode}
    except Exception as e:
        return {"test_id": test_id, "status": "error", "message": "Unknown error", "color": "black",
                "code": "UKE", "judge_score": 0}


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
                        "code": "RE"}
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
            # cmp_checker = ["g++","/checker.cpp"]
            compile_cmd = [
                "docker", "run", "--rm",
                "-v", f"./{code_dir}:/sandbox",  # 挂载代码目录到 Docker 容器
                "--memory", f"{mem_limit}m",  # 限制内存
                "--cpus", f"{cpu_limit}",  # 限制 CPU
                docker_image, "g++",
                f"/sandbox/{code_file.name}",
                "-o", f"/sandbox/{executable}"
            ]
            compile_result = subprocess.run(
                compile_cmd, capture_output=True, text=True, timeout=SerialToml.cp_time_limit)
            if compile_result.returncode != 0:
                return_ls = {"status": "error", "message": compile_result.stderr, "results": ["Compile error"], "test_id": "0",
                             "color": "yellow", "code": "CE", "judge_score": 0}
                # 编译失败, 返回错误信息
                return return_ls
            compile_checker_cmd = [
                "g++", f"./{code_dir}/checker.cpp", "-o", f"./{code_dir}/checker", "-std=c++14", "-O2"]
            run_result = subprocess.run(
                compile_checker_cmd, capture_output=True, text=True, timeout=SerialToml.cp_time_limit)
            if run_result.returncode != 0:
                return_ls = {"status": "error", "message": compile_result.stderr, "results": ["Checker compile error"], "test_id": "0",
                             "color": "black", "code": "UKE", "judge_score": 0}
                return return_ls
            # 运行测试用例
            test_results = []
            test_scores = []
            for test_file in code_dir.glob(f"{problem_id}-*.in"):
                test_id = test_file.stem.split("-")[-1]
                expected_output_file = code_dir / f"{problem_id}-{test_id}.out"
                # 确保输出文件存在
                if not expected_output_file.exists():
                    test_results.append(
                        {"test_id": test_id, "status": "error", "message": "Missing expected output", "code": "UKE", "judge_score": 0})
                    continue
                test_result = run_cpp_exe(executable, code_dir, docker_image, test_file, expected_output_file, test_id,
                                          time_limit)
                test_results.append(test_result)
                test_scores.append(test_result["judge_score"])
            dd = __import__(tmpstr := str(
                code_dir/"calc").replace("/", "."), fromlist=True)
            func = "calc"
            calc_sum_score = getattr(dd, func, None)
            # calc_sum_score => 题目上传者提供的 calc 函数
            tmp = calc_sum_score(test_scores, SerialToml.checker_max_score)
            it = 0
            for i in test_results:
                i["score"] = tmp[it]
                it += 1
                # todo
            return {"status": "completed", "results": test_results, "score": tmp[-1]}

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

    except ValueError as e:
        return {"status": "error", "message": str(e)}
