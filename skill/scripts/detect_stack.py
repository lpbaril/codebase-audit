#!/usr/bin/env python3
"""
Technology Stack Detection Script

Scans a target codebase and detects technologies, frameworks, cloud providers,
and compliance indicators to recommend the appropriate audit path.

Usage:
    python detect_stack.py /path/to/target

Output:
    JSON object with detected technologies and recommended audits
"""

import json
import os
import re
import sys
from pathlib import Path


def read_file_safe(path: Path) -> str:
    """Safely read a file, returning empty string on error."""
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ""


def find_files(root: Path, patterns: list) -> list:
    """Find files matching any of the given patterns."""
    matches = []
    for pattern in patterns:
        matches.extend(root.glob(pattern))
    return matches


def detect_node_frameworks(root: Path) -> dict:
    """Detect Node.js frameworks from package.json."""
    result = {"detected": False, "frameworks": [], "is_mobile": False}

    package_json = root / "package.json"
    if not package_json.exists():
        return result

    content = read_file_safe(package_json)
    if not content:
        return result

    result["detected"] = True

    # Framework detection patterns
    framework_patterns = {
        "react": r'"react"\s*:',
        "next.js": r'"next"\s*:',
        "vue": r'"vue"\s*:',
        "nuxt": r'"nuxt"\s*:',
        "angular": r'"@angular/core"\s*:',
        "express": r'"express"\s*:',
        "fastify": r'"fastify"\s*:',
        "nestjs": r'"@nestjs/core"\s*:',
        "remix": r'"@remix-run',
        "svelte": r'"svelte"\s*:',
        "react-native": r'"react-native"\s*:',
        "expo": r'"expo"\s*:',
    }

    for framework, pattern in framework_patterns.items():
        if re.search(pattern, content):
            result["frameworks"].append(framework)
            if framework in ["react-native", "expo"]:
                result["is_mobile"] = True

    return result


def detect_python_frameworks(root: Path) -> dict:
    """Detect Python frameworks."""
    result = {"detected": False, "frameworks": []}

    files = ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]
    content = ""

    for f in files:
        path = root / f
        if path.exists():
            result["detected"] = True
            content += read_file_safe(path)

    if not content:
        return result

    framework_patterns = {
        "django": r'django',
        "flask": r'flask',
        "fastapi": r'fastapi',
        "pyramid": r'pyramid',
        "tornado": r'tornado',
    }

    for framework, pattern in framework_patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            result["frameworks"].append(framework)

    return result


def detect_ruby_frameworks(root: Path) -> dict:
    """Detect Ruby frameworks."""
    result = {"detected": False, "frameworks": []}

    gemfile = root / "Gemfile"
    if not gemfile.exists():
        return result

    content = read_file_safe(gemfile)
    result["detected"] = True

    if re.search(r"gem\s+['\"]rails['\"]", content):
        result["frameworks"].append("rails")
    if re.search(r"gem\s+['\"]sinatra['\"]", content):
        result["frameworks"].append("sinatra")

    return result


def detect_php_frameworks(root: Path) -> dict:
    """Detect PHP frameworks."""
    result = {"detected": False, "frameworks": []}

    composer = root / "composer.json"
    if not composer.exists():
        return result

    content = read_file_safe(composer)
    result["detected"] = True

    if "laravel" in content.lower():
        result["frameworks"].append("laravel")
    if "symfony" in content.lower():
        result["frameworks"].append("symfony")

    return result


def detect_java_frameworks(root: Path) -> dict:
    """Detect Java/Kotlin frameworks."""
    result = {"detected": False, "frameworks": []}

    # Check for Maven
    pom = root / "pom.xml"
    if pom.exists():
        content = read_file_safe(pom)
        result["detected"] = True
        if "spring" in content.lower():
            result["frameworks"].append("spring-boot")

    # Check for Gradle
    for gradle_file in root.glob("**/build.gradle*"):
        content = read_file_safe(gradle_file)
        result["detected"] = True
        if "spring" in content.lower():
            result["frameworks"].append("spring-boot")
        break

    return result


def detect_ios(root: Path) -> bool:
    """Detect iOS project."""
    indicators = [
        root / "Podfile",
        *root.glob("*.xcodeproj"),
        *root.glob("*.xcworkspace"),
        *root.glob("**/Info.plist"),
    ]
    return any(p.exists() if hasattr(p, 'exists') else True for p in indicators)


