# 🚀 Dynamic Lambda Execution Pipeline on AWS

A modern, automated AWS pipeline for securely executing Python code from a GitHub repository using Lambda functions. This solution leverages **AWS CodePipeline**, **CodeBuild**, **Amazon S3**, and two Lambda functions to orchestrate, process, and dynamically execute Python code delivered as zipped artifacts.

---

## 📦 Overview

This project demonstrates a robust DevOps workflow for serverless code execution:

```
GitHub (lambda.py)
   ↓
CodePipeline → CodeBuild (packages code)
   ↓
Amazon S3 (stores artifact)
   ↓
Lambda A (extracts & forwards code)
   ↓
Lambda B (executes code dynamically)
```

---

## 🏗️ Architecture Components

### 1️⃣ GitHub Repository

- Hosts the `lambda.py` source file.
- Serves as the source stage for CodePipeline.

### 2️⃣ AWS CodePipeline

- Monitors the GitHub repository for changes.
- Triggers CodeBuild to package the latest code.

### 3️⃣ AWS CodeBuild

- Executes the `buildspec.yml` to:
  - Zip the `lambda.py` file.
  - Output `lambda.zip` as an artifact.

**Sample `buildspec.yml`:**
```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.9
  build:
    commands:
      - echo "Zipping lambda.py..."
      - zip -r lambda.zip lambda.py

artifacts:
  files:
    - lambda.zip
```

### 4️⃣ Amazon S3

- Stores the zipped Lambda code (`lambda.zip`).
- Triggers Lambda A upon new artifact upload.

### 5️⃣ Lambda A – Code Extractor

- Triggered by S3 PUT events.
- Downloads and unzips `lambda.zip`.
- Reads `lambda.py` and forwards the code to Lambda B.

### 6️⃣ Lambda B – Code Executor

- Receives Python code from Lambda A via the event payload.
- Logs and executes the code using `exec()`.
- Returns execution status and output.

> ⚠️ **Security Note:** Executing arbitrary code with `exec()` is inherently risky. This pipeline assumes a trusted, private GitHub repository and tightly controlled IAM permissions.

---

## 🚀 Deployment Steps

1. **Create an S3 Bucket** for artifact storage.
2. **Set Up CodePipeline** connected to your GitHub repository.
3. **Configure CodeBuild** with the provided `buildspec.yml`.
4. **Deploy Lambda A** with S3 trigger permissions.
5. **Deploy Lambda B** to receive and execute code.
6. **Test the Pipeline** by pushing changes to GitHub and monitoring the end-to-end workflow.

---

## 🔒 Security Best Practices

- Restrict GitHub repository access to trusted collaborators.
- Prevent direct user uploads to S3.
- Apply least-privilege IAM roles for Lambda and CodeBuild.
- Consider additional code validation or sandboxing for production environments.

---

## 📝 Example `lambda.py`

```python
print("Hello from lambda!")
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---