def detect_android(root: Path) -> bool:
    """Detect Android project."""
    # Check for AndroidManifest.xml
    manifests = list(root.glob("**/AndroidManifest.xml"))
    if manifests:
        return True

    # Check for app/build.gradle
    gradle_files = list(root.glob("**/build.gradle*"))
    for gf in gradle_files:
        content = read_file_safe(gf)
        if "com.android" in content or "android {" in content:
            return True

    return False


def detect_flutter(root: Path) -> bool:
    """Detect Flutter project."""
    pubspec = root / "pubspec.yaml"
    if pubspec.exists():
        content = read_file_safe(pubspec)
        return "flutter:" in content
    return False


def detect_cloud_provider(root: Path) -> str:
    """Detect cloud provider from configuration files."""
    # Check Terraform files
    tf_files = list(root.glob("**/*.tf"))
    for tf in tf_files[:10]:  # Limit to first 10 files
        content = read_file_safe(tf)
        if 'provider "aws"' in content or "aws_" in content:
            return "aws"
        if 'provider "google"' in content or "google_" in content:
            return "gcp"
        if 'provider "azurerm"' in content or "azurerm_" in content:
            return "azure"

    # Check serverless.yml
    serverless = root / "serverless.yml"
    if serverless.exists():
        content = read_file_safe(serverless)
        if "provider:" in content:
            if "aws" in content.lower():
                return "aws"
            if "google" in content.lower():
                return "gcp"
            if "azure" in content.lower():
                return "azure"

    # Check for cloud-specific files
    if (root / "app.yaml").exists():
        return "gcp"

    if list(root.glob("**/.aws/**")) or list(root.glob("**/aws-exports*")):
        return "aws"

    return "unknown"


def detect_infrastructure(root: Path) -> list:
    """Detect infrastructure technologies."""
    infra = []

    # Docker
    if (root / "Dockerfile").exists() or (root / "docker-compose.yml").exists():
        infra.append("docker")

    # Kubernetes
    yaml_files = list(root.glob("**/*.yaml")) + list(root.glob("**/*.yml"))
    for yf in yaml_files[:20]:  # Limit search
        content = read_file_safe(yf)
        if "apiVersion:" in content and ("kind: Deployment" in content or "kind: Service" in content):
            infra.append("kubernetes")
            break

    # Terraform
    if list(root.glob("**/*.tf")):
        infra.append("terraform")

    # Serverless
    if (root / "serverless.yml").exists() or (root / "serverless.ts").exists():
        infra.append("serverless")

    # AWS SAM
    if (root / "template.yaml").exists() or (root / "template.yml").exists():
        content = read_file_safe(root / "template.yaml") or read_file_safe(root / "template.yml")
        if "AWS::Serverless" in content:
            infra.append("aws-sam")

    return list(set(infra))


def detect_api_type(root: Path) -> list:
    """Detect API types used."""
    api_types = []

    # GraphQL
    graphql_files = list(root.glob("**/*.graphql")) + list(root.glob("**/schema.graphql"))
    if graphql_files:
        api_types.append("graphql")
    else:
        # Check for GraphQL in code
        for ext in ["*.ts", "*.js", "*.py"]:
            for f in list(root.glob(f"**/{ext}"))[:20]:
                content = read_file_safe(f)
                if "type Query" in content or "graphql" in content.lower():
                    api_types.append("graphql")
                    break
            if "graphql" in api_types:
                break

    # gRPC
    if list(root.glob("**/*.proto")):
        api_types.append("grpc")

    # REST is assumed if we have API endpoints
    # This is a simplification - most apps have REST
    api_types.append("rest")

    return list(set(api_types))


def detect_compliance_indicators(root: Path) -> list:
    """Detect compliance requirements from documentation."""
    indicators = []

    # Files to check
    doc_files = [
        root / "README.md",
        root / "readme.md",
        root / "SECURITY.md",
        root / "docs" / "README.md",
        root / "COMPLIANCE.md",
    ]

    content = ""
    for f in doc_files:
        if f.exists():
            content += read_file_safe(f).lower()

    # Also check for compliance-related folders
    for folder in ["compliance", "security", "docs"]:
        folder_path = root / folder
        if folder_path.exists() and folder_path.is_dir():
            for f in folder_path.glob("*.md"):
                content += read_file_safe(f).lower()

    # Compliance patterns
    patterns = {
        "hipaa": r'\bhipaa\b|\bphi\b|\bprotected health\b',
        "pci-dss": r'\bpci[\s-]?dss\b|\bpayment card\b|\bcardholder\b',
        "gdpr": r'\bgdpr\b|\bdata subject\b|\beu data\b',
        "soc2": r'\bsoc\s*2\b|\btrust services\b',
        "iso-27001": r'\biso[\s-]?27001\b',
        "fedramp": r'\bfedramp\b|\bfederal\b',
    }

    for compliance, pattern in patterns.items():
        if re.search(pattern, content):
            indicators.append(compliance)

    return indicators


def determine_app_type(platforms: list, frameworks: list) -> str:
    """Determine primary application type."""
    if "ios" in platforms or "android" in platforms:
        if "web" in platforms:
            return "full-stack"
        return "mobile"

    if any(f in frameworks for f in ["express", "fastapi", "django", "flask", "nestjs", "spring-boot"]):
        if any(f in frameworks for f in ["react", "vue", "angular", "next.js", "nuxt"]):
            return "full-stack"
        return "api"

    if any(f in frameworks for f in ["react", "vue", "angular", "next.js", "nuxt", "svelte"]):
        return "web"

    return "unknown"


def recommend_audits(detection: dict) -> dict:
    """Recommend audit phases and specialized audits."""
    specialized = []

    # Always recommend core phases
    phases = list(range(13))  # Phases 0-12

    # Mobile audit
    if "ios" in detection["platforms"] or "android" in detection["platforms"]:
        specialized.append("mobile")

    # Cloud audits
    if detection["cloud"] == "aws":
        specialized.append("aws")
    elif detection["cloud"] == "gcp":
        specialized.append("gcp")
    elif detection["cloud"] == "azure":
        specialized.append("azure")

    # Infrastructure audits
    if "kubernetes" in detection["infrastructure"]:
        specialized.append("kubernetes")

    # API audits
    if "graphql" in detection["api_type"]:
        specialized.append("graphql")

    return {
        "recommended_phases": phases,
        "recommended_specialized": specialized
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python detect_stack.py /path/to/target", file=sys.stderr)
        sys.exit(1)

    target = Path(sys.argv[1]).resolve()

    if not target.exists():
        print(f"Error: Path does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    # Detect technologies
    platforms = ["web"]  # Default to web
    frameworks = []

    # Node.js/JavaScript
    node = detect_node_frameworks(target)
    frameworks.extend(node["frameworks"])
    if node["is_mobile"]:
        platforms.extend(["ios", "android"])

    # Python
    python = detect_python_frameworks(target)
    frameworks.extend(python["frameworks"])

    # Ruby
    ruby = detect_ruby_frameworks(target)
    frameworks.extend(ruby["frameworks"])

    # PHP
    php = detect_php_frameworks(target)
    frameworks.extend(php["frameworks"])

    # Java
    java = detect_java_frameworks(target)
    frameworks.extend(java["frameworks"])

    # Mobile platforms
    if detect_ios(target) and "ios" not in platforms:
        platforms.append("ios")
    if detect_android(target) and "android" not in platforms:
        platforms.append("android")
    if detect_flutter(target):
        platforms.extend(["ios", "android"])
        frameworks.append("flutter")

    # Cloud provider
    cloud = detect_cloud_provider(target)

    # Infrastructure
    infrastructure = detect_infrastructure(target)

    # API type
    api_type = detect_api_type(target)

    # Compliance indicators
    compliance = detect_compliance_indicators(target)

    # Build detection result
    detection = {
        "platforms": list(set(platforms)),
        "frameworks": list(set(frameworks)),
        "cloud": cloud,
        "infrastructure": infrastructure,
        "api_type": api_type,
        "compliance_indicators": compliance,
    }

    # Determine app type
    detection["app_type"] = determine_app_type(detection["platforms"], detection["frameworks"])

    # Get recommendations
    recommendations = recommend_audits(detection)
    detection.update(recommendations)

    # Output JSON
    print(json.dumps(detection, indent=2))


if __name__ == "__main__":
    main()
